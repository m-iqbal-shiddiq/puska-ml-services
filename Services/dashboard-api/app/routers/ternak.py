import datetime as dt

from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from sqlalchemy import func, and_, text
from sqlalchemy.orm import Session

from app.database.connection import SessionLocal
from app.database.models import DimLokasi, DimWaktu, FactDistribusi, FactProduksi, FactPopulasi
from app.schemas.ternak import TernakMasterData


router = APIRouter(redirect_slashes=False)

def get_db(): 
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        

@router.get(path='/ternak', 
            response_model=TernakMasterData, 
            status_code=status.HTTP_200_OK)
async def get_ternak_data(db: Session = Depends(get_db),
                          tahun: int | None = None,
                          provinsi: str | None = None,
                          kabupaten_kota: str | None = None,
                          perah_pedaging: str | None = None,
                          jantan_betina: str | None = None,
                          dewasa_anakan: str | None = None):
    
    
    responses = {}
    
    
    ### Get ternak_potong data ###
    responses['ternak_potong'] = {}
    
    responses['ternak_potong']['total_distribusi'] = (
        db.query(func.sum(FactDistribusi.jumlah_distribusi))
        .where(FactDistribusi.id_jenis_produk == 2)
        .scalar()
    )
    
    responses['ternak_potong']['total_produksi'] = (
        db.query(func.sum(FactDistribusi.jumlah_penjualan))
        .where(FactDistribusi.id_jenis_produk == 2)
        .scalar()
    )
    
    if responses['ternak_potong']['total_distribusi'] is None:
        responses['ternak_potong']['total_distribusi'] = 0
        
    if responses['ternak_potong']['total_produksi'] is None:
        responses['ternak_potong']['total_produksi'] = 0
        responses['ternak_potong']['persentase'] = 0
    else:
        responses['ternak_potong']['persentase'] = round(
            (responses['ternak_potong']['total_distribusi'] / responses['ternak_potong']['total_produksi']) * 100,
            2
        )
    
    
    ### Get daging_ternak data ###
    responses['daging_ternak'] = {}
    
    responses['daging_ternak']['total_distribusi'] = (
        db.query(func.sum(FactDistribusi.jumlah_distribusi))
        .where(FactDistribusi.id_jenis_produk == 1)
        .scalar()
    )
          
    responses['daging_ternak']['total_produksi'] = (
        db.query(func.sum(FactDistribusi.jumlah_penjualan))
        .where(FactDistribusi.id_jenis_produk == 1)
        .scalar()
    )
    
    if responses['daging_ternak']['total_distribusi'] is None:
        responses['daging_ternak']['total_distribusi'] = 0
    
    if responses['daging_ternak']['total_produksi'] is None:
        responses['daging_ternak']['total_produksi'] = 0
        responses['daging_ternak']['persentase'] = 0
    else:
        responses['daging_ternak']['persentase'] = round(
            (responses['daging_ternak']['total_distribusi'] / responses['daging_ternak']['total_produksi']) * 100,
            2
        )
    
    
    ### Get susu_segar data ###
    responses['susu_segar'] = {}
    
    responses['susu_segar']['total_distribusi'] = (
        db.query(func.sum(FactDistribusi.jumlah_distribusi))
        .where(FactDistribusi.id_jenis_produk == 3)
        .scalar()
    )
    
    responses['susu_segar']['total_produksi'] = (
        db.query(func.sum(FactDistribusi.jumlah_penjualan))
        .where(FactDistribusi.id_jenis_produk == 3)
        .scalar()
    )
    
    if responses['susu_segar']['total_distribusi'] is None:
        responses['susu_segar']['total_distribusi'] = 0
    
    if responses['susu_segar']['total_produksi'] is None:
        responses['susu_segar']['total_produksi'] = 0
        responses['susu_segar']['persentase'] = 0
    else:
        responses['susu_segar']['persentase'] = round(
            (responses['susu_segar']['total_distribusi'] / responses['susu_segar']['total_produksi']) * 100,
            2
        )

        
    ### Get first date in database and current date ###    
    end_date = dt.date.today()
    # end_date = datetime.strptime("2023-01-07", "%Y-%m-%d")
    start_date = end_date - timedelta(days=7)
    
    all_dates = {
        (start_date + timedelta(days=x)).strftime("%Y-%m-%d"): 0
        for x in range((end_date - start_date).days + 1)
    }
    
        
    ### Get Produksi dan Distribusi Ternak Potong ###
    responses['pro_dis_ternak_potong'] = {}
    
    # Distribusi
    dis_ternak_potong_list = (
        db.query(DimWaktu.tanggal,
                 func.sum(FactDistribusi.jumlah_distribusi))
        .where(and_(FactDistribusi.id_jenis_produk == 2,
                    DimWaktu.tanggal >= start_date))
        .join(DimWaktu, FactDistribusi.id_waktu == DimWaktu.id)
        .group_by(DimWaktu.tanggal)
        .order_by(DimWaktu.tanggal)
        .all()
    )
    
    if len(dis_ternak_potong_list) == 0:
        dis_ternak_potong_dict = {}
    else:
        dis_ternak_potong_dict = {
            dis_ternak_potong_list[i][0].strftime("%Y-%m-%d"): dis_ternak_potong_list[i][1]
            for i in range(len(dis_ternak_potong_list))
        }
        
    dis_ternak_potong_result = all_dates.copy()
    dis_ternak_potong_result.update(dis_ternak_potong_dict)
    
    # Produksi
    pro_ternak_potong_list = (
        db.query(DimWaktu.tanggal,
                 func.sum(FactProduksi.jumlah_produksi))
        .where(and_(FactProduksi.id_jenis_produk == 2,
                    DimWaktu.tanggal >= start_date))
        .join(DimWaktu, FactProduksi.id_waktu == DimWaktu.id)
        .group_by(DimWaktu.tanggal)
        .order_by(DimWaktu.tanggal)
        .all()
    )
    
    if len(pro_ternak_potong_list) == 0:
        pro_ternak_potong_dict = {}
    else:
        pro_ternak_potong_dict = {
            pro_ternak_potong_list[i][0].strftime("%Y-%m-%d"): pro_ternak_potong_list[i][1]
            for i in range(len(pro_ternak_potong_list))
        }
    
    pro_ternak_potong_result = all_dates.copy()
    pro_ternak_potong_result.update(pro_ternak_potong_dict)
    
    pro_dis_ternak_potong_list = []
    for date in pro_ternak_potong_result.keys():
        pro_dis_ternak_potong_list.append({
            'label': date,
            'distribusi': dis_ternak_potong_result[date],
            'produksi': pro_ternak_potong_result[date]
        })
        
    responses['pro_dis_ternak_potong'] = pro_dis_ternak_potong_list


    ### Get Produksi dan Distribusi Daging Ternak ###
    responses['pro_dis_daging_ternak'] = {}
    
    # Distribusi
    dis_daging_ternak_list = (
        db.query(DimWaktu.tanggal,
                 func.sum(FactDistribusi.jumlah_distribusi))
        .where(and_(FactDistribusi.id_jenis_produk == 1,
                    DimWaktu.tanggal >= start_date))
        .join(DimWaktu, FactDistribusi.id_waktu == DimWaktu.id)
        .group_by(DimWaktu.tanggal)
        .order_by(DimWaktu.tanggal)
        .all()
    )
    
    if len(dis_daging_ternak_list) == 0:
        dis_daging_ternak_dict = {}
    else:
        dis_daging_ternak_dict = {
            dis_daging_ternak_list[i][0].strftime("%Y-%m-%d"): dis_daging_ternak_list[i][1]
            for i in range(len(dis_daging_ternak_list))
        }
        
    dis_daging_ternak_result = all_dates.copy()
    dis_daging_ternak_result.update(dis_daging_ternak_dict)
    
    # Produksi
    pro_daging_ternak_list = (
        db.query(DimWaktu.tanggal,
                 func.sum(FactProduksi.jumlah_produksi))
        .where(and_(FactProduksi.id_jenis_produk == 1,
                    DimWaktu.tanggal >= start_date))
        .join(DimWaktu, FactProduksi.id_waktu == DimWaktu.id)
        .group_by(DimWaktu.tanggal)
        .order_by(DimWaktu.tanggal)
        .all()
    )
    
    if len(pro_daging_ternak_list) == 0:
        pro_daging_ternak_dict = {}
    else:
        pro_daging_ternak_dict = {
            pro_daging_ternak_list[i][0].strftime("%Y-%m-%d"): pro_daging_ternak_list[i][1]
            for i in range(len(pro_daging_ternak_list))
        }
    
    pro_daging_ternak_result = all_dates.copy()
    pro_daging_ternak_result.update(pro_daging_ternak_dict)
    
    pro_dis_daging_ternak_list = []
    for date in pro_daging_ternak_result.keys():
        pro_dis_daging_ternak_list.append({
            'label': date,
            'distribusi': dis_daging_ternak_result[date],
            'produksi': pro_daging_ternak_result[date]
        })
        
    responses['pro_dis_daging_ternak'] = pro_dis_daging_ternak_list

    
    ### Get Produksi dan Distribusi Susu Segar ###
    responses['pro_dis_susu_segar'] = {}
    
     # Distribusi
    dis_susu_segar_list = (
        db.query(DimWaktu.tanggal,
                 func.sum(FactDistribusi.jumlah_distribusi))
        .where(and_(FactDistribusi.id_jenis_produk == 3,
                    DimWaktu.tanggal >= start_date))
        .join(DimWaktu, FactDistribusi.id_waktu == DimWaktu.id)
        .group_by(DimWaktu.tanggal)
        .order_by(DimWaktu.tanggal)
        .all()
    )
    
    if len(dis_susu_segar_list) == 0:
        dis_susu_segar_dict = {}
    else:
        dis_susu_segar_dict = {
            dis_susu_segar_list[i][0].strftime("%Y-%m-%d"): dis_susu_segar_list[i][1]
            for i in range(len(dis_susu_segar_list))
        }
        
    dis_susu_segar_result = all_dates.copy()
    dis_susu_segar_result.update(dis_susu_segar_dict)
    
    # Produksi
    pro_susu_segar_list = (
        db.query(DimWaktu.tanggal,
                 func.sum(FactProduksi.jumlah_produksi))
        .where(and_(FactProduksi.id_jenis_produk == 3,
                    DimWaktu.tanggal >= start_date))
        .join(DimWaktu, FactProduksi.id_waktu == DimWaktu.id)
        .group_by(DimWaktu.tanggal)
        .order_by(DimWaktu.tanggal)
        .all()
    )
    
    if len(pro_susu_segar_list) == 0:
        pro_susu_segar_dict = {}
    else:
        pro_susu_segar_dict = {
            pro_susu_segar_list[i][0].strftime("%Y-%m-%d"): pro_susu_segar_list[i][1]
            for i in range(len(pro_susu_segar_list))
        }
    
    pro_susu_segar_result = all_dates.copy()
    pro_susu_segar_result.update(pro_susu_segar_dict)
    
    pro_dis_susu_segar_list = []
    for date in pro_susu_segar_result.keys():
        pro_dis_susu_segar_list.append({
            'label': date,
            'distribusi': dis_susu_segar_result[date],
            'produksi': pro_susu_segar_result[date]
        })
        
    responses['pro_dis_susu_segar'] = pro_dis_susu_segar_list
    
    ### Get sebaran_populasi_all ###
    if  (tahun is None) and (provinsi is None) and \
        (kabupaten_kota is None) and (perah_pedaging is None) and \
        (jantan_betina is None) and (dewasa_anakan is None):
            
            query = (
                db.query(DimWaktu.tahun,
                         DimLokasi.provinsi,
                         func.sum(FactPopulasi.jumlah).label('total_populasi'))
                .join(DimWaktu, FactPopulasi.id_waktu == DimWaktu.id)
                .join(DimLokasi, FactPopulasi.id_lokasi == DimLokasi.id)
                .group_by(DimWaktu.tahun, DimLokasi.provinsi)
                .order_by(DimWaktu.tahun)
            )
            
            results = query.all()
            
            results_dict = {}
            lonlat_dict = {}
            for year, provinsi, total_populasi in results:
                
                if year not in results_dict:
                    results_dict[year] = {
                        'year': year,
                        'sebaran_populasi': []
                    }
                    
                if provinsi not in lonlat_dict:
                    lonlat_dict[provinsi] = {}
                    
                    query = (
                        db.query(DimLokasi.longitude, DimLokasi.langitude)
                        .where(and_(DimLokasi.provinsi == provinsi,
                                    DimLokasi.kabupaten_kota == None,
                                    DimLokasi.kecamatan == None))
                    )
                    
                    lonlat = query.one()
  
                    lonlat_dict[provinsi]['longitude'] = lonlat[0]
                    lonlat_dict[provinsi]['langitude'] = lonlat[1]
                    
                results_dict[year]['sebaran_populasi'].append({
                    'region': f"POINT ({lonlat_dict[provinsi]['longitude']} {lonlat_dict[provinsi]['langitude']})",
                    'title': provinsi,
                    'populasi': int(total_populasi)
                })
                    
            responses['sebaran_populasi_all'] = list(results_dict.values())  
                
    else:
        
        if provinsi:
            query = (
                db.query(DimWaktu.tahun,
                         DimLokasi.provinsi,
                         DimLokasi.kabupaten_kota,
                         FactPopulasi.tipe_ternak,
                         FactPopulasi.jenis_kelamin,
                         FactPopulasi.tipe_usia,
                         func.sum(FactPopulasi.jumlah).label('total_populasi'))
                .join(DimWaktu, FactPopulasi.id_waktu == DimWaktu.id)
                .join(DimLokasi, FactPopulasi.id_lokasi == DimLokasi.id)
            )
        else:
            query = (
                db.query(DimWaktu.tahun,
                         DimLokasi.provinsi,
                         FactPopulasi.tipe_ternak,
                         FactPopulasi.jenis_kelamin,
                         FactPopulasi.tipe_usia,
                         func.sum(FactPopulasi.jumlah).label('total_populasi'))
                .join(DimWaktu, FactPopulasi.id_waktu == DimWaktu.id)
                .join(DimLokasi, FactPopulasi.id_lokasi == DimLokasi.id)
            )
        
        if tahun:
            query = query.where(DimWaktu.tahun == tahun)
        
        if provinsi:
            query = query.where(DimLokasi.provinsi == provinsi)
        
        if kabupaten_kota:
            query = query.where(DimLokasi.kabupaten_kota == kabupaten_kota)
            
        if perah_pedaging:
            query = query.where(FactPopulasi.tipe_ternak == perah_pedaging)
            
        if jantan_betina:
            query = query.where(FactPopulasi.jenis_kelamin == jantan_betina)
            
        if dewasa_anakan:
            query = query.where(FactPopulasi.tipe_usia == dewasa_anakan)
        
        if provinsi:
            results = query.group_by(DimWaktu.tahun,
                                     DimLokasi.provinsi,
                                     DimLokasi.kabupaten_kota,
                                     FactPopulasi.tipe_ternak,
                                     FactPopulasi.jenis_kelamin,
                                     FactPopulasi.tipe_usia).all()
            
            results_dict = {}
            lonlat_dict = {}
            for year, provinsi, kabupaten_kota, tipe_ternak, jenis_kelamin, tipe_usia, total_populasi in results:
                    
                if year not in results_dict:
                    results_dict[year] = {
                        'year': year,
                        'sebaran_populasi': []
                    }
                    
                if kabupaten_kota not in lonlat_dict:
                    lonlat_dict[kabupaten_kota] = {}
                    
                    query = (
                        db.query(DimLokasi.longitude, DimLokasi.langitude)
                        .where(and_(DimLokasi.kabupaten_kota == kabupaten_kota,
                                    DimLokasi.kecamatan == None))
                    )
                    
                    lonlat = query.one()

                    lonlat_dict[kabupaten_kota]['longitude'] = lonlat[0]
                    lonlat_dict[kabupaten_kota]['langitude'] = lonlat[1]
                    
                results_dict[year]['sebaran_populasi'].append({
                    'region': f"POINT ({lonlat_dict[kabupaten_kota]['longitude']} {lonlat_dict[kabupaten_kota]['langitude']})",
                    'title': kabupaten_kota,
                    'populasi': int(total_populasi)
                })
            
            responses['sebaran_populasi'] = list(results_dict.values())
            
        else:     
            results = query.group_by(DimWaktu.tahun,
                                     DimLokasi.provinsi,
                                     FactPopulasi.tipe_ternak,
                                     FactPopulasi.jenis_kelamin,
                                     FactPopulasi.tipe_usia).all()
            
            results_dict = {}
            lonlat_dict = {}
            for year, provinsi, tipe_ternak, jenis_kelamin, tipe_usia, total_populasi in results:
                        
                if year not in results_dict:
                    results_dict[year] = {
                        'year': year,
                        'sebaran_populasi': []
                    }
                    
                if provinsi not in lonlat_dict:
                    lonlat_dict[provinsi] = {}
                    
                    query = (
                        db.query(DimLokasi.longitude, DimLokasi.langitude)
                        .where(and_(DimLokasi.provinsi == provinsi,
                                    DimLokasi.kabupaten_kota == None,
                                    DimLokasi.kecamatan == None))
                    )
                    
                    lonlat = query.one()

                    lonlat_dict[provinsi]['longitude'] = lonlat[0]
                    lonlat_dict[provinsi]['langitude'] = lonlat[1]
                    
                results_dict[year]['sebaran_populasi'].append({
                    'region': f"POINT ({lonlat_dict[provinsi]['longitude']} {lonlat_dict[provinsi]['langitude']})",
                    'title': provinsi,
                    'populasi': int(total_populasi)
                })  
                
            responses['sebaran_populasi'] = list(results_dict.values())
    
    
    ### Get ringkasan_populasi ###
    responses['ringkasan_populasi'] = {
        'jumlah_perah_dewasa': {
            'produksi': 0,
            'distribusi': 0
        },
        'jumlah_perah_anakan': {
            'produksi': 0,
            'distribusi': 0
        },
        'jumlah_pedaging_dewasa': {
            'produksi': 0,
            'distribusi': 0
        },
        'jumlah_pedaging_anakan': {
            'produksi': 0,
            'distribusi': 0
        
        }
    }
    
    
    ### Get table ###
    responses['table'] = [
        {
            'wilayah': 'Aceh',
            'perah_dewasa_jantan': 0,
            'perah_dewasa_betina': 0,
            'perah_anakan_jantan': 0,
            'perah_anakan_betina': 0,
            'pedaging_dewasa_jantan': 0,
            'pedaging_dewasa_betina': 0,
            'pedaging_anakan_jantan': 0,
            'pedaging_anakan_betina': 0
        }
    ]
    
    
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=responses
    )