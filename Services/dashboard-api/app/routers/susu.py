import datetime as dt

from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from sqlalchemy import func, and_
from sqlalchemy.orm import Session

from app.database.connection import SessionLocal
from app.database.models import DimLokasi, DimWaktu, DimMitraBisnis, FactDistribusi, FactProduksi, DimUnitPeternakan
from app.schemas.susu import SusuMasterData


router = APIRouter(redirect_slashes=False)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        

@router.get(path='/susu')
async def get_susu_data(db: Session = Depends(get_db),
                        tahun: int | None = None,
                        provinsi: str | None = None,
                        unit_peternakan: str | None = None):
    
    responses = {}
    
    # Get Year
    dis_id_waktu_list = (
        db.query(FactDistribusi.id_waktu)
        .distinct()
        .all()
    )
    
    pro_id_waktu_list = (
        db.query(FactProduksi.id_waktu)
        .distinct()
        .all()
    )
    
    pro_dis_id_waktu_list = []
    for item in dis_id_waktu_list + pro_id_waktu_list:
        if item[0] not in pro_dis_id_waktu_list:
            pro_dis_id_waktu_list.append(item[0])
    
    year_list = (
        db.query(DimWaktu.tahun)
        .where(DimWaktu.id.in_(pro_dis_id_waktu_list))
        .distinct()
        .all()
    )
    year_list = [year[0] for year in year_list]
    
    if tahun is not None:
        year_list = [tahun]
    
    for year in year_list:
        responses[year] = {}
        
        dis_id_lokasi_list = (
            db.query(FactDistribusi.id_lokasi)
            .where(FactDistribusi.id_waktu.in_([
                item[0]
                for item in (
                    db.query(DimWaktu.id)
                    .where(DimWaktu.tahun == year)
                    .all()
                )
            ]))
            .distinct()
            .all()
        )
        
        pro_id_lokasi_list = (
            db.query(FactProduksi.id_lokasi)
            .where(FactProduksi.id_waktu.in_([
                item[0]
                for item in (
                    db.query(DimWaktu.id)
                    .where(DimWaktu.tahun == year)
                    .all()
                )
            ]))
            .distinct()
            .all()
        )
        
        pro_dis_id_lokasi_list = []
        for item in dis_id_lokasi_list + pro_id_lokasi_list:
            if item[0] not in pro_dis_id_lokasi_list:
                pro_dis_id_lokasi_list.append(item[0])
                
        if provinsi is not None:
            pro_dis_id_lokasi_list = [
                item[0]
                for item in (
                    db.query(DimLokasi.id)
                    .where(DimLokasi.provinsi == provinsi)
                    .all()
                )
            ]

        if unit_peternakan is not None:
            id_unit_peternakan = (
                db.query(DimUnitPeternakan.id)
                .where(DimUnitPeternakan.nama_unit == unit_peternakan)
                .first()
            )
                
        # Search data in every location
        for id_lokasi in pro_dis_id_lokasi_list:
            
            lokasi_data = (
                db.query(DimLokasi.provinsi, 
                         DimLokasi.kabupaten_kota, 
                         DimLokasi.kecamatan)
                .where(DimLokasi.id == id_lokasi)
                .first()
            )
            
            if lokasi_data[1] is None:
                lokasi_str = f"{lokasi_data[0]}" 
            else:
                if lokasi_data[2] is None:
                    lokasi_str = f"{lokasi_data[0]} - {lokasi_data[1]}"
                else:
                    lokasi_str = f"{lokasi_data[0]} - {lokasi_data[1]} - {lokasi_data[2]}"
                    
            responses[year][lokasi_str] = {}
            
            
            # Get Susu Segar Data
            responses[year][lokasi_str]['susu_segar'] = {}
            query = (
                db.query(func.sum(FactDistribusi.jumlah_distribusi))
                .where(FactDistribusi.id_jenis_produk == 3)
                .where(FactDistribusi.id_lokasi == id_lokasi)
                .where(FactDistribusi.id_waktu.in_([
                    item[0]
                    for item in (
                        db.query(DimWaktu.id)
                        .where(DimWaktu.tahun == year)
                        .all()
                    )
                ]))
                # .scalar()
            )
            
            if id_unit_peternakan is not None:
                query = query.where(FactDistribusi.id_unit_peternak == id_unit_peternakan)
                
            dis_susu_segar = query.scalar()
            
            if dis_susu_segar is None:
                responses[year][lokasi_str]['susu_segar']['distribusi'] = 0
            else:
                responses[year][lokasi_str]['susu_segar']['distribusi'] = dis_susu_segar
                
            query = (
                db.query(func.sum(FactProduksi.jumlah_produksi))
                .where(FactProduksi.id_jenis_produk == 3)
                .where(FactProduksi.id_lokasi == id_lokasi)
                .where(FactProduksi.id_waktu.in_([
                    item[0]
                    for item in (
                        db.query(DimWaktu.id)
                        .where(DimWaktu.tahun == year)
                        .all()
                    )
                ]))
                # .scalar()
            )
            
            if id_unit_peternakan is not None:
                query = query.where(FactProduksi.id_unit_peternak == id_unit_peternakan)
            
            pro_susu_segar = query.scalar()
            
            if pro_susu_segar is None:
                responses[year][lokasi_str]['susu_segar']['produksi'] = 0
            else:
                responses[year][lokasi_str]['susu_segar']['produksi'] = pro_susu_segar
            
                
            # Get Susu Pasteurisasi Data
            responses[year][lokasi_str]['susu_pasteurisasi'] = {}
            query = (
                db.query(func.sum(FactDistribusi.jumlah_distribusi))
                .where(FactDistribusi.id_jenis_produk == 4)
                .where(FactDistribusi.id_lokasi == id_lokasi)
                .where(FactDistribusi.id_waktu.in_([
                    item[0]
                    for item in (
                        db.query(DimWaktu.id)
                        .where(DimWaktu.tahun == year)
                        .all()
                    )
                ]))
                # .scalar()
            )
            
            if id_unit_peternakan is not None:
                query = query.where(FactDistribusi.id_unit_peternak == id_unit_peternakan)
            
            dis_susu_pasteurisasi = query.scalar()
            
            if dis_susu_pasteurisasi is None:
                responses[year][lokasi_str]['susu_pasteurisasi']['distribusi'] = 0
            else:
                responses[year][lokasi_str]['susu_pasteurisasi']['distribusi'] = dis_susu_pasteurisasi
                
            query = (
                db.query(func.sum(FactProduksi.jumlah_produksi))
                .where(FactProduksi.id_jenis_produk == 4)
                .where(FactProduksi.id_lokasi == id_lokasi)
                .where(FactProduksi.id_waktu.in_([
                    item[0]
                    for item in (
                        db.query(DimWaktu.id)
                        .where(DimWaktu.tahun == year)
                        .all()
                    )
                ]))
                # .scalar()
            )
            
            if id_unit_peternakan is not None:
                query = query.where(FactProduksi.id_unit_peternak == id_unit_peternakan)
                
            pro_susu_pasteurisasi = query.scalar()
            
            if pro_susu_pasteurisasi is None:
                responses[year][lokasi_str]['susu_pasteurisasi']['produksi'] = 0
            else:
                responses[year][lokasi_str]['susu_pasteurisasi']['produksi'] = pro_susu_pasteurisasi
                
            
            # Get Susu Kefir Data
            responses[year][lokasi_str]['susu_kefir'] = {}
            query = (
                db.query(func.sum(FactDistribusi.jumlah_distribusi))
                .where(FactDistribusi.id_jenis_produk == 5)
                .where(FactDistribusi.id_lokasi == id_lokasi)
                .where(FactDistribusi.id_waktu.in_([
                    item[0]
                    for item in (
                        db.query(DimWaktu.id)
                        .where(DimWaktu.tahun == year)
                        .all()
                    )
                ]))
                # .scalar()
            )
            
            if id_unit_peternakan is not None:
                query = query.where(FactDistribusi.id_unit_peternak == id_unit_peternakan)
                
            dis_susu_kefir = query.scalar()
            
            if dis_susu_kefir is None:
                responses[year][lokasi_str]['susu_kefir']['distribusi'] = 0
            else:
                responses[year][lokasi_str]['susu_kefir']['distribusi'] = dis_susu_kefir
            
            query = (
                db.query(func.sum(FactProduksi.jumlah_produksi))
                .where(FactProduksi.id_jenis_produk == 5)
                .where(FactProduksi.id_lokasi == id_lokasi)
                .where(FactProduksi.id_waktu.in_([
                    item[0]
                    for item in (
                        db.query(DimWaktu.id)
                        .where(DimWaktu.tahun == year)
                        .all()
                    )
                ]))
                # .scalar()
            )
            
            if id_unit_peternakan is not None:
                query = query.where(FactProduksi.id_unit_peternak == id_unit_peternakan)
                
            pro_susu_kefir = query.scalar()
            
            if pro_susu_kefir is None:
                responses[year][lokasi_str]['susu_kefir']['produksi'] = 0
            else:
                responses[year][lokasi_str]['susu_kefir']['produksi'] = pro_susu_kefir
                
            
            # Get Yogurt Data
            responses[year][lokasi_str]['yogurt'] = {}
            query = (
                db.query(func.sum(FactDistribusi.jumlah_distribusi))
                .where(FactDistribusi.id_jenis_produk == 6)
                .where(FactDistribusi.id_lokasi == id_lokasi)
                .where(FactDistribusi.id_waktu.in_([
                    item[0]
                    for item in (
                        db.query(DimWaktu.id)
                        .where(DimWaktu.tahun == year)
                        .all()
                    )
                ]))
                # .scalar()
            )
            
            if id_unit_peternakan is not None:
                query = query.where(FactDistribusi.id_unit_peternak == id_unit_peternakan)
                
            dis_yogurt = query.scalar()
            
            if dis_yogurt is None:
                responses[year][lokasi_str]['yogurt']['distribusi'] = 0
            else:
                responses[year][lokasi_str]['yogurt']['distribusi'] = dis_yogurt
                
            query = (
                db.query(func.sum(FactProduksi.jumlah_produksi))
                .where(FactProduksi.id_jenis_produk == 6)
                .where(FactProduksi.id_lokasi == id_lokasi)
                .where(FactProduksi.id_waktu.in_([
                    item[0]
                    for item in (
                        db.query(DimWaktu.id)
                        .where(DimWaktu.tahun == year)
                        .all()
                    )
                ]))
                # .scalar()
            )
            
            if id_unit_peternakan is not None:
                query = query.where(FactProduksi.id_unit_peternak == id_unit_peternakan)
                
            pro_yogurt = query.scalar()
            
            if pro_yogurt is None:
                responses[year][lokasi_str]['yogurt']['produksi'] = 0
            else:
                responses[year][lokasi_str]['yogurt']['produksi'] = pro_yogurt 
                
            
            # Get Keju Data
            responses[year][lokasi_str]['keju'] = {}
            query = (
                db.query(func.sum(FactDistribusi.jumlah_distribusi))
                .where(FactDistribusi.id_jenis_produk == 7)
                .where(FactDistribusi.id_lokasi == id_lokasi)
                .where(FactDistribusi.id_waktu.in_([
                    item[0]
                    for item in (
                        db.query(DimWaktu.id)
                        .where(DimWaktu.tahun == year)
                        .all()
                    )
                ]))
                # .scalar()
            )
            
            if id_unit_peternakan is not None:
                query = query.where(FactDistribusi.id_unit_peternak == id_unit_peternakan)
                
            dis_keju = query.scalar()
            
            if dis_keju is None:
                responses[year][lokasi_str]['keju']['distribusi'] = 0
            else:
                responses[year][lokasi_str]['keju']['distribusi'] = dis_keju
                
            query = (
                db.query(func.sum(FactProduksi.jumlah_produksi))
                .where(FactProduksi.id_jenis_produk == 7)
                .where(FactProduksi.id_lokasi == id_lokasi)
                .where(FactProduksi.id_waktu.in_([
                    item[0]
                    for item in (
                        db.query(DimWaktu.id)
                        .where(DimWaktu.tahun == year)
                        .all()
                    )
                ]))
                # .scalar()
            )
            
            if id_unit_peternakan is not None:
                query = query.where(FactProduksi.id_unit_peternak == id_unit_peternakan)
                
            pro_keju = query.scalar()
            
            if pro_keju is None:
                responses[year][lokasi_str]['keju']['produksi'] = 0
            else:
                responses[year][lokasi_str]['keju']['produksi'] = pro_keju
                
            
            # Get Prediction Data
            responses[year][lokasi_str]['prediksi_produksi_susu_segar'] = []
            responses[year][lokasi_str]['prediksi_produksi'] = None
            # Belum ada tabel prediksi
            
            
            total_produksi = (
                responses[year][lokasi_str]['susu_segar']['produksi'] + \
                responses[year][lokasi_str]['susu_pasteurisasi']['produksi'] + \
                responses[year][lokasi_str]['susu_kefir']['produksi'] + \
                responses[year][lokasi_str]['yogurt']['produksi']
            )
            
            total_distribusi = (
                responses[year][lokasi_str]['susu_segar']['distribusi'] + \
                responses[year][lokasi_str]['susu_pasteurisasi']['distribusi'] + \
                responses[year][lokasi_str]['susu_kefir']['distribusi'] + \
                responses[year][lokasi_str]['yogurt']['distribusi']
            )
            
            # Get percentage produksi
            responses[year][lokasi_str]['persentase_produksi'] = {}
            if total_produksi != 0:
                responses[year][lokasi_str]['persentase_produksi']['susu_segar'] = round(
                    responses[year][lokasi_str]['susu_segar']['produksi'] / total_produksi, 2
                )
                responses[year][lokasi_str]['persentase_produksi']['susu_pasteurisasi'] = round(
                    responses[year][lokasi_str]['susu_pasteurisasi']['produksi'] / total_produksi, 2
                )
                responses[year][lokasi_str]['persentase_produksi']['susu_kefir'] = round(
                    responses[year][lokasi_str]['susu_kefir']['produksi'] / total_produksi, 2
                )
                responses[year][lokasi_str]['persentase_produksi']['yogurt'] = round(
                    responses[year][lokasi_str]['yogurt']['produksi'] / total_produksi, 2
                )
            else:
                responses[year][lokasi_str]['persentase_produksi']['susu_segar'] = 0
                responses[year][lokasi_str]['persentase_produksi']['susu_pasteurisasi'] = 0
                responses[year][lokasi_str]['persentase_produksi']['susu_kefir'] = 0
                responses[year][lokasi_str]['persentase_produksi']['yogurt'] = 0
                
            # Get percentage distribusi
            responses[year][lokasi_str]['persentase_distribusi'] = {}
            if total_distribusi != 0:
                responses[year][lokasi_str]['persentase_distribusi']['susu_segar'] = round(
                    responses[year][lokasi_str]['susu_segar']['distribusi'] / total_distribusi, 2
                )
                responses[year][lokasi_str]['persentase_distribusi']['susu_pasteurisasi'] = round(
                    responses[year][lokasi_str]['susu_pasteurisasi']['distribusi'] / total_distribusi, 2
                )
                responses[year][lokasi_str]['persentase_distribusi']['susu_kefir'] = round(
                    responses[year][lokasi_str]['susu_kefir']['distribusi'] / total_distribusi, 2
                )
                responses[year][lokasi_str]['persentase_distribusi']['yogurt'] = round(
                    responses[year][lokasi_str]['yogurt']['distribusi'] / total_distribusi, 2
                )
            else:
                responses[year][lokasi_str]['persentase_distribusi']['susu_segar'] = 0
                responses[year][lokasi_str]['persentase_distribusi']['susu_pasteurisasi'] = 0
                responses[year][lokasi_str]['persentase_distribusi']['susu_kefir'] = 0
                responses[year][lokasi_str]['persentase_distribusi']['yogurt'] = 0
                
            # Get produksi and distribusi in location 7 days
            start_date = datetime.today() - timedelta(days=7)
            end_date = datetime.today()
            
            all_dates = {
                (start_date + timedelta(days=x)).strftime("%Y-%m-%d"): 0
                for x in range((end_date - start_date).days + 1)
            }
            
            id_waktu_list = (
                db.query(DimWaktu.id,
                         DimWaktu.tanggal)
                .where(DimWaktu.tanggal.in_(all_dates.keys()))
                .all()
            )
            
            id_waktu_dict = {
                id_waktu[0]: id_waktu[1].strftime("%Y-%m-%d")
                for id_waktu in id_waktu_list
            }
            
            
            responses[year][lokasi_str]['prod_dis'] = {}
            
            # Distribusi
            dis_susu_segar_list = (
                db.query(FactDistribusi.id_waktu, func.sum(FactDistribusi.jumlah_distribusi))
                .where(and_(FactDistribusi.id_jenis_produk == 3,
                            FactDistribusi.id_lokasi == id_lokasi,
                            FactDistribusi.id_waktu.in_(id_waktu_dict.keys())))
                .group_by(FactDistribusi.id_waktu)
                .all()
            )
            
            dis_susu_segar_result = {}
            for dis_susu_segar in dis_susu_segar_list:
                dis_susu_segar_result[id_waktu_dict[dis_susu_segar[0]]] = dis_susu_segar[1]
            
            responses[year][lokasi_str]['prod_dis']['distribusi'] = all_dates.copy()
            responses[year][lokasi_str]['prod_dis']['distribusi'].update(dis_susu_segar_result)
            
            # Produksi
            pro_susu_segar_list = (
                db.query(FactProduksi.id_waktu, func.sum(FactProduksi.jumlah_produksi))
                .where(and_(FactProduksi.id_jenis_produk == 3,
                            FactProduksi.id_lokasi == id_lokasi,
                            FactProduksi.id_waktu.in_(id_waktu_dict.keys())))
                .group_by(FactProduksi.id_waktu)
                .all()
            )
            
            pro_susu_segar_result = {}
            for pro_susu_segar in pro_susu_segar_list:
                pro_susu_segar_result[id_waktu_dict[pro_susu_segar[0]]] = pro_susu_segar[1]
            
            responses[year][lokasi_str]['prod_dis']['produksi'] = all_dates.copy()
            responses[year][lokasi_str]['prod_dis']['produksi'].update(pro_susu_segar_result)

            
            # Permintaan susu segar by mitra bisnis
            responses[year][lokasi_str]['permintaan_susu_segar_dari_mitra'] = {}
            
            aggregate_by_mitra = (
                db.query(DimMitraBisnis.nama_mitra_bisnis, func.sum(FactDistribusi.jumlah_distribusi))
                .where(and_(FactDistribusi.id_jenis_produk == 3,
                            FactDistribusi.id_lokasi == id_lokasi,
                            FactDistribusi.id_waktu.in_([
                                item[0]
                                for item in (
                                    db.query(DimWaktu.id)
                                    .where(DimWaktu.tahun == year)
                                    .all()
                                )]
                            )))
                .join(DimMitraBisnis, DimMitraBisnis.id == FactDistribusi.id_mitra_bisnis)
                .group_by(DimMitraBisnis.nama_mitra_bisnis)
                .all()
            )
            mitra_result_dict = {}
            for item in aggregate_by_mitra:
                mitra_result_dict[item[0]] = item[1]
                
            responses[year][lokasi_str]['permintaan_susu_segar_dari_mitra'] = mitra_result_dict
            
            
            # Get persentase distribusi data
            try:
                responses[year][lokasi_str]['persentase_distribusi'] = round(
                    (
                        responses[year][lokasi_str]['susu_segar']['distribusi'] + \
                        responses[year][lokasi_str]['susu_pasteurisasi']['distribusi'] + \
                        responses[year][lokasi_str]['susu_kefir']['distribusi'] + \
                        responses[year][lokasi_str]['yogurt']['distribusi'] + \
                        responses[year][lokasi_str]['keju']['distribusi']
                    ) / (
                        responses[year][lokasi_str]['susu_segar']['produksi'] + \
                        responses[year][lokasi_str]['susu_pasteurisasi']['produksi'] + \
                        responses[year][lokasi_str]['susu_kefir']['produksi'] + \
                        responses[year][lokasi_str]['yogurt']['produksi'] + \
                        responses[year][lokasi_str]['keju']['produksi']
                    ), 2
                )
            except:
                responses[year][lokasi_str]['total_persentase_distribusi'] = 0
            
            
            # Get total pendapatan
            distribusi_data_list = (
                db.query(FactDistribusi.jumlah_distribusi, FactDistribusi.harga_rata_rata)
                .where(and_(FactDistribusi.id_lokasi == id_lokasi,
                            FactDistribusi.id_jenis_produk == 3,
                            FactDistribusi.id_waktu.in_([
                                item[0]
                                for item in (
                                    db.query(DimWaktu.id)
                                    .where(DimWaktu.tahun == year)
                                    .all()
                                )]
                            )))
                .all()
            )
            
            total_pendapatan = 0
            for distribusi_data in distribusi_data_list:
                total_pendapatan += distribusi_data[0] * distribusi_data[1]
                
            responses[year][lokasi_str]['total_pendapatan'] = total_pendapatan
            
            # Get min, max, and average harga
            responses[year][lokasi_str]['harga_susu'] = {}

            harga_minimum = (
                db.query(func.min(FactDistribusi.harga_minimum))
                .where(and_(FactDistribusi.id_lokasi == id_lokasi,
                            FactDistribusi.id_jenis_produk == 3,
                            FactDistribusi.id_waktu.in_([
                                item[0]
                                for item in (
                                    db.query(DimWaktu.id)
                                    .where(DimWaktu.tahun == year)
                                    .all()
                                )]
                            )))
                .scalar()
            )
            
            if harga_minimum is not None:
                responses[year][lokasi_str]['harga_susu']['minimum'] = harga_minimum
            else:
                responses[year][lokasi_str]['harga_susu']['minimum'] = 0
                     
            harga_maksimum = (
                db.query(func.max(FactDistribusi.harga_maximum))
                .where(and_(FactDistribusi.id_lokasi == id_lokasi,
                            FactDistribusi.id_jenis_produk == 3,
                            FactDistribusi.id_waktu.in_([
                                item[0]
                                for item in (
                                    db.query(DimWaktu.id)
                                    .where(DimWaktu.tahun == year)
                                    .all()
                                )]
                            )))
                .scalar()
            )
            
            if harga_maksimum is not None:
                responses[year][lokasi_str]['harga_susu']['maximum'] = harga_maksimum
            else:
                responses[year][lokasi_str]['harga_susu']['maximum'] = 0
                    
            harga_rataan = (
                db.query(func.avg(FactDistribusi.harga_rata_rata))
                .where(and_(FactDistribusi.id_lokasi == id_lokasi,
                            FactDistribusi.id_jenis_produk == 3,
                            FactDistribusi.id_waktu.in_([
                                item[0]
                                for item in (
                                    db.query(DimWaktu.id)
                                    .where(DimWaktu.tahun == year)
                                    .all()
                                )]
                            )))
                .scalar()
            )
            
            if harga_rataan is not None:
                responses[year][lokasi_str]['harga_susu']['rata_rata'] = float(harga_rataan)
            else:
                responses[year][lokasi_str]['harga_susu']['rata_rata'] = 0
            
                
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=responses
    )
     