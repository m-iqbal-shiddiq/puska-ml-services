import datetime as dt

from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from sqlalchemy import func, and_
from sqlalchemy.orm import Session

from app.database.connection import SessionLocal
from app.database.models import DimLokasi, DimWaktu, DimMitraBisnis, FactDistribusi, FactProduksi, DimUnitPeternakan
from app.schemas.susu import SusuMasterData

from decimal import Decimal

router = APIRouter(redirect_slashes=False)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        

def get_produksi_data(db, id_jenis_produk: int, tahun: int, provinsi: str, unit_peternakan: str):
    prod_subquery = (
        db.query(DimWaktu.tahun,
                 DimLokasi.provinsi,
                 DimUnitPeternakan.nama_unit,
                 FactProduksi.jumlah_produksi)
        .join(DimWaktu, DimWaktu.id == FactProduksi.id_waktu)
        .join(DimLokasi, DimLokasi.id == FactProduksi.id_lokasi)
        .join(DimUnitPeternakan, DimUnitPeternakan.id == FactProduksi.id_unit_peternakan)
        .where(FactProduksi.id_jenis_produk == id_jenis_produk)
    )
    
    if tahun:
        prod_subquery = prod_subquery.where(DimWaktu.tahun == tahun)
    if provinsi:
        prod_subquery = prod_subquery.where(DimLokasi.provinsi == provinsi)
    if unit_peternakan:
        prod_subquery = prod_subquery.where(DimUnitPeternakan.nama_unit == unit_peternakan)
        
    prod_subquery = prod_subquery.subquery()    
    query = db.query(
        func.sum(prod_subquery.c.jumlah_produksi).label('total_produksi')
    )
    
    return query.scalar()

def get_distribusi_data(db, id_jenis_produk: int, tahun: int, provinsi: str, unit_peternakan: str):
    dis_subquery = (
        db.query(DimWaktu.tahun,
                 DimLokasi.provinsi,
                 DimUnitPeternakan.nama_unit,
                 FactDistribusi.jumlah_distribusi)
        .join(DimWaktu, DimWaktu.id == FactDistribusi.id_waktu)
        .join(DimLokasi, DimLokasi.id == FactDistribusi.id_lokasi)
        .join(DimUnitPeternakan, DimUnitPeternakan.id == FactDistribusi.id_unit_peternakan)
        .where(FactDistribusi.id_jenis_produk == id_jenis_produk)
    )
    
    if tahun:
        dis_subquery = dis_subquery.where(DimWaktu.tahun == tahun)
    if provinsi:
        dis_subquery = dis_subquery.where(DimLokasi.provinsi == provinsi)
    if unit_peternakan:
        dis_subquery = dis_subquery.where(DimUnitPeternakan.nama_unit == unit_peternakan)
        
    dis_subquery = dis_subquery.subquery()    
    query = db.query(
        func.sum(dis_subquery.c.jumlah_distribusi).label('total_distribusi')
    )
    
    return query.scalar()
 
def get_produksi_series_by_interval(db, id_jenis_produk:int, provinsi: str, unit_peternakan: str, days=365):
    start_date = datetime.today() - timedelta(days=days)
    end_date = datetime.today()
    
    sub_query = (
        db.query(DimWaktu.tanggal,
                 FactProduksi.jumlah_produksi)
        .join(DimWaktu, DimWaktu.id == FactProduksi.id_waktu)
        .join(DimLokasi, DimLokasi.id == FactProduksi.id_lokasi)
        .join(DimUnitPeternakan, DimUnitPeternakan.id == FactProduksi.id_unit_peternakan)
        .where(DimWaktu.tanggal >= start_date)
        .where(FactProduksi.id_jenis_produk == id_jenis_produk)
    )
    
    if provinsi:
        sub_query = sub_query.where(DimLokasi.provinsi == provinsi)
    if unit_peternakan:
        sub_query = sub_query.where(DimUnitPeternakan.nama_unit == unit_peternakan)
        
    sub_query = sub_query.subquery()
    
    query = (
        db.query(sub_query.c.tanggal,
                 func.sum(sub_query.c.jumlah_produksi).label('total_produksi'))
        .group_by(sub_query.c.tanggal)
        .order_by(sub_query.c.tanggal)
    )
    
    data_dict = {item[0].strftime('%d-%m-%Y'): int(item[1]) for item in query.all()}
    all_dates = {(start_date + timedelta(days=i)).strftime('%d-%m-%Y') for i in range((end_date - start_date).days)}
    complete_data = {date: data_dict.get(date, 0) for date in all_dates}
    sorted_data = sorted(complete_data.items(), key=lambda x: datetime.strptime(x[0], '%d-%m-%Y'))
    sorted_data_dict = dict(sorted_data)
    
    return sorted_data_dict

def get_produksi_series_by_year(db, id_jenis_produk:int, tahun: int, provinsi: str, unit_peternakan: str):
    start_date = dt.datetime(tahun, 1, 1)
    end_date = dt.datetime(tahun, 12, 31)
    
    sub_query = (
        db.query(DimWaktu.tanggal,
                 FactProduksi.jumlah_produksi)
        .join(DimWaktu, DimWaktu.id == FactProduksi.id_waktu)
        .join(DimLokasi, DimLokasi.id == FactProduksi.id_lokasi)
        .join(DimUnitPeternakan, DimUnitPeternakan.id == FactProduksi.id_unit_peternakan)
        .where(DimWaktu.tahun == tahun)
        .where(FactProduksi.id_jenis_produk == id_jenis_produk)
    )
    
    if provinsi:
        sub_query = sub_query.where(DimLokasi.provinsi == provinsi)
    if unit_peternakan:
        sub_query = sub_query.where(DimUnitPeternakan.nama_unit == unit_peternakan)
        
    sub_query = sub_query.subquery()
    
    query = (
        db.query(sub_query.c.tanggal,
                 func.sum(sub_query.c.jumlah_produksi).label('total_distribusi'))
        .group_by(sub_query.c.tanggal)
        .order_by(sub_query.c.tanggal)
    )
    
    data_dict = {item[0].strftime('%d-%m-%Y'): int(item[1]) for item in query.all()}
    all_dates = {(start_date + timedelta(days=i)).strftime('%d-%m-%Y') for i in range((end_date - start_date).days + 1)}
    complete_data = {date: data_dict.get(date, 0) for date in all_dates}
    sorted_data = sorted(complete_data.items(), key=lambda x: datetime.strptime(x[0], '%d-%m-%Y'))
    sorted_data_dict = dict(sorted_data)
    
    return sorted_data_dict
    
def get_distribusi_series_by_interval(db, id_jenis_produk:int, provinsi: str, unit_peternakan: str, days=365):
    start_date = datetime.today() - timedelta(days=days)
    end_date = datetime.today()
    
    sub_query = (
        db.query(DimWaktu.tanggal,
                 FactDistribusi.jumlah_distribusi)
        .join(DimWaktu, DimWaktu.id == FactDistribusi.id_waktu)
        .join(DimLokasi, DimLokasi.id == FactDistribusi.id_lokasi)
        .join(DimUnitPeternakan, DimUnitPeternakan.id == FactDistribusi.id_unit_peternakan)
        .where(DimWaktu.tanggal >= start_date)
        .where(FactDistribusi.id_jenis_produk == id_jenis_produk)
    )
    
    if provinsi:
        sub_query = sub_query.where(DimLokasi.provinsi == provinsi)
    if unit_peternakan:
        sub_query = sub_query.where(DimUnitPeternakan.nama_unit == unit_peternakan)
        
    sub_query = sub_query.subquery()
    
    query = (
        db.query(sub_query.c.tanggal,
                 func.sum(sub_query.c.jumlah_distribusi).label('total_distribusi'))
        .group_by(sub_query.c.tanggal)
        .order_by(sub_query.c.tanggal)
    )
    
    data_dict = {item[0].strftime('%d-%m-%Y'): int(item[1]) for item in query.all()}
    all_dates = {(start_date + timedelta(days=i)).strftime('%d-%m-%Y') for i in range((end_date - start_date).days)}
    complete_data = {date: data_dict.get(date, 0) for date in all_dates}
    sorted_data = sorted(complete_data.items(), key=lambda x: datetime.strptime(x[0], '%d-%m-%Y'))
    sorted_data_dict = dict(sorted_data)
    
    return sorted_data_dict

def get_distribusi_series_by_year(db, id_jenis_produk:int, tahun: int, provinsi: str, unit_peternakan: str):
    start_date = dt.datetime(tahun, 1, 1)
    end_date = dt.datetime(tahun, 12, 31)
    
    sub_query = (
        db.query(DimWaktu.tanggal,
                 FactDistribusi.jumlah_distribusi)
        .join(DimWaktu, DimWaktu.id == FactDistribusi.id_waktu)
        .join(DimLokasi, DimLokasi.id == FactDistribusi.id_lokasi)
        .join(DimUnitPeternakan, DimUnitPeternakan.id == FactDistribusi.id_unit_peternakan)
        .where(DimWaktu.tahun == tahun)
        .where(FactDistribusi.id_jenis_produk == id_jenis_produk)
    )
    
    if provinsi:
        sub_query = sub_query.where(DimLokasi.provinsi == provinsi)
    if unit_peternakan:
        sub_query = sub_query.where(DimUnitPeternakan.nama_unit == unit_peternakan)
        
    sub_query = sub_query.subquery()
    
    query = (
        db.query(sub_query.c.tanggal,
                 func.sum(sub_query.c.jumlah_distribusi).label('total_distribusi'))
        .group_by(sub_query.c.tanggal)
        .order_by(sub_query.c.tanggal)
    )
    
    data_dict = {item[0].strftime('%d-%m-%Y'): int(item[1]) for item in query.all()}
    all_dates = {(start_date + timedelta(days=i)).strftime('%d-%m-%Y') for i in range((end_date - start_date).days + 1)}
    complete_data = {date: data_dict.get(date, 0) for date in all_dates}
    sorted_data = sorted(complete_data.items(), key=lambda x: datetime.strptime(x[0], '%d-%m-%Y'))
    sorted_data_dict = dict(sorted_data)
    
    return sorted_data_dict

def get_permintaan_susu_segar_dari_mitra(db, id_jenis_produk:int, tahun: int, provinsi: str, unit_peternakan: str):
    sub_query = (
        db.query(DimMitraBisnis.nama_mitra_bisnis,
                 FactDistribusi.jumlah_distribusi)
        .join(DimWaktu, DimWaktu.id == FactDistribusi.id_waktu)
        .join(DimLokasi, DimLokasi.id == FactDistribusi.id_lokasi)
        .join(DimUnitPeternakan, DimUnitPeternakan.id == FactDistribusi.id_unit_peternakan)
        .join(DimMitraBisnis, DimMitraBisnis.id == FactDistribusi.id_mitra_bisnis)
        .where(FactDistribusi.id_jenis_produk == id_jenis_produk)
    )
   
    if tahun:
        sub_query = sub_query.where(DimWaktu.tahun == tahun)
    if provinsi:
        sub_query = sub_query.where(DimLokasi.provinsi == provinsi)
    if unit_peternakan:
        sub_query = sub_query.where(DimUnitPeternakan.nama_unit == unit_peternakan)
    
    sub_query = sub_query.subquery()
    
    query = (
        db.query(sub_query.c.nama_mitra_bisnis,
                 func.sum(sub_query.c.jumlah_distribusi).label('total_distribusi'))
        .group_by(sub_query.c.nama_mitra_bisnis)
        .order_by(func.sum(sub_query.c.jumlah_distribusi).desc())
    )
    
    data_dict = {item[0]: round(item[1], 2) for item in query.all()}
    
    return data_dict

def get_total_pendapatan(db, id_jenis_produk, tahun, provinsi, unit_peternakan):
    
    query = (
        db.query(FactDistribusi.jumlah_distribusi, 
                 FactDistribusi.harga_rata_rata)
        .join(DimWaktu, DimWaktu.id == FactDistribusi.id_waktu)
        .join(DimLokasi, DimLokasi.id == FactDistribusi.id_lokasi)
        .join(DimUnitPeternakan, DimUnitPeternakan.id == FactDistribusi.id_unit_peternakan)
        .where(FactDistribusi.id_jenis_produk == id_jenis_produk)
    )
    
    if tahun:
        query = query.where(DimWaktu.tahun == tahun)
    if provinsi:
        query = query.where(DimLokasi.provinsi == provinsi)
    if unit_peternakan:
        query = query.where(DimUnitPeternakan.nama_unit == unit_peternakan)
        
    data_list = query.all()
    
    total_pendapatan = 0
    for data in data_list:
        total_pendapatan += data[0] * data[1]
        
    return total_pendapatan
    
def get_harga_minimum(db, id_jenis_produk, tahun, provinsi, unit_peternakan):
    sub_query = (
        db.query(FactDistribusi.harga_minimum)
        .join(DimWaktu, DimWaktu.id == FactDistribusi.id_waktu)
        .join(DimLokasi, DimLokasi.id == FactDistribusi.id_lokasi)
        .join(DimUnitPeternakan, DimUnitPeternakan.id == FactDistribusi.id_unit_peternakan)
        .where(FactDistribusi.id_jenis_produk == id_jenis_produk)
    )
    
    if tahun:
        sub_query = sub_query.where(DimWaktu.tahun == tahun)
    if provinsi:
        sub_query = sub_query.where(DimLokasi.provinsi == provinsi)
    if unit_peternakan:
        sub_query = sub_query.where(DimUnitPeternakan.nama_unit == unit_peternakan)
        
    sub_query = sub_query.subquery()
    
    query = (
        db.query(func.min(sub_query.c.harga_minimum).label('harga_minimum'))
    )
    
    return query.scalar()

def get_harga_maximum(db, id_jenis_produk, tahun, provinsi, unit_peternakan):
    sub_query = (
        db.query(FactDistribusi.harga_maximum)
        .join(DimWaktu, DimWaktu.id == FactDistribusi.id_waktu)
        .join(DimLokasi, DimLokasi.id == FactDistribusi.id_lokasi)
        .join(DimUnitPeternakan, DimUnitPeternakan.id == FactDistribusi.id_unit_peternakan)
        .where(FactDistribusi.id_jenis_produk == id_jenis_produk)
    )
    
    if tahun:
        sub_query = sub_query.where(DimWaktu.tahun == tahun)
    if provinsi:
        sub_query = sub_query.where(DimLokasi.provinsi == provinsi)
    if unit_peternakan:
        sub_query = sub_query.where(DimUnitPeternakan.nama_unit == unit_peternakan)
        
    sub_query = sub_query.subquery()
    
    query = (
        db.query(func.max(sub_query.c.harga_maximum).label('harga_maximum'))
    )
    
    return query.scalar()

def get_harga_rata_rata(db, id_jenis_produk, tahun, provinsi, unit_peternakan):
    sub_query = (
        db.query(FactDistribusi.harga_rata_rata)
        .join(DimWaktu, DimWaktu.id == FactDistribusi.id_waktu)
        .join(DimLokasi, DimLokasi.id == FactDistribusi.id_lokasi)
        .join(DimUnitPeternakan, DimUnitPeternakan.id == FactDistribusi.id_unit_peternakan)
        .where(FactDistribusi.id_jenis_produk == id_jenis_produk)
    )
    
    if tahun:
        sub_query = sub_query.where(DimWaktu.tahun == tahun)
    if provinsi:
        sub_query = sub_query.where(DimLokasi.provinsi == provinsi)
    if unit_peternakan:
        sub_query = sub_query.where(DimUnitPeternakan.nama_unit == unit_peternakan)
        
    sub_query = sub_query.subquery()
    
    query = (
        db.query(func.avg(sub_query.c.harga_rata_rata).label('harga_rata_rata'))
    )
    
    if query.scalar():
        return round(query.scalar(), 2)
    else:
        return None

def convert_decimals(obj):
    if isinstance(obj, dict):
        return {k: convert_decimals(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_decimals(i) for i in obj]
    elif isinstance(obj, Decimal):
        return float(obj)
    else:
        return obj


@router.get(path='/susu')
async def get_susu_data(db: Session = Depends(get_db),
                        tahun: int | None = None,
                        provinsi: str | None = None,
                        unit_peternakan: str | None = None):
    
    try:
        responses = {}
        
        # Prediksi
        responses['prediksi'] = [{}]
        
        # Susu Segar
        responses['susu_segar'] = {}
        responses['susu_segar']['produksi'] = get_produksi_data(db, 3, tahun, provinsi, unit_peternakan)
        responses['susu_segar']['distribusi'] = get_distribusi_data(db, 3, tahun, provinsi, unit_peternakan)
        
        # Susu Pasteurisasi
        responses['susu_pasteurisasi'] = {}
        responses['susu_pasteurisasi']['produksi'] = get_produksi_data(db, 4, tahun, provinsi, unit_peternakan)
        responses['susu_pasteurisasi']['distribusi'] = get_distribusi_data(db, 4, tahun, provinsi, unit_peternakan)
        
        # Susu Kefir
        responses['susu_kefir'] = {}
        responses['susu_kefir']['produksi'] = get_produksi_data(db, 5, tahun, provinsi, unit_peternakan)
        responses['susu_kefir']['distribusi'] = get_distribusi_data(db, 5, tahun, provinsi, unit_peternakan)
        
        # Yogurt
        responses['yogurt'] = {}
        responses['yogurt']['produksi'] = get_produksi_data(db, 6, tahun, provinsi, unit_peternakan)
        responses['yogurt']['distribusi'] = get_distribusi_data(db, 6, tahun, provinsi, unit_peternakan)
        
        # Keju
        responses['keju'] = {}
        responses['keju']['produksi'] = get_produksi_data(db, 7, tahun, provinsi, unit_peternakan)
        responses['keju']['distribusi'] = get_distribusi_data(db, 7, tahun, provinsi, unit_peternakan)
        
        # Persentase Produksi
        total_produksi = (
            (responses['susu_segar']['produksi'] or 0) + \
            (responses['susu_pasteurisasi']['produksi'] or 0)+ \
            (responses['susu_kefir']['produksi'] or 0) + \
            (responses['yogurt']['produksi'] or 0)
        )
        
        responses['persentase_produksi'] = {}
        
        if total_produksi == 0:
            responses['persentase_produksi']['susu_segar'] = 0
            responses['persentase_produksi']['susu_pasteurisasi'] = 0
            responses['persentase_produksi']['susu_kefir'] = 0
            responses['persentase_produksi']['yogurt'] = 0
        else:
            responses['persentase_produksi']['susu_segar'] = round((responses['susu_segar']['produksi'] or 0) / total_produksi, 2)
            responses['persentase_produksi']['susu_pasteurisasi'] = round((responses['susu_pasteurisasi']['produksi'] or 0) / total_produksi, 2)
            responses['persentase_produksi']['susu_kefir'] = round((responses['susu_kefir']['produksi'] or 0) / total_produksi, 2)
            responses['persentase_produksi']['yogurt'] = round((responses['yogurt']['produksi'] or 0) / total_produksi, 2)
        
        # Persentase Distribusi
        total_distribusi = (
            (responses['susu_segar']['distribusi'] or 0) + \
            (responses['susu_pasteurisasi']['distribusi'] or 0) + \
            (responses['susu_kefir']['distribusi'] or 0) + \
            (responses['yogurt']['distribusi'] or 0)
        )
        
        responses['persentase_distribusi'] = {}
        
        if total_distribusi == 0:
            responses['persentase_distribusi']['susu_segar'] = 0
            responses['persentase_distribusi']['susu_pasteurisasi'] = 0
            responses['persentase_distribusi']['susu_kefir'] = 0
            responses['persentase_distribusi']['yogurt'] = 0
        else:
            responses['persentase_distribusi']['susu_segar'] = round((responses['susu_segar']['distribusi'] or 0)/ total_distribusi, 2)
            responses['persentase_distribusi']['susu_pasteurisasi'] = round((responses['susu_pasteurisasi']['distribusi'] or 0)/ total_distribusi, 2)
            responses['persentase_distribusi']['susu_kefir'] = round((responses['susu_kefir']['distribusi'] or 0) / total_distribusi, 2)
            responses['persentase_distribusi']['yogurt'] = round((responses['yogurt']['distribusi'] or 0) / total_distribusi, 2)
            
        # Produksi dan Distribusi Susu Segar
        responses['prod_dis_susu_segar'] = {}
        
        if tahun:
            produksi = get_produksi_series_by_year(db, 3, tahun, provinsi, unit_peternakan)
            distribusi = get_distribusi_series_by_year(db, 3, tahun, provinsi, unit_peternakan)

            responses['prod_dis_susu_segar']['label'] = list(produksi.keys())
            responses['prod_dis_susu_segar']['produksi'] = list(produksi.values())
            responses['prod_dis_susu_segar']['distribusi'] = list(distribusi.values())
        else:
            produksi = get_produksi_series_by_interval(db, 3, provinsi, unit_peternakan)
            distribusi = get_distribusi_series_by_interval(db, 3, provinsi, unit_peternakan)
            
            responses['prod_dis_susu_segar']['label'] = list(produksi.keys())
            responses['prod_dis_susu_segar']['produksi'] = list(produksi.values())
            responses['prod_dis_susu_segar']['distribusi'] = list(distribusi.values())
        
        # Permintaan Susu Segar dari Mitra Bisnis
        responses['permintaan_susu_segar_dari_mitra_all'] = {}
        
        mitra_bisnis = get_permintaan_susu_segar_dari_mitra(db, 3, tahun, provinsi, unit_peternakan)
        
        responses['permintaan_susu_segar_dari_mitra_all']['label'] = list(mitra_bisnis.keys())
        responses['permintaan_susu_segar_dari_mitra_all']['value'] = list(mitra_bisnis.values())
        
        # Total Persentase Distribusi
        try:
            responses['total_persentase_distribusi'] = round(
                (
                    (responses['susu_segar']['distribusi'] or 0) + \
                    (responses['susu_pasteurisasi']['distribusi'] or 0) + \
                    (responses['susu_kefir']['distribusi'] or 0) + \
                    (responses['yogurt']['distribusi'] or 0)
                ) / (
                    (responses['susu_segar']['produksi'] or 0) + \
                    (responses['susu_pasteurisasi']['produksi'] or 0) + \
                    (responses['susu_kefir']['produksi'] or 0) + \
                    (responses['yogurt']['produksi'] or 0)
                ), 2
            )
        except:
            responses['total_persentase_distribusi'] = 0
        
        # Total Pendapatan
        responses['total_pendapatan'] = get_total_pendapatan(db, 3, tahun, provinsi, unit_peternakan)
        
        # Harga Minimum
        responses['harga_susu'] = {}
        responses['harga_susu']['minimum'] = get_harga_minimum(db, 3, tahun, provinsi, unit_peternakan)
        responses['harga_susu']['maximum'] = get_harga_maximum(db, 3, tahun, provinsi, unit_peternakan)
        responses['harga_susu']['rata_rata'] = get_harga_rata_rata(db, 3, tahun, provinsi, unit_peternakan)
        
        # return responses
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=convert_decimals(responses)
        )
    
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": str(e)}
    )


