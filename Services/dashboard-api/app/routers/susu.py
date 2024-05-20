import datetime as dt

from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from sqlalchemy import func, and_
from sqlalchemy.orm import Session

from app.database.connection import SessionLocal
from app.database.models import DimLokasi, DimWaktu, DimMitraBisnis, FactDistribusi, FactProduksi
from app.schemas.susu import SusuMasterData


router = APIRouter(redirect_slashes=False)

def get_db():   
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        

def get_fact_distribusi_data(db: Session,
                             tahun: int,
                             id_jenis_produk: int,
                             provinsi: str | None,
                             kabupaten_kota: str | None):
    
    query = query = (
        db.query(func.sum(FactDistribusi.jumlah_distribusi))
        .join(DimWaktu, DimWaktu.id == FactDistribusi.id_waktu)
        .join(DimLokasi, DimLokasi.id == FactDistribusi.id_lokasi)
        .where(and_(DimWaktu.tahun == tahun,
                    FactDistribusi.id_jenis_produk == id_jenis_produk))
    )
    
    if provinsi:
        query = query.where(DimLokasi.provinsi == provinsi)
    if kabupaten_kota:
        query = query.where(DimLokasi.kabupaten_kota == kabupaten_kota)
        
    if query.scalar() is None:
        return 0
    else:
        return query.scalar()
    

def get_fact_produksi_data(db: Session,
                           tahun: int,
                           id_jenis_produk: int,
                           provinsi: str | None,
                           kabupaten_kota: str | None):
    
    query = (
        db.query(func.sum(FactProduksi.jumlah_produksi))
        .join(DimWaktu, DimWaktu.id == FactProduksi.id_waktu)
        .join(DimLokasi, DimLokasi.id == FactProduksi.id_lokasi)
        .where(and_(DimWaktu.tahun == tahun,
                    FactProduksi.id_jenis_produk == id_jenis_produk))
    )
    
    if provinsi:
        query = query.where(DimLokasi.provinsi == provinsi)
    if kabupaten_kota:
        query = query.where(DimLokasi.kabupaten_kota == kabupaten_kota)
    
    if query.scalar() is None:
        return 0
    else:
        return query.scalar()
       
       

@router.get(path='/susu',
            response_model=SusuMasterData,
            status_code=status.HTTP_200_OK)
async def get_susu_data(db: Session = Depends(get_db),
                        tahun: int = None,
                        provinsi: str | None = None,
                        kabupaten_kota: str | None = None):
    
    responses = {
        'year': tahun,
        'data': {}
    }
    
    
    ### Get susu_segar data ###
    responses['data']['susu_segar'] = {}
    
    # produksi
    responses['data']['susu_segar']['produksi'] = get_fact_produksi_data(
        db=db,
        tahun=tahun,
        id_jenis_produk=3,
        provinsi=provinsi,
        kabupaten_kota=kabupaten_kota
    )
    
    # distribusi
    responses['data']['susu_segar']['distribusi'] = get_fact_distribusi_data(
        db=db,
        tahun=tahun,
        id_jenis_produk=3,
        provinsi=provinsi,
        kabupaten_kota=kabupaten_kota
    )
    
    
    ### Get susu_pasteurisasi data ###
    responses['data']['susu_pasteurisasi'] = {}
    
    # produksi
    responses['data']['susu_pasteurisasi']['produksi'] = get_fact_produksi_data(
        db=db,
        tahun=tahun,
        id_jenis_produk=4,
        provinsi=provinsi,
        kabupaten_kota=kabupaten_kota
    )
    
    # distribusi
    responses['data']['susu_pasteurisasi']['distribusi'] = get_fact_distribusi_data(
        db=db,
        tahun=tahun,
        id_jenis_produk=4,
        provinsi=provinsi,
        kabupaten_kota=kabupaten_kota
    )
    
    
    ### Get susu_kefir data ###
    responses['data']['susu_kefir'] = {}
    
    # produksi
    responses['data']['susu_kefir']['produksi'] = get_fact_produksi_data(
        db=db,
        tahun=tahun,
        id_jenis_produk=5,
        provinsi=provinsi,
        kabupaten_kota=kabupaten_kota
    )
        
    # distribusi
    responses['data']['susu_kefir']['distribusi'] = get_fact_distribusi_data(
        db=db,
        tahun=tahun,
        id_jenis_produk=5,
        provinsi=provinsi,
        kabupaten_kota=kabupaten_kota
    )
    
    
    ### Get yogurt data ###
    responses['data']['yogurt'] = {}
    
    # produksi
    responses['data']['yogurt']['produksi'] = get_fact_produksi_data(
        db=db,
        tahun=tahun,
        id_jenis_produk=6,
        provinsi=provinsi,
        kabupaten_kota=kabupaten_kota
    )
    
    # distribusi
    responses['data']['yogurt']['distribusi'] = get_fact_distribusi_data(
        db=db,
        tahun=tahun,
        id_jenis_produk=6,
        provinsi=provinsi,
        kabupaten_kota=kabupaten_kota
    )
    
    
    ### Get keju data ###
    responses['data']['keju'] = {}
    
    # produksi
    responses['data']['keju']['produksi'] = get_fact_produksi_data(
        db=db,
        tahun=tahun,
        id_jenis_produk=7,
        provinsi=provinsi,
        kabupaten_kota=kabupaten_kota
    )
    
    # distribusi
    responses['data']['keju']['distribusi'] = get_fact_distribusi_data(
        db=db,
        tahun=tahun,
        id_jenis_produk=7,
        provinsi=provinsi,
        kabupaten_kota=kabupaten_kota
    )
    
    
    ### Get prediksi data ###
    responses['data']['prediksi'] = [
        {
            'label': '01-01-2021',
            'actual': 1,
            'predict': 1.5
        },
        {
            'label': '01-02-2021',
            'actual': 1.5,
            'predict': 2
        },
        {
            'label': '01-03-2021',
            'actual': 2,
            'predict': 2.5
        },
        {
            'label': '01-04-2021',
            'actual': 2.5,
            'predict': 3
        },
        {
            'label': '01-05-2021',
            'actual': 3,
            'predict': 3.5
        },
        {
            'label': '01-06-2021',
            'actual': 3.5,
            'predict': 4
        },
        {
            'label': '01-07-2021',
            'actual': 4,
            'predict': 4.5
        }
    ]
    
    
    ### Get persentase produksi data ###
    responses['data']['persentase_produksi'] = {}
    
    total_produksi = (
        responses['data']['susu_segar']['produksi'] + \
        responses['data']['susu_pasteurisasi']['produksi'] + \
        responses['data']['susu_kefir']['produksi'] + \
        responses['data']['yogurt']['produksi']
    )
    
    if total_produksi != 0:
        responses['data']['persentase_produksi']['susu_segar'] = round(
            responses['data']['susu_segar']['produksi'] / total_produksi, 2
        )
        responses['data']['persentase_produksi']['susu_pasteurisasi'] = round(
            responses['data']['susu_pasteurisasi']['produksi'] / total_produksi, 2
        )
        responses['data']['persentase_produksi']['susu_kefir'] = round(
            responses['data']['susu_kefir']['produksi'] / total_produksi, 2
        )
        responses['data']['persentase_produksi']['yogurt'] = round(
            responses['data']['yogurt']['produksi'] / total_produksi, 2
        )
    else:
        responses['data']['persentase_produksi']['susu_segar'] = 0
        responses['data']['persentase_produksi']['susu_pasteurisasi'] = 0
        responses['data']['persentase_produksi']['susu_kefir'] = 0
        responses['data']['persentase_produksi']['yogurt'] = 0
        
    
    ### Get persentase distribusi data ###
    responses['data']['persentase_distribusi'] = {}
    
    total_distribusi = (
        responses['data']['susu_segar']['distribusi'] + \
        responses['data']['susu_pasteurisasi']['distribusi'] + \
        responses['data']['susu_kefir']['distribusi'] + \
        responses['data']['yogurt']['distribusi'] + \
        responses['data']['keju']['distribusi']
    )
    
    if total_distribusi != 0:
        responses['data']['persentase_distribusi']['susu_segar'] = round(
            responses['data']['susu_segar']['distribusi'] / total_distribusi, 2
        )
        responses['data']['persentase_distribusi']['susu_pasteurisasi'] = round(
            responses['data']['susu_pasteurisasi']['distribusi'] / total_distribusi, 2
        )
        responses['data']['persentase_distribusi']['susu_kefir'] = round(
            responses['data']['susu_kefir']['distribusi'] / total_distribusi, 2
        )
        responses['data']['persentase_distribusi']['yogurt'] = round(
            responses['data']['yogurt']['distribusi'] / total_distribusi, 2
        )
    else:
        responses['data']['persentase_distribusi']['susu_segar'] = 0
        responses['data']['persentase_distribusi']['susu_pasteurisasi'] = 0
        responses['data']['persentase_distribusi']['susu_kefir'] = 0
        responses['data']['persentase_distribusi']['yogurt'] = 0
    
    ### Get pro_dis_susu_segar data ###
    end_date = dt.date.today()
    # end_date = datetime.strptime("2023-01-07", "%Y-%m-%d")
    start_date = end_date - timedelta(days=7)

    all_dates = {
        (start_date + timedelta(days=x)).strftime("%Y-%m-%d"): 0
        for x in range((end_date - start_date).days + 1)
    }
    
    # Distribusi
    query = (
        db.query(DimWaktu.tanggal, 
                 func.sum(FactDistribusi.jumlah_distribusi))
        .where(and_(FactDistribusi.id_jenis_produk == 3,
                    DimWaktu.tanggal >= start_date,
                    DimWaktu.tanggal <= end_date))
        .join(DimWaktu, DimWaktu.id == FactDistribusi.id_waktu)
        .join(DimLokasi, DimLokasi.id == FactDistribusi.id_lokasi)
        .group_by(DimWaktu.tanggal)
        .order_by(DimWaktu.tanggal)
    )
    
    if provinsi:
        query = query.where(DimLokasi.provinsi == provinsi)
    if kabupaten_kota:
        query = query.where(DimLokasi.kabupaten_kota == kabupaten_kota)
        
    dis_susu_segar_list = query.all()
    
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
    query = (
        db.query(DimWaktu.tanggal,
                 func.sum(FactProduksi.jumlah_produksi))
        .where(and_(FactProduksi.id_jenis_produk == 3,
                    DimWaktu.tanggal >= start_date,
                    DimWaktu.tanggal <= end_date))
        .join(DimWaktu, DimWaktu.id == FactProduksi.id_waktu)
        .join(DimLokasi, DimLokasi.id == FactProduksi.id_lokasi)
        .group_by(DimWaktu.tanggal)
        .order_by(DimWaktu.tanggal)
    )
    
    if provinsi:
        query = query.where(DimLokasi.provinsi == provinsi)
    if kabupaten_kota:
        query = query.where(DimLokasi.kabupaten_kota == kabupaten_kota)
        
    pro_susu_segar_list = query.all()
    
    if len(pro_susu_segar_list) == 0:
        pro_susu_segar_dict = {}
    else:
        pro_susu_segar_dict = {
            pro_susu_segar_list[i][0].strftime("%Y-%m-%d"): pro_susu_segar_list[i][1]
            for i in range(len(pro_susu_segar_list))
        }
        
    pro_susu_segar_result = all_dates.copy()
    pro_susu_segar_result.update(pro_susu_segar_dict)
    
    responses['data']['prod_dis_susu_segar'] = []
    for date in all_dates.keys():
        responses['data']['prod_dis_susu_segar'].append({
            'lable': date,
            'produksi': pro_susu_segar_result[date],
            'distribusi': dis_susu_segar_result[date]
        })
    
        
    ### Get permintaan_susu_segar_dari_mitra_all data ###
    query = (
        db.query(DimMitraBisnis.nama_mitra_bisnis,
                 func.sum(FactDistribusi.jumlah_distribusi))
        .where(and_(FactDistribusi.id_jenis_produk == 3,
                    DimWaktu.tahun == tahun))
        .join(DimWaktu, DimWaktu.id == FactDistribusi.id_waktu)
        .join(DimLokasi, DimLokasi.id == FactDistribusi.id_lokasi)
        .join(DimMitraBisnis, DimMitraBisnis.id == FactDistribusi.id_mitra_bisnis)
        .group_by(DimMitraBisnis.nama_mitra_bisnis)
    )
    
    if provinsi:
        query = query.where(DimLokasi.provinsi == provinsi)
    if kabupaten_kota:
        query = query.where(DimLokasi.kabupaten_kota == kabupaten_kota)
        
    mitra_result_list = query.all()
    
    responses['data']['permintaan_susu_segar_dari_mitra_all'] = []
    for mitra_bisnis in mitra_result_list:
        responses['data']['permintaan_susu_segar_dari_mitra_all'].append({
            'label': mitra_bisnis[0],
            'value': mitra_bisnis[1]
        })
        
        
    ### Get total_persentase_distribusi data ###
    try:
        responses['data']['total_persentase_distribusi'] = round(
            (
                responses['data']['susu_segar']['distribusi'] + \
                responses['data']['susu_pasteurisasi']['distribusi'] + \
                responses['data']['susu_kefir']['distribusi'] + \
                responses['data']['yogurt']['distribusi'] + \
                responses['data']['keju']['distribusi']
            ) / (
                responses['data']['susu_segar']['produksi'] + \
                responses['data']['susu_pasteurisasi']['produksi'] + \
                responses['data']['susu_kefir']['produksi'] + \
                responses['data']['yogurt']['produksi'] + \
                responses['data']['keju']['produksi']
            ), 2
        ) * 100
    except:
        responses['data']['total_persentase_distribusi'] = 0
        
        
    ### Get total_pendapatan data ###
    query = (
        db.query(FactDistribusi.jumlah_distribusi, 
                 FactDistribusi.harga_rata_rata)
        .where(and_(FactDistribusi.id_jenis_produk == 3,
                    DimWaktu.tahun == tahun))
        .join(DimWaktu, DimWaktu.id == FactDistribusi.id_waktu)
        .join(DimLokasi, DimLokasi.id == FactDistribusi.id_lokasi)
    )
    
    if provinsi:
        query = query.where(DimLokasi.provinsi == provinsi)
    if kabupaten_kota:
        query = query.where(DimLokasi.kabupaten_kota == kabupaten_kota)
        
    distribusi_data_list = query.all()
    
    total_pendapatan = 0
    for distribusi_data in distribusi_data_list:
        total_pendapatan += distribusi_data[0] * distribusi_data[1]
        
    responses['data']['total_pendapatan'] = total_pendapatan
    
    
    ### Get harga_susu data ###
    responses['data']['harga_susu'] = {}
    
    # Minimum
    query = (
        db.query(func.min(FactDistribusi.harga_minimum))
        .where(and_(FactDistribusi.id_jenis_produk == 3,
                    DimWaktu.tahun == tahun))
        .join(DimWaktu, DimWaktu.id == FactDistribusi.id_waktu)
        .join(DimLokasi, DimLokasi.id == FactDistribusi.id_lokasi)
    )
    
    if provinsi:
        query = query.where(DimLokasi.provinsi == provinsi)
    if kabupaten_kota:
        query = query.where(DimLokasi.kabupaten_kota == kabupaten_kota)
        
    if query.scalar() is not None:
        responses['data']['harga_susu']['minimum'] = query.scalar()
    else:
        responses['data']['harga_susu']['minimum'] = 0
        
    # Maximum
    query = (
        db.query(func.max(FactDistribusi.harga_maximum))
        .where(and_(FactDistribusi.id_jenis_produk == 3,
                    DimWaktu.tahun == tahun))
        .join(DimWaktu, DimWaktu.id == FactDistribusi.id_waktu)
        .join(DimLokasi, DimLokasi.id == FactDistribusi.id_lokasi)
    )
    
    if provinsi:
        query = query.where(DimLokasi.provinsi == provinsi)
    if kabupaten_kota:
        query = query.where(DimLokasi.kabupaten_kota == kabupaten_kota)
        
    if query.scalar() is not None:
        responses['data']['harga_susu']['maximum'] = query.scalar()
    else:
        responses['data']['harga_susu']['maximum'] = 0
        
    # Rata-rata
    query = (
        db.query(func.avg(FactDistribusi.harga_rata_rata))
        .where(and_(FactDistribusi.id_jenis_produk == 3,
                    DimWaktu.tahun == tahun))
        .join(DimWaktu, DimWaktu.id == FactDistribusi.id_waktu)
        .join(DimLokasi, DimLokasi.id == FactDistribusi.id_lokasi)
    )
    
    if provinsi:
        query = query.where(DimLokasi.provinsi == provinsi)
    if kabupaten_kota:
        query = query.where(DimLokasi.kabupaten_kota == kabupaten_kota)
    
    harga_rataan = round(query.scalar(), 2)
    
    if harga_rataan is None:
        responses['data']['harga_susu']['rata_rata'] = 0
    else:
        responses['data']['harga_susu']['rata_rata'] = float(harga_rataan)
   
    
    
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=responses
    )
     