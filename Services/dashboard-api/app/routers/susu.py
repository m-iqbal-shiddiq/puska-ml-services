import calendar
import datetime as dt

from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, status, Query
from fastapi.responses import JSONResponse


from typing import Optional

from sqlalchemy import func, and_
from sqlalchemy.orm import Session

from app.database.connection import SessionLocal
from app.database.models import DimLokasi, DimWaktu, DimMitraBisnis, FactDistribusi, FactDistribusiStream, FactProduksi, FactProduksiStream, DimUnitPeternakan, PredSusu
from app.schemas.susu import SusuMasterData

from decimal import Decimal

router = APIRouter(redirect_slashes=False)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        

def filter_data(query, tahun:int, bulan: int, hari: str, provinsi: str, kabupaten_kota: str, unit_peternakan: str):
    if tahun:
        query = query.where(DimWaktu.tahun == tahun)
    if bulan:
        query = query.where(DimWaktu.bulan == bulan)
    if hari:
        query = query.where(DimWaktu.hari == hari)
    if provinsi:
        query = query.where(DimLokasi.provinsi == provinsi)
    if kabupaten_kota:
        query = query.where(DimLokasi.kabupaten_kota == kabupaten_kota)
    if unit_peternakan:
        query = query.where(DimUnitPeternakan.nama_unit == unit_peternakan)
    
    return query

def filter_series_data(query, provinsi: str, kabupaten_kota: str, unit_peternakan: str):
    if provinsi:
        query = query.where(DimLokasi.provinsi == provinsi)
    if kabupaten_kota:
        query = query.where(DimLokasi.kabupaten_kota == kabupaten_kota)
    if unit_peternakan:
        query = query.where(DimUnitPeternakan.nama_unit == unit_peternakan)
    
    return query
        

def get_produksi_data(db, id_jenis_produk: int, tahun: int, bulan: int, hari: int, provinsi: str, kabupaten_kota: str, unit_peternakan: str):
    sub_query = (
        db.query(DimWaktu.tahun,
                 DimWaktu.bulan,
                 DimWaktu.hari,
                 DimLokasi.provinsi,
                 DimUnitPeternakan.nama_unit,
                 FactProduksiStream.jumlah_produksi)
        .join(DimWaktu, DimWaktu.id == FactProduksiStream.id_waktu)
        .join(DimLokasi, DimLokasi.id == FactProduksiStream.id_lokasi)
        .join(DimUnitPeternakan, DimUnitPeternakan.id == FactProduksiStream.id_unit_peternakan)
        .where(FactProduksiStream.id_jenis_produk == id_jenis_produk)
    )
    
    sub_query = filter_data(sub_query, tahun, bulan, hari, provinsi, kabupaten_kota, unit_peternakan)
        
    sub_query = sub_query.subquery()    
    query = db.query(
        func.sum(sub_query.c.jumlah_produksi).label('total_produksi')
    )
    
    result = query.scalar()
    
    if result is None:
        sub_query = (
        db.query(DimWaktu.tahun,
                 DimWaktu.bulan,
                 DimWaktu.hari,
                 DimLokasi.provinsi,
                 DimUnitPeternakan.nama_unit,
                 FactProduksi.jumlah_produksi)
            .join(DimWaktu, DimWaktu.id == FactProduksi.id_waktu)
            .join(DimLokasi, DimLokasi.id == FactProduksi.id_lokasi)
            .join(DimUnitPeternakan, DimUnitPeternakan.id == FactProduksi.id_unit_peternakan)
            .where(FactProduksi.id_jenis_produk == id_jenis_produk)
        )
        
        sub_query = filter_data(sub_query, tahun, bulan, hari, provinsi, kabupaten_kota, unit_peternakan)
            
        sub_query = sub_query.subquery()    
        query = db.query(
            func.sum(sub_query.c.jumlah_produksi).label('total_produksi')
        )
    
        result = query.scalar()
        
    if result:
        return result
    else:
        return 0
    
def get_distribusi_data(db, id_jenis_produk: int, tahun: int, bulan: int, hari: int, provinsi: str, kabupaten_kota: str, unit_peternakan: str):
    sub_query = (
        db.query(DimWaktu.tahun,
                 DimWaktu.bulan,
                 DimWaktu.hari,
                 DimLokasi.provinsi,
                 DimUnitPeternakan.nama_unit,
                 FactDistribusiStream.jumlah_distribusi)
        .join(DimWaktu, DimWaktu.id == FactDistribusiStream.id_waktu)
        .join(DimLokasi, DimLokasi.id == FactDistribusiStream.id_lokasi)
        .join(DimUnitPeternakan, DimUnitPeternakan.id == FactDistribusiStream.id_unit_peternakan)
        .where(FactDistribusiStream.id_jenis_produk == id_jenis_produk)
    )
    
    sub_query = filter_data(sub_query, tahun, bulan, hari, provinsi, kabupaten_kota, unit_peternakan)
        
    sub_query = sub_query.subquery()    
    query = db.query(
        func.sum(sub_query.c.jumlah_distribusi).label('total_distribusi')
    )
    
    result = query.scalar()
    
    if result is None:
        sub_query = (
        db.query(DimWaktu.tahun,
                 DimWaktu.bulan,
                 DimWaktu.hari,
                 DimLokasi.provinsi,
                 DimUnitPeternakan.nama_unit,
                 FactDistribusi.jumlah_distribusi)
            .join(DimWaktu, DimWaktu.id == FactDistribusi.id_waktu)
            .join(DimLokasi, DimLokasi.id == FactDistribusi.id_lokasi)
            .join(DimUnitPeternakan, DimUnitPeternakan.id == FactDistribusi.id_unit_peternakan)
            .where(FactDistribusi.id_jenis_produk == id_jenis_produk)
        )
        
        sub_query = filter_data(sub_query, tahun, bulan, hari, provinsi, kabupaten_kota, unit_peternakan)
            
        sub_query = sub_query.subquery()    
        query = db.query(
            func.sum(sub_query.c.jumlah_distribusi).label('total_distribusi')
        )
    
        result = query.scalar()
    
    if result:
        return result
    else:
        return 0
 
def get_produksi_yearly(db, id_jenis_produk:int, provinsi: str, kabupaten_kota: str, unit_peternakan: str):
    current_year = datetime.today().year
    
    sub_query = (
        db.query(DimWaktu.tahun,
                 FactProduksiStream.jumlah_produksi)
        .join(DimWaktu, DimWaktu.id == FactProduksiStream.id_waktu)
        .join(DimLokasi, DimLokasi.id == FactProduksiStream.id_lokasi)
        .join(DimUnitPeternakan, DimUnitPeternakan.id == FactProduksiStream.id_unit_peternakan)
        .where(FactProduksiStream.id_jenis_produk == id_jenis_produk)
    )
    
    sub_query = filter_series_data(sub_query, provinsi, kabupaten_kota, unit_peternakan)
    sub_query = sub_query.subquery()
    
    query = (
        db.query(sub_query.c.tahun,
                 func.sum(sub_query.c.jumlah_produksi).label('total_produksi'))
        .group_by(sub_query.c.tahun)
        .order_by(sub_query.c.tahun)
    )
    
    data_dict = {item[0]: int(item[1]) for item in query.all()}
    all_years = {year[0] for year in db.query(DimWaktu.tahun).distinct().where(DimWaktu.tahun <= current_year).all()}
    not_found_years = all_years - set(data_dict.keys())
    
    if len(not_found_years) > 0:
        sub_query = (
            db.query(DimWaktu.tahun,
                     FactProduksi.jumlah_produksi)
            .join(DimWaktu, DimWaktu.id == FactProduksi.id_waktu)
            .join(DimLokasi, DimLokasi.id == FactProduksi.id_lokasi)
            .join(DimUnitPeternakan, DimUnitPeternakan.id == FactProduksi.id_unit_peternakan)
            .where(DimWaktu.tahun.in_(not_found_years))
            .where(FactProduksi.id_jenis_produk == id_jenis_produk)
        )
        
        sub_query = filter_series_data(sub_query, provinsi, kabupaten_kota, unit_peternakan)
        sub_query = sub_query.subquery()
        
        query = (
            db.query(sub_query.c.tahun,
                     func.sum(sub_query.c.jumlah_produksi).label('total_produksi'))
            .group_by(sub_query.c.tahun)
            .order_by(sub_query.c.tahun)
        )
        
        found_data_dict = {item[0]: int(item[1]) for item in query.all()}
        data_dict = {**data_dict, **found_data_dict}
        
    complete_data = {}
    for year in range(list(all_years)[0], current_year + 1):
        if year not in data_dict:
            complete_data[year] = 0
        else:
            complete_data[year] = data_dict[year]
    
    return complete_data

def get_distribusi_yearly(db, id_jenis_produk:int, provinsi: str, kabupaten_kota: str, unit_peternakan: str):
    current_year = datetime.today().year
    
    sub_query = (
        db.query(DimWaktu.tahun,
                 FactDistribusiStream.jumlah_distribusi)
        .join(DimWaktu, DimWaktu.id == FactDistribusiStream.id_waktu)
        .join(DimLokasi, DimLokasi.id == FactDistribusiStream.id_lokasi)
        .join(DimUnitPeternakan, DimUnitPeternakan.id == FactDistribusiStream.id_unit_peternakan)
        .where(FactDistribusiStream.id_jenis_produk == id_jenis_produk)
    )
    
    sub_query = filter_series_data(sub_query, provinsi, kabupaten_kota, unit_peternakan)
    sub_query = sub_query.subquery()
    
    query = (
        db.query(sub_query.c.tahun,
                 func.sum(sub_query.c.jumlah_distribusi).label('total_distribusi'))
        .group_by(sub_query.c.tahun)
        .order_by(sub_query.c.tahun)
    )
    
    data_dict = {item[0]: int(item[1]) for item in query.all()}
    all_years = {year[0] for year in db.query(DimWaktu.tahun).distinct().where(DimWaktu.tahun <= current_year).all()}
    not_found_years = all_years - set(data_dict.keys())
    
    if len(not_found_years) > 0:
        sub_query = (
            db.query(DimWaktu.tahun,
                     FactDistribusi.jumlah_distribusi)
            .join(DimWaktu, DimWaktu.id == FactDistribusi.id_waktu)
            .join(DimLokasi, DimLokasi.id == FactDistribusi.id_lokasi)
            .join(DimUnitPeternakan, DimUnitPeternakan.id == FactDistribusi.id_unit_peternakan)
            .where(DimWaktu.tahun.in_(not_found_years))
            .where(FactDistribusi.id_jenis_produk == id_jenis_produk)
        )
        
        sub_query = filter_series_data(sub_query, provinsi, kabupaten_kota, unit_peternakan)
        sub_query = sub_query.subquery()
        
        query = (
            db.query(sub_query.c.tahun,
                     func.sum(sub_query.c.jumlah_distribusi).label('total_distribusi'))
            .group_by(sub_query.c.tahun)
            .order_by(sub_query.c.tahun)
        )
        
        found_data_dict = {item[0]: int(item[1]) for item in query.all()}
        data_dict = {**data_dict, **found_data_dict}
        
    complete_data = {}
    for year in range(list(all_years)[0], current_year + 1):
        if year not in data_dict:
            complete_data[year] = 0
        else:
            complete_data[year] = data_dict[year]
            
    return complete_data

def get_produksi_monthly(db, id_jenis_produk:int, tahun: int, provinsi: str, kabupaten_kota: str, unit_peternakan: str):
    current_year = datetime.today().year
    if tahun == current_year:
        current_month = datetime.today().month
    else:
        current_month = 12
        
    sub_query = (
        db.query(DimWaktu.bulan,
                 FactProduksiStream.jumlah_produksi)
        .join(DimWaktu, DimWaktu.id == FactProduksiStream.id_waktu)
        .join(DimLokasi, DimLokasi.id == FactProduksiStream.id_lokasi)
        .join(DimUnitPeternakan, DimUnitPeternakan.id == FactProduksiStream.id_unit_peternakan)
        .where(DimWaktu.tahun == tahun)
        .where(FactProduksiStream.id_jenis_produk == id_jenis_produk)
    )
    
    sub_query = filter_series_data(sub_query, provinsi, kabupaten_kota, unit_peternakan)
    sub_query = sub_query.subquery()
    
    query = (
        db.query(sub_query.c.bulan,
                 func.sum(sub_query.c.jumlah_produksi).label('total_produksi'))
        .group_by(sub_query.c.bulan)
        .order_by(sub_query.c.bulan)
    )
    
    data_dict = {item[0]: int(item[1]) for item in query.all()}
    all_months = {month for month in range(1, current_month + 1)}
    not_found_months = all_months - set(data_dict.keys())
    
    if len(not_found_months) > 0:
        sub_query = (
            db.query(DimWaktu.bulan,
                     FactProduksi.jumlah_produksi)
            .join(DimWaktu, DimWaktu.id == FactProduksi.id_waktu)
            .join(DimLokasi, DimLokasi.id == FactProduksi.id_lokasi)
            .join(DimUnitPeternakan, DimUnitPeternakan.id == FactProduksi.id_unit_peternakan)
            .where(DimWaktu.tahun == tahun)
            .where(DimWaktu.bulan.in_(not_found_months))
            .where(FactProduksi.id_jenis_produk == id_jenis_produk)
        )
        
        sub_query = filter_series_data(sub_query, provinsi, kabupaten_kota, unit_peternakan)
        sub_query = sub_query.subquery()
        
        query = (
            db.query(sub_query.c.bulan,
                     func.sum(sub_query.c.jumlah_produksi).label('total_produksi'))
            .group_by(sub_query.c.bulan)
            .order_by(sub_query.c.bulan)
        )
        
        found_data_dict = {item[0]: int(item[1]) for item in query.all()}
        data_dict = {**data_dict, **found_data_dict}
    
    complete_data = {}  
    for i in range(1, current_month + 1):
        if i not in data_dict:
            complete_data[i] = 0
        else:
            complete_data[i] = data_dict[i]
            
    return complete_data

def get_distribusi_monthly(db, id_jenis_produk:int, tahun: int, provinsi: str, kabupaten_kota: str, unit_peternakan: str):
    current_year = datetime.today().year
    if tahun == current_year:
        current_month = datetime.today().month
    else:
        current_month = 12
        
    sub_query = (
        db.query(DimWaktu.bulan,
                 FactDistribusiStream.jumlah_distribusi)
        .join(DimWaktu, DimWaktu.id == FactDistribusiStream.id_waktu)
        .join(DimLokasi, DimLokasi.id == FactDistribusiStream.id_lokasi)
        .join(DimUnitPeternakan, DimUnitPeternakan.id == FactDistribusiStream.id_unit_peternakan)
        .where(DimWaktu.tahun == tahun)
        .where(FactDistribusiStream.id_jenis_produk == id_jenis_produk)
    )
    
    sub_query = filter_series_data(sub_query, provinsi, kabupaten_kota, unit_peternakan)
    sub_query = sub_query.subquery()
    
    query = (
        db.query(sub_query.c.bulan,
                 func.sum(sub_query.c.jumlah_distribusi).label('total_distribusi'))
        .group_by(sub_query.c.bulan)
        .order_by(sub_query.c.bulan)
    )
    
    data_dict = {item[0]: int(item[1]) for item in query.all()}
    all_months = {month for month in range(1, current_month + 1)}
    not_found_months = all_months - set(data_dict.keys())
    
    if len(not_found_months) > 0:
        sub_query = (
            db.query(DimWaktu.bulan,
                     FactDistribusi.jumlah_distribusi)
            .join(DimWaktu, DimWaktu.id == FactDistribusi.id_waktu)
            .join(DimLokasi, DimLokasi.id == FactDistribusi.id_lokasi)
            .join(DimUnitPeternakan, DimUnitPeternakan.id == FactDistribusi.id_unit_peternakan)
            .where(DimWaktu.tahun == tahun)
            .where(DimWaktu.bulan.in_(not_found_months))
            .where(FactDistribusi.id_jenis_produk == id_jenis_produk)
        )
        
        sub_query = filter_series_data(sub_query, provinsi, kabupaten_kota, unit_peternakan)
        sub_query = sub_query.subquery()
        
        query = (
            db.query(sub_query.c.bulan,
                     func.sum(sub_query.c.jumlah_distribusi).label('total_distribusi'))
            .group_by(sub_query.c.bulan)
            .order_by(sub_query.c.bulan)
        )
        
        found_data_dict = {item[0]: int(item[1]) for item in query.all()}
        data_dict = {**data_dict, **found_data_dict}
        
    complete_data = {}
    for i in range(1, current_month + 1):
        if i not in data_dict:
            complete_data[i] = 0
        else:
            complete_data[i] = data_dict[i]
            
    return complete_data

def get_produksi_daily(db, id_jenis_produk:int, tahun: int, bulan: int, provinsi: str, kabupaten_kota: str, unit_peternakan: str):
    if tahun == datetime.today().year:
        if bulan == datetime.today().month:
            last_day = datetime.today().day
        else:
            last_day = calendar.monthrange(tahun, bulan)[1]
    else:
        last_day = calendar.monthrange(tahun, bulan)[1]
    
    all_dates = [datetime(tahun, bulan, day) for day in range(1, last_day + 1)]
    
    sub_query = (
        db.query(DimWaktu.tanggal,
                 FactProduksiStream.jumlah_produksi)
        .join(DimWaktu, DimWaktu.id == FactProduksiStream.id_waktu)
        .join(DimLokasi, DimLokasi.id == FactProduksiStream.id_lokasi)
        .join(DimUnitPeternakan, DimUnitPeternakan.id == FactProduksiStream.id_unit_peternakan)
        .where(DimWaktu.tanggal.in_(all_dates))
        .where(FactProduksiStream.id_jenis_produk == id_jenis_produk)
    )
    
    sub_query = filter_series_data(sub_query, provinsi, kabupaten_kota, unit_peternakan)
    sub_query = sub_query.subquery()
    
    query = (
        db.query(sub_query.c.tanggal,
                 func.sum(sub_query.c.jumlah_produksi).label('total_produksi'))
        .group_by(sub_query.c.tanggal)
        .order_by(sub_query.c.tanggal)
    )
    
    data_dict = {item[0].strftime('%d-%m-%Y'): int(item[1]) for item in query.all()}
    all_dates = {(datetime(tahun, bulan, day)).strftime('%d-%m-%Y') for day in range(1, last_day + 1)}
    not_found_dates = all_dates - set(data_dict.keys())
    not_found_dates = [datetime.strptime(date, '%d-%m-%Y') for date in not_found_dates]
    
    if len(not_found_dates) > 0:
        sub_query = (
            db.query(DimWaktu.tanggal,
                     FactProduksi.jumlah_produksi)
            .join(DimWaktu, DimWaktu.id == FactProduksi.id_waktu)
            .join(DimLokasi, DimLokasi.id == FactProduksi.id_lokasi)
            .join(DimUnitPeternakan, DimUnitPeternakan.id == FactProduksi.id_unit_peternakan)
            .where(DimWaktu.tanggal.in_(not_found_dates))
            .where(FactProduksi.id_jenis_produk == id_jenis_produk)
        )
        
        sub_query = filter_series_data(sub_query, provinsi, kabupaten_kota, unit_peternakan)
        sub_query = sub_query.subquery()
        
        query = (
            db.query(sub_query.c.tanggal,
                     func.sum(sub_query.c.jumlah_produksi).label('total_produksi'))
            .group_by(sub_query.c.tanggal)
            .order_by(sub_query.c.tanggal)
        )
        
        found_data_dict = {item[0].strftime('%d-%m-%Y'): int(item[1]) for item in query.all()}
        data_dict = {**data_dict, **found_data_dict}
        
    complete_data = {date: data_dict.get(date, 0) for date in all_dates}
    sorted_data = sorted(complete_data.items(), key=lambda x: datetime.strptime(x[0], '%d-%m-%Y'))
    sorted_data_dict = dict(sorted_data)

    return sorted_data_dict

def get_distribusi_daily(db, id_jenis_produk:int, tahun: int, bulan: int, provinsi: str, kabupaten_kota: str, unit_peternakan: str):
    if tahun == datetime.today().year:
        if bulan == datetime.today().month:
            last_day = datetime.today().day
        else:
            last_day = calendar.monthrange(tahun, bulan)[1]
    else:
        last_day = calendar.monthrange(tahun, bulan)[1]
    
    all_dates = [datetime(tahun, bulan, day) for day in range(1, last_day + 1)]
    
    sub_query = (
        db.query(DimWaktu.tanggal,
                 FactDistribusiStream.jumlah_distribusi)
        .join(DimWaktu, DimWaktu.id == FactDistribusiStream.id_waktu)
        .join(DimLokasi, DimLokasi.id == FactDistribusiStream.id_lokasi)
        .join(DimUnitPeternakan, DimUnitPeternakan.id == FactDistribusiStream.id_unit_peternakan)
        .where(DimWaktu.tanggal.in_(all_dates))
        .where(FactDistribusiStream.id_jenis_produk == id_jenis_produk)
    )
    
    sub_query = filter_series_data(sub_query, provinsi, kabupaten_kota, unit_peternakan)
    sub_query = sub_query.subquery()
    
    query = (
        db.query(sub_query.c.tanggal,
                 func.sum(sub_query.c.jumlah_distribusi).label('total_distribusi'))
        .group_by(sub_query.c.tanggal)
        .order_by(sub_query.c.tanggal)
    )
    
    data_dict = {item[0].strftime('%d-%m-%Y'): int(item[1]) for item in query.all()}
    all_dates = {(datetime(tahun, bulan, day)).strftime('%d-%m-%Y') for day in range(1, last_day + 1)}
    not_found_dates = all_dates - set(data_dict.keys())
    not_found_dates = [datetime.strptime(date, '%d-%m-%Y') for date in not_found_dates]
    
    if len(not_found_dates) > 0:
        sub_query = (
            db.query(DimWaktu.tanggal,
                     FactDistribusi.jumlah_distribusi)
            .join(DimWaktu, DimWaktu.id == FactDistribusi.id_waktu)
            .join(DimLokasi, DimLokasi.id == FactDistribusi.id_lokasi)
            .join(DimUnitPeternakan, DimUnitPeternakan.id == FactDistribusi.id_unit_peternakan)
            .where(DimWaktu.tanggal.in_(not_found_dates))
            .where(FactDistribusi.id_jenis_produk == id_jenis_produk)
        )
        
        sub_query = filter_series_data(sub_query, provinsi, kabupaten_kota, unit_peternakan)
        sub_query = sub_query.subquery()
        
        query = (
            db.query(sub_query.c.tanggal,
                     func.sum(sub_query.c.jumlah_distribusi).label('total_distribusi'))
            .group_by(sub_query.c.tanggal)
            .order_by(sub_query.c.tanggal)
        )
        
        found_data_dict = {item[0].strftime('%d-%m-%Y'): int(item[1]) for item in query.all()}
        data_dict = {**data_dict, **found_data_dict}
        
    complete_data = {date: data_dict.get(date, 0) for date in all_dates}
    sorted_data = sorted(complete_data.items(), key=lambda x: datetime.strptime(x[0], '%d-%m-%Y'))
    sorted_data_dict = dict(sorted_data)
    
    return sorted_data_dict 

def get_permintaan_susu_segar_dari_mitra(db, id_jenis_produk:int, tahun: int, bulan: int, hari: int, provinsi: str, kabupaten_kota: str, unit_peternakan: str):
    sub_query = (
        db.query(DimMitraBisnis.nama_mitra_bisnis,
                 FactDistribusiStream.jumlah_distribusi)
        .join(DimWaktu, DimWaktu.id == FactDistribusiStream.id_waktu)
        .join(DimLokasi, DimLokasi.id == FactDistribusiStream.id_lokasi)
        .join(DimUnitPeternakan, DimUnitPeternakan.id == FactDistribusiStream.id_unit_peternakan)
        .join(DimMitraBisnis, DimMitraBisnis.id == FactDistribusiStream.id_mitra_bisnis)
        .where(FactDistribusiStream.id_jenis_produk == id_jenis_produk)
    )
   
    sub_query = filter_data(sub_query, tahun, bulan, hari, provinsi, kabupaten_kota, unit_peternakan)
    sub_query = sub_query.subquery()
    
    query = (
        db.query(sub_query.c.nama_mitra_bisnis,
                 func.sum(sub_query.c.jumlah_distribusi).label('total_distribusi'))
        .group_by(sub_query.c.nama_mitra_bisnis)
        .order_by(func.sum(sub_query.c.jumlah_distribusi).desc())
    )
    
    data_dict = {item[0]: round(item[1], 2) for item in query.all()}
    
    mitra_bisnis_all = db.query(DimMitraBisnis.nama_mitra_bisnis).all()
    mitra_bisnis_all = [item[0] for item in mitra_bisnis_all]
    
    not_found_mitra_bisnis = set(mitra_bisnis_all) - set(data_dict.keys())

    if len(not_found_mitra_bisnis) > 0:
        sub_query = (
            db.query(DimMitraBisnis.nama_mitra_bisnis,
                     FactDistribusi.jumlah_distribusi)
            .join(DimWaktu, DimWaktu.id == FactDistribusi.id_waktu)
            .join(DimLokasi, DimLokasi.id == FactDistribusi.id_lokasi)
            .join(DimUnitPeternakan, DimUnitPeternakan.id == FactDistribusi.id_unit_peternakan)
            .join(DimMitraBisnis, DimMitraBisnis.id == FactDistribusi.id_mitra_bisnis)
            .where(DimMitraBisnis.nama_mitra_bisnis.in_(not_found_mitra_bisnis))
            .where(FactDistribusi.id_jenis_produk == id_jenis_produk)
        )

        sub_query = filter_data(sub_query, tahun, bulan, hari, provinsi, kabupaten_kota, unit_peternakan)
        sub_query = sub_query.subquery()
        
        query = (
            db.query(sub_query.c.nama_mitra_bisnis,
                     func.sum(sub_query.c.jumlah_distribusi).label('total_distribusi'))
            .group_by(sub_query.c.nama_mitra_bisnis)
            .order_by(func.sum(sub_query.c.jumlah_distribusi).desc())
        )
        
        found_data_dict = {item[0]: round(item[1], 2) for item in query.all()}
        data_dict = {**data_dict, **found_data_dict}
    
    return data_dict

def get_total_pendapatan(db, id_jenis_produk: int, tahun: int, bulan: int, hari: int, provinsi: str, kabupaten_kota: str, unit_peternakan: str):
    
    query = (
        db.query(FactDistribusiStream.jumlah_distribusi, 
                 FactDistribusiStream.harga_rata_rata)
        .join(DimWaktu, DimWaktu.id == FactDistribusiStream.id_waktu)
        .join(DimLokasi, DimLokasi.id == FactDistribusiStream.id_lokasi)
        .join(DimUnitPeternakan, DimUnitPeternakan.id == FactDistribusiStream.id_unit_peternakan)
        .where(FactDistribusiStream.id_jenis_produk == id_jenis_produk)
    )
    
    query = filter_data(query, tahun, bulan, hari, provinsi, kabupaten_kota, unit_peternakan)
        
    data_list = query.all()
    
    if len(data_list) == 0:
        query = (
            db.query(FactDistribusi.jumlah_distribusi, 
                     FactDistribusi.harga_rata_rata)
            .join(DimWaktu, DimWaktu.id == FactDistribusi.id_waktu)
            .join(DimLokasi, DimLokasi.id == FactDistribusi.id_lokasi)
            .join(DimUnitPeternakan, DimUnitPeternakan.id == FactDistribusi.id_unit_peternakan)
            .where(FactDistribusi.id_jenis_produk == id_jenis_produk)
        )
        
        query = filter_data(query, tahun, bulan, hari, provinsi, kabupaten_kota, unit_peternakan)
    
    total_pendapatan = 0
    for data in data_list:
        total_pendapatan += data[0] * data[1]
        
    return total_pendapatan
    
def get_harga_minimum(db, id_jenis_produk: int, tahun: int, bulan: int, hari: int, provinsi: str, kabupaten_kota: str, unit_peternakan: str):
    sub_query = (
        db.query(FactDistribusiStream.harga_minimum)
        .join(DimWaktu, DimWaktu.id == FactDistribusiStream.id_waktu)
        .join(DimLokasi, DimLokasi.id == FactDistribusiStream.id_lokasi)
        .join(DimUnitPeternakan, DimUnitPeternakan.id == FactDistribusiStream.id_unit_peternakan)
        .where(FactDistribusiStream.id_jenis_produk == id_jenis_produk)
    )
    
    sub_query = filter_data(sub_query, tahun, bulan, hari, provinsi, kabupaten_kota, unit_peternakan)    
    sub_query = sub_query.subquery()
    
    query = (
        db.query(func.min(sub_query.c.harga_minimum).label('harga_minimum'))
    )
    
    result = query.scalar()
    
    if result is None:
        sub_query = (
            db.query(FactDistribusi.harga_minimum)
            .join(DimWaktu, DimWaktu.id == FactDistribusi.id_waktu)
            .join(DimLokasi, DimLokasi.id == FactDistribusi.id_lokasi)
            .join(DimUnitPeternakan, DimUnitPeternakan.id == FactDistribusi.id_unit_peternakan)
            .where(FactDistribusi.id_jenis_produk == id_jenis_produk)
        )
        
        sub_query = filter_data(sub_query, tahun, bulan, hari, provinsi, kabupaten_kota, unit_peternakan)
        sub_query = sub_query.subquery()
        
        query = (
            db.query(func.min(sub_query.c.harga_minimum).label('harga_minimum'))
        )
    
        result = query.scalar()
    
    if result:
        return result
    else:
        return 0

def get_harga_maximum(db, id_jenis_produk: int, tahun: int, bulan: int, hari: int, provinsi: str, kabupaten_kota: str, unit_peternakan: str):
    sub_query = (
        db.query(FactDistribusiStream.harga_maximum)
        .join(DimWaktu, DimWaktu.id == FactDistribusiStream.id_waktu)
        .join(DimLokasi, DimLokasi.id == FactDistribusiStream.id_lokasi)
        .join(DimUnitPeternakan, DimUnitPeternakan.id == FactDistribusiStream.id_unit_peternakan)
        .where(FactDistribusiStream.id_jenis_produk == id_jenis_produk)
    )
    
    sub_query = filter_data(sub_query, tahun, bulan, hari, provinsi, kabupaten_kota, unit_peternakan)
    sub_query = sub_query.subquery()
    
    query = (
        db.query(func.max(sub_query.c.harga_maximum).label('harga_maximum'))
    )
    
    result = query.scalar()
    
    if result is None:
        sub_query = (
            db.query(FactDistribusi.harga_maximum)
            .join(DimWaktu, DimWaktu.id == FactDistribusi.id_waktu)
            .join(DimLokasi, DimLokasi.id == FactDistribusi.id_lokasi)
            .join(DimUnitPeternakan, DimUnitPeternakan.id == FactDistribusi.id_unit_peternakan)
            .where(FactDistribusi.id_jenis_produk == id_jenis_produk)
        )
        
        sub_query = filter_data(sub_query, tahun, bulan, hari, provinsi, kabupaten_kota, unit_peternakan)   
        sub_query = sub_query.subquery()
        
        query = (
            db.query(func.max(sub_query.c.harga_maximum).label('harga_maximum'))
        )
    
        result = query.scalar()
    
    if result:
        return result
    else:
        return 0

def get_harga_rata_rata(db, id_jenis_produk: int, tahun: int, bulan: int, hari: int, provinsi: str, kabupaten_kota: str, unit_peternakan: str):
    sub_query = (
        db.query(FactDistribusiStream.harga_rata_rata)
        .join(DimWaktu, DimWaktu.id == FactDistribusiStream.id_waktu)
        .join(DimLokasi, DimLokasi.id == FactDistribusiStream.id_lokasi)
        .join(DimUnitPeternakan, DimUnitPeternakan.id == FactDistribusiStream.id_unit_peternakan)
        .where(FactDistribusiStream.id_jenis_produk == id_jenis_produk)
    )
    
    sub_query = filter_data(sub_query, tahun, bulan, hari, provinsi, kabupaten_kota, unit_peternakan)      
    sub_query = sub_query.subquery()
    
    query = (
        db.query(func.avg(sub_query.c.harga_rata_rata).label('harga_rata_rata'))
    )
    
    result = query.scalar()
    
    if result is None:
        sub_query = (
            db.query(FactDistribusi.harga_rata_rata)
            .join(DimWaktu, DimWaktu.id == FactDistribusi.id_waktu)
            .join(DimLokasi, DimLokasi.id == FactDistribusi.id_lokasi)
            .join(DimUnitPeternakan, DimUnitPeternakan.id == FactDistribusi.id_unit_peternakan)
            .where(FactDistribusi.id_jenis_produk == id_jenis_produk)
        )
        
        sub_query = filter_data(sub_query, tahun, bulan, hari, provinsi, kabupaten_kota, unit_peternakan)
        sub_query = sub_query.subquery()
        
        query = (
            db.query(func.avg(sub_query.c.harga_rata_rata).label('harga_rata_rata'))
        )
    
        result = query.scalar()
    
    if result:
        return round(result, 2)
    else:
        return 0

def get_prediksi_data(db, provinsi, kabupaten_kota, unit_peternakan, days=30):
    start_date = datetime.today() - timedelta(days=days)
    # start_date = datetime.strptime("2023-01-01", "%Y-%m-%d")
    end_date = datetime.today() + timedelta(days=1)
    # end_date = start_date + timedelta(days=days)
    
    sub_query_produksi = (
        db.query(DimWaktu.tanggal,
                 DimLokasi.provinsi,
                 DimUnitPeternakan.nama_unit,
                 FactProduksi.jumlah_produksi)
        .join(DimWaktu, DimWaktu.id == FactProduksi.id_waktu)
        .join(DimLokasi, DimLokasi.id == FactProduksi.id_lokasi)
        .join(DimUnitPeternakan, DimUnitPeternakan.id == FactProduksi.id_unit_peternakan)
        .where(DimWaktu.tanggal >= start_date)
        .where(DimWaktu.tanggal < end_date)
    )
    
    sub_query_prediksi = filter_series_data(sub_query_produksi, provinsi, kabupaten_kota, unit_peternakan)
    sub_query_produksi = sub_query_produksi.subquery()
    
    query = (
        db.query(sub_query_produksi.c.tanggal,
                 func.sum(sub_query_produksi.c.jumlah_produksi).label('total_produksi'))
        .group_by(sub_query_produksi.c.tanggal)
        .order_by(sub_query_produksi.c.tanggal)
    )
    
    produksi_dict = {item[0].strftime('%d-%m-%Y'): int(item[1]) for item in query.all()}
    all_dates = {(start_date + timedelta(days=i)).strftime('%d-%m-%Y') for i in range((end_date - start_date).days)}
    produksi_complete_data = {date: produksi_dict.get(date, 0) for date in all_dates}
    produksi_complete_data[end_date.strftime('%d-%m-%Y')] = None
    produksi_sorted_data = sorted(produksi_complete_data.items(), key=lambda x: datetime.strptime(x[0], '%d-%m-%Y'))
    produksi_result_dict = dict(produksi_sorted_data)
    
    sub_query_prediksi = (
        db.query(DimWaktu.tanggal,
                 DimLokasi.provinsi,
                 DimUnitPeternakan.nama_unit,
                 PredSusu.prediction)
        .join(DimWaktu, DimWaktu.id == PredSusu.id_waktu)
        .join(DimLokasi, DimLokasi.id == PredSusu.id_lokasi)
        .join(DimUnitPeternakan, DimUnitPeternakan.id == PredSusu.id_unit_peternakan)
        .where(DimWaktu.tanggal >= start_date)
        .where(DimWaktu.tanggal <= end_date)
    )
    
    sub_query_prediksi = filter_series_data(sub_query_prediksi, provinsi, kabupaten_kota, unit_peternakan)
    sub_query_prediksi = sub_query_prediksi.subquery()
    
    query = (
        db.query(sub_query_prediksi.c.tanggal,
                 sub_query_prediksi.c.prediction)
        .order_by(sub_query_prediksi.c.tanggal)
    )
    
    prediksi_dict = {item[0].strftime('%d-%m-%Y'): int(item[1]) for item in query.all()}
    all_dates = {(start_date + timedelta(days=i)).strftime('%d-%m-%Y') for i in range((end_date - start_date).days + 1)}
    prediksi_complete_data = {date: prediksi_dict.get(date, 0) for date in all_dates}
    prediksi_sorted_data = sorted(prediksi_complete_data.items(), key=lambda x: datetime.strptime(x[0], '%d-%m-%Y'))
    prediksi_result_dict = dict(prediksi_sorted_data)
    
    data_result = []
    for key in produksi_result_dict.keys():
        data_result.append({
            'label': key,
            'actual': produksi_result_dict[key],
            'predict': prediksi_result_dict[key]
        })
        
    return data_result  
    
def convert_decimals(obj):
    if isinstance(obj, dict):
        return {k: convert_decimals(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_decimals(i) for i in obj]
    elif isinstance(obj, Decimal):
        return float(obj)
    else:
        return obj


@router.get(path='/susu',
            response_model=SusuMasterData, 
            status_code=status.HTTP_200_OK)
async def get_susu_data(db: Session = Depends(get_db),
                        tahun: Optional[int] = Query(None),
                        bulan: Optional[int] = Query(None),
                        hari: Optional[int] = Query(None),
                        provinsi: Optional[str] = Query(None),
                        kabupaten_kota: Optional[str] = Query(None),
                        unit_peternakan: Optional[str] = Query(None)):
    
    try:
        responses = {}
        
        # Susu Segar
        responses['susu_segar'] = {}
        responses['susu_segar']['produksi'] = get_produksi_data(db=db, id_jenis_produk=3, tahun=tahun, bulan=bulan, hari=hari, provinsi=provinsi, kabupaten_kota=kabupaten_kota, unit_peternakan=unit_peternakan)
        responses['susu_segar']['distribusi'] = get_distribusi_data(db=db, id_jenis_produk=3, tahun=tahun, bulan=bulan, hari=hari, provinsi=provinsi, kabupaten_kota=kabupaten_kota, unit_peternakan=unit_peternakan)

        # Susu Pasteurisasi
        responses['susu_pasteurisasi'] = {}
        responses['susu_pasteurisasi']['produksi'] = get_produksi_data(db=db, id_jenis_produk=4, tahun=tahun, bulan=bulan, hari=hari, provinsi=provinsi, kabupaten_kota=kabupaten_kota, unit_peternakan=unit_peternakan)
        responses['susu_pasteurisasi']['distribusi'] = get_distribusi_data(db=db, id_jenis_produk=4, tahun=tahun, bulan=bulan, hari=hari, provinsi=provinsi, kabupaten_kota=kabupaten_kota, unit_peternakan=unit_peternakan)
        
        # Susu Kefir
        responses['susu_kefir'] = {}
        responses['susu_kefir']['produksi'] = get_produksi_data(db=db, id_jenis_produk=5, tahun=tahun, bulan=bulan, hari=hari, provinsi=provinsi, kabupaten_kota=kabupaten_kota, unit_peternakan=unit_peternakan)
        responses['susu_kefir']['distribusi'] = get_distribusi_data(db=db, id_jenis_produk=5, tahun=tahun, bulan=bulan, hari=hari, provinsi=provinsi, kabupaten_kota=kabupaten_kota, unit_peternakan=unit_peternakan)
        
        # Yogurt
        responses['yogurt'] = {}
        responses['yogurt']['produksi'] = get_produksi_data(db=db,id_jenis_produk=6, tahun=tahun, bulan=bulan, hari=hari, provinsi=provinsi, kabupaten_kota=kabupaten_kota, unit_peternakan=unit_peternakan)
        responses['yogurt']['distribusi'] = get_distribusi_data(db=db, id_jenis_produk=6, tahun=tahun, bulan=bulan, hari=hari, provinsi=provinsi, kabupaten_kota=kabupaten_kota, unit_peternakan=unit_peternakan)
        
        # Keju
        responses['keju'] = {}
        responses['keju']['produksi'] = get_produksi_data(db=db, id_jenis_produk=7, tahun=tahun, bulan=bulan, hari=hari, provinsi=provinsi, kabupaten_kota=kabupaten_kota, unit_peternakan=unit_peternakan)
        responses['keju']['distribusi'] = get_distribusi_data(db=db, id_jenis_produk=7, tahun=tahun, bulan=bulan, hari=hari, provinsi=provinsi, kabupaten_kota=kabupaten_kota, unit_peternakan=unit_peternakan)
        
        # Prediksi
        responses['prediksi'] = get_prediksi_data(db, provinsi, kabupaten_kota, unit_peternakan)
        
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
        responses['prod_dis_susu_segar'] = []
        
        if tahun:
            if bulan:
                produksi = get_produksi_daily(db, id_jenis_produk=3, tahun=tahun, bulan=bulan, provinsi=provinsi, kabupaten_kota=kabupaten_kota, unit_peternakan=unit_peternakan)
                distribusi = get_distribusi_daily(db, id_jenis_produk=3, tahun=tahun, bulan=bulan, provinsi=provinsi, kabupaten_kota=kabupaten_kota, unit_peternakan=unit_peternakan)
            else:
                produksi = get_produksi_monthly(db, id_jenis_produk=3, tahun=tahun, provinsi=provinsi, kabupaten_kota=kabupaten_kota, unit_peternakan=unit_peternakan)
                distribusi = get_distribusi_monthly(db, id_jenis_produk=3, tahun=tahun, provinsi=provinsi, kabupaten_kota=kabupaten_kota, unit_peternakan=unit_peternakan)
        else:
            produksi = get_produksi_yearly(db, id_jenis_produk=3, provinsi=provinsi, kabupaten_kota=kabupaten_kota, unit_peternakan=unit_peternakan)
            distribusi = get_distribusi_yearly(db, id_jenis_produk=3, provinsi=provinsi, kabupaten_kota=kabupaten_kota, unit_peternakan=unit_peternakan)        

        for key in produksi.keys():
            responses['prod_dis_susu_segar'].append({
                'label': str(key),
                'produksi': produksi[key],
                'distribusi': distribusi[key]
            })
        
        # Permintaan Susu Segar dari Mitra Bisnis
        responses['permintaan_susu_segar_dari_mitra_all'] = []
        
        mitra_bisnis = get_permintaan_susu_segar_dari_mitra(db=db, id_jenis_produk=3, tahun=tahun, bulan=bulan, hari=hari, provinsi=provinsi, kabupaten_kota=kabupaten_kota, unit_peternakan=unit_peternakan)
        
        for key in mitra_bisnis:
            responses['permintaan_susu_segar_dari_mitra_all'].append({
                'label': str(key),
                'value': mitra_bisnis[key]
            })
        
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
        responses['total_pendapatan'] = get_total_pendapatan(db=db, id_jenis_produk=3, tahun=tahun, bulan=bulan, hari=hari, provinsi=provinsi, kabupaten_kota=kabupaten_kota, unit_peternakan=unit_peternakan)
        
        # Harga Minimum
        responses['harga_susu'] = {}
        responses['harga_susu']['minimum'] = get_harga_minimum(db=db, id_jenis_produk=3, tahun=tahun, bulan=bulan, hari=hari, provinsi=provinsi, kabupaten_kota=kabupaten_kota, unit_peternakan=unit_peternakan)
        responses['harga_susu']['maximum'] = get_harga_maximum(db=db, id_jenis_produk=3, tahun=tahun, bulan=bulan, hari=hari, provinsi=provinsi, kabupaten_kota=kabupaten_kota, unit_peternakan=unit_peternakan)
        responses['harga_susu']['rata_rata'] = get_harga_rata_rata(db=db, id_jenis_produk=3, tahun=tahun, bulan=bulan, hari=hari, provinsi=provinsi, kabupaten_kota=kabupaten_kota, unit_peternakan=unit_peternakan)
        
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


