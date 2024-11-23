import sys
import json
import datetime as dt

from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from sqlalchemy import func, and_, text
from sqlalchemy.orm import Session

from app.database.connection import SessionLocal
from app.database.models import DimLokasi, DimWaktu, FactDistribusi, FactDistribusiStream, FactProduksi, FactProduksiStream, FactPopulasi, FactPopulasiStream
from app.schemas.ternak import TernakMasterData

from decimal import Decimal

router = APIRouter(redirect_slashes=False)

def get_db(): 
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_produksi_data(db, id_jenis_produk):
    
    query = (
        db.query(func.sum(FactProduksiStream.jumlah_produksi))
        .where(FactProduksiStream.id_jenis_produk == id_jenis_produk)
    )
    
    result = query.scalar()
    
    if result is None:
        query = (
            db.query(func.sum(FactProduksi.jumlah_produksi))
            .where(FactProduksi.id_jenis_produk == id_jenis_produk)
        )
        
        result = query.scalar()
    
    if result:
        return result
    else:
        return 0

def get_distribusi_data(db, id_jenis_produk):
    
    query = (
        db.query(func.sum(FactDistribusiStream.jumlah_distribusi))
        .where(FactDistribusiStream.id_jenis_produk == id_jenis_produk)
    )
    
    result = query.scalar()
    
    if result is None:
        query = (
            db.query(func.sum(FactDistribusi.jumlah_distribusi))
            .where(FactDistribusi.id_jenis_produk == id_jenis_produk)
        )
        
        result = query.scalar()
    
    if result:
        return result
    else:
        return 0

def get_produksi_series_by_interval(db, id_jenis_produk:int, days=365):
    start_date = datetime.today() - timedelta(days=days)
    end_date = datetime.today()
    
    sub_query = (
        db.query(DimWaktu.tanggal,
                 FactProduksiStream.jumlah_produksi)
        .join(DimWaktu, DimWaktu.id == FactProduksiStream.id_waktu)
        .where(DimWaktu.tanggal >= start_date)
        .where(FactProduksiStream.id_jenis_produk == id_jenis_produk)
    )
    
    sub_query = sub_query.subquery()
    
    query = (
        db.query(sub_query.c.tanggal,
                 func.sum(sub_query.c.jumlah_produksi).label('total_produksi'))
        .group_by(sub_query.c.tanggal)
        .order_by(sub_query.c.tanggal)
    )
    
    data_dict = {item[0].strftime('%d-%m-%Y'): float(item[1]) for item in query.all()}
    all_dates = {(start_date + timedelta(days=i)).strftime('%d-%m-%Y') for i in range((end_date - start_date).days)}
    
    not_found_dates = all_dates - set(data_dict.keys())
    not_found_dates = sorted(list(not_found_dates), key=lambda x: datetime.strptime(x, '%d-%m-%Y'))
    not_found_dates = [datetime.strptime(date, '%d-%m-%Y').date() for date in not_found_dates]
    
    if len(not_found_dates) > 0:
        sub_query = (
            db.query(DimWaktu.tanggal,
                    FactProduksi.jumlah_produksi)
            .join(DimWaktu, DimWaktu.id == FactProduksi.id_waktu)
            .where(DimWaktu.tanggal.in_(not_found_dates))
            .where(FactProduksi.id_jenis_produk == id_jenis_produk)
        )
        
        sub_query = sub_query.subquery()
    
        query = (
            db.query(sub_query.c.tanggal,
                    func.sum(sub_query.c.jumlah_produksi).label('total_distribusi'))
            .group_by(sub_query.c.tanggal)
            .order_by(sub_query.c.tanggal)
        )
        
        found_data_dict = {item[0].strftime('%d-%m-%Y'): float(item[1]) for item in query.all()}
        data_dict = {**data_dict, **found_data_dict}
        
    complete_data = {date: data_dict.get(date, 0) for date in all_dates}
    sorted_data = sorted(complete_data.items(), key=lambda x: datetime.strptime(x[0], '%d-%m-%Y'))
    sorted_data_dict = dict(sorted_data)
    
    return sorted_data_dict
        
def get_distribusi_series_by_interval(db, id_jenis_produk:int, days=365):
    start_date = datetime.today() - timedelta(days=days)
    end_date = datetime.today()
    
    sub_query = (
        db.query(DimWaktu.tanggal,
                 FactDistribusiStream.jumlah_distribusi)
        .join(DimWaktu, DimWaktu.id == FactDistribusiStream.id_waktu)
        .where(DimWaktu.tanggal >= start_date)
        .where(FactDistribusiStream.id_jenis_produk == id_jenis_produk)
    )
    
    sub_query = sub_query.subquery()
    
    query = (
        db.query(sub_query.c.tanggal,
                 func.sum(sub_query.c.jumlah_distribusi).label('total_distribusi'))
        .group_by(sub_query.c.tanggal)
        .order_by(sub_query.c.tanggal)
    )
    
    data_dict = {item[0].strftime('%d-%m-%Y'): float(item[1]) for item in query.all()}
    all_dates = {(start_date + timedelta(days=i)).strftime('%d-%m-%Y') for i in range((end_date - start_date).days)}
    
    not_found_dates = all_dates - set(data_dict.keys())
    not_found_dates = sorted(list(not_found_dates), key=lambda x: datetime.strptime(x, '%d-%m-%Y'))
    not_found_dates = [datetime.strptime(date, '%d-%m-%Y').date() for date in not_found_dates]
    
    if len(not_found_dates) > 0:
        sub_query = (
            db.query(DimWaktu.tanggal,
                    FactDistribusi.jumlah_distribusi)
            .join(DimWaktu, DimWaktu.id == FactDistribusi.id_waktu)
            .where(DimWaktu.tanggal.in_(not_found_dates))
            .where(FactDistribusi.id_jenis_produk == id_jenis_produk)
        )
        
        sub_query = sub_query.subquery()
    
        query = (
            db.query(sub_query.c.tanggal,
                    func.sum(sub_query.c.jumlah_distribusi).label('total_distribusi'))
            .group_by(sub_query.c.tanggal)
            .order_by(sub_query.c.tanggal)
        )
        
        found_data_dict = {item[0].strftime('%d-%m-%Y'): float(item[1]) for item in query.all()}
        data_dict = {**data_dict, **found_data_dict}
        
    complete_data = {date: data_dict.get(date, 0) for date in all_dates}
    sorted_data = sorted(complete_data.items(), key=lambda x: datetime.strptime(x[0], '%d-%m-%Y'))
    sorted_data_dict = dict(sorted_data)
    
    return sorted_data_dict
    
def get_sebaran_populasi_all(db, tahun:int=None, provinsi:str=None, kabupaten_kota:str=None, perah_pedaging:str=None, jantan_betina:str=None, dewasa_anakan:str=None):
    sub_query = (
        db.query(DimWaktu.tahun,
                 DimLokasi.provinsi,
                 DimLokasi.kabupaten_kota,
                 DimLokasi.kecamatan,
                 FactPopulasiStream.tipe_ternak,
                 FactPopulasiStream.jenis_kelamin,
                 FactPopulasiStream.tipe_usia,
                 FactPopulasiStream.jumlah)
        .join(DimWaktu, DimWaktu.id == FactPopulasiStream.id_waktu)
        .join(DimLokasi, DimLokasi.id == FactPopulasiStream.id_lokasi)
    )
    
    if tahun:
        sub_query = sub_query.where(DimWaktu.tahun == tahun)
    else:
        sub_query = sub_query.where(DimWaktu.tahun > 2022)
    if provinsi:
        sub_query = sub_query.where(DimLokasi.provinsi == provinsi)
    if kabupaten_kota:
        sub_query = sub_query.where(DimLokasi.kabupaten_kota == kabupaten_kota)
    if perah_pedaging:
        sub_query = sub_query.where(FactPopulasiStream.tipe_ternak == perah_pedaging)
    if jantan_betina:
        sub_query = sub_query.where(FactPopulasiStream.jenis_kelamin == jantan_betina)
    if dewasa_anakan:
        sub_query = sub_query.where(FactPopulasiStream.tipe_usia == dewasa_anakan)
        
    sub_query = sub_query.subquery()
    
    if provinsi:
        if kabupaten_kota:
            query = (
                db.query(sub_query.c.kecamatan,
                         func.sum(sub_query.c.jumlah).label('total_populasi'))
                .group_by(sub_query.c.kecamatan)
            )
            
            query_str = text(
                """
                    SELECT ST_AsText(region_simp)
                    FROM dim_lokasi
                    WHERE
                        provinsi = :provinsi AND
                        kabupaten_kota = :kabupaten_kota AND
                        kecamatan = :kecamatan
                """
            )
            
            locations = (
                db.query(DimLokasi.kecamatan)
                .where(DimLokasi.provinsi == provinsi)
                .where(DimLokasi.kabupaten_kota == kabupaten_kota)
                .distinct()
            ).all()
            
        else:
            query = (
                db.query(sub_query.c.kabupaten_kota,
                         func.sum(sub_query.c.jumlah).label('total_populasi'))
                .group_by(sub_query.c.kabupaten_kota)
            )
            
            query_str = text(
                """
                    SELECT ST_AsText(region_simp)
                    FROM dim_lokasi
                    WHERE
                        provinsi = :provinsi AND
                        kabupaten_kota = :kabupaten_kota AND
                        kecamatan IS NULL
                """
            )
            
            locations = (
                db.query(DimLokasi.kabupaten_kota)
                .where(DimLokasi.provinsi == provinsi)
                .distinct()
            ).all()
            
    else:
        query = (
            db.query(sub_query.c.provinsi,
                     func.sum(sub_query.c.jumlah).label('total_populasi'))
            .group_by(sub_query.c.provinsi)
        )
        
        query_str = text(
            """
                SELECT ST_AsText(region_simp)
                FROM dim_lokasi
                WHERE
                    provinsi = :provinsi AND
                    kabupaten_kota IS NULL AND
                    kecamatan IS NULL
            """
        )
        
        locations = (
            db.query(DimLokasi.provinsi)
            .distinct()
        ).all()
        
    data_dict = {item[0]: int(item[1]) for item in query.all()}
    locations = [item[0] for item in locations if item[0] is not None]
    
    not_found_locations = set(locations) - set(data_dict.keys())

    if len(not_found_locations) > 0:
        sub_query = (
            db.query(DimWaktu.tahun,
                    DimLokasi.provinsi,
                    DimLokasi.kabupaten_kota,
                    DimLokasi.kecamatan,
                    FactPopulasi.tipe_ternak,
                    FactPopulasi.jenis_kelamin,
                    FactPopulasi.tipe_usia,
                    FactPopulasi.jumlah)
            .join(DimWaktu, DimWaktu.id == FactPopulasi.id_waktu)
            .join(DimLokasi, DimLokasi.id == FactPopulasi.id_lokasi)
        )
        
        if tahun:
            sub_query = sub_query.where(DimWaktu.tahun == tahun)
        if provinsi:
            sub_query = sub_query.where(DimLokasi.provinsi == provinsi)
        if kabupaten_kota:
            sub_query = sub_query.where(DimLokasi.kabupaten_kota == kabupaten_kota)
        if perah_pedaging:
            sub_query = sub_query.where(FactPopulasi.tipe_ternak == perah_pedaging)
        if jantan_betina:
            sub_query = sub_query.where(FactPopulasi.jenis_kelamin == jantan_betina)
        if dewasa_anakan:
            sub_query = sub_query.where(FactPopulasi.tipe_usia == dewasa_anakan)
            
        sub_query = sub_query.subquery()
        
        if provinsi:
            if kabupaten_kota:
                query = (
                    db.query(sub_query.c.kecamatan,
                             func.sum(sub_query.c.jumlah).label('total_populasi'))
                    .where(sub_query.c.kecamatan.in_(not_found_locations))
                    .group_by(sub_query.c.kecamatan)
                )
            else:
                query = (
                    db.query(sub_query.c.kabupaten_kota,
                             func.sum(sub_query.c.jumlah).label('total_populasi'))
                    .where(sub_query.c.kabupaten_kota.in_(not_found_locations))
                    .group_by(sub_query.c.kabupaten_kota)
                )
        else:
            query = (
                db.query(sub_query.c.provinsi,
                         func.sum(sub_query.c.jumlah).label('total_populasi'))
                .where(sub_query.c.provinsi.in_(not_found_locations))
                .group_by(sub_query.c.provinsi)
            )
        
        data_dict_not_found = {item[0]: int(item[1]) for item in query.all()}
        data_dict = {**data_dict, **data_dict_not_found}
        
    data_result = []
    for key in data_dict.keys():
        if key is None:
            continue
        if provinsi:
            if kabupaten_kota:
                params = {'provinsi': provinsi, 'kabupaten_kota': kabupaten_kota, 'kecamatan': key}
                title = f'{key}, {kabupaten_kota}, {provinsi}'
            else:    
                params = {'provinsi': provinsi, 'kabupaten_kota': key}
                title = f'{key}, {provinsi}'
        else:
            params = {'provinsi': key}
            title = key
        
        lonlat = db.execute(query_str, params).fetchone()
        lonlat = lonlat[0]
        
        data_result.append({
            'region': lonlat,
            'title': title,
            'populasi': data_dict[key]
        })
    
    return data_result
    
def get_ringkasan_populasi(db, tahun:int=None, provinsi:str=None, kabupaten_kota:str=None, perah_pedaging:str=None, jantan_betina:str=None, dewasa_anakan:str=None):
    sub_query = (
        db.query(DimWaktu.tahun,
                 DimLokasi.provinsi,
                 DimLokasi.kabupaten_kota,
                 DimLokasi.kecamatan,
                 FactPopulasiStream.tipe_ternak,
                 FactPopulasiStream.jenis_kelamin,
                 FactPopulasiStream.tipe_usia,
                 FactPopulasiStream.jumlah)
        .join(DimWaktu, DimWaktu.id == FactPopulasiStream.id_waktu)
        .join(DimLokasi, DimLokasi.id == FactPopulasiStream.id_lokasi)
    )
    
    if tahun:
        sub_query = sub_query.where(DimWaktu.tahun == tahun)
    if provinsi:
        sub_query = sub_query.where(DimLokasi.provinsi == provinsi)
    if kabupaten_kota:
        sub_query = sub_query.where(DimLokasi.kabupaten_kota == kabupaten_kota)
    if perah_pedaging:
        sub_query = sub_query.where(FactPopulasiStream.tipe_ternak == perah_pedaging)
    if jantan_betina:
        sub_query = sub_query.where(FactPopulasiStream.jenis_kelamin == jantan_betina)
    if dewasa_anakan:
        sub_query = sub_query.where(FactPopulasiStream.tipe_usia == dewasa_anakan)
        
    sub_query = sub_query.subquery()
    
    query = db.query(func.sum(sub_query.c.jumlah).label('total_populasi'))
    
    data = query.scalar()
    
    if data is None:
        sub_query = (
            db.query(DimWaktu.tahun,
                     DimLokasi.provinsi,
                     DimLokasi.kabupaten_kota,
                     DimLokasi.kecamatan,
                     FactPopulasi.tipe_ternak,
                     FactPopulasi.jenis_kelamin,
                     FactPopulasi.tipe_usia,
                     FactPopulasi.jumlah)
            .join(DimWaktu, DimWaktu.id == FactPopulasi.id_waktu)
            .join(DimLokasi, DimLokasi.id == FactPopulasi.id_lokasi)
        )
        
        if tahun:
            sub_query = sub_query.where(DimWaktu.tahun == tahun)
        if provinsi:
            sub_query = sub_query.where(DimLokasi.provinsi == provinsi)
        if kabupaten_kota:
            sub_query = sub_query.where(DimLokasi.kabupaten_kota == kabupaten_kota)
        if perah_pedaging:
            sub_query = sub_query.where(FactPopulasi.tipe_ternak == perah_pedaging)
        if jantan_betina:
            sub_query = sub_query.where(FactPopulasi.jenis_kelamin == jantan_betina)
        if dewasa_anakan:
            sub_query = sub_query.where(FactPopulasi.tipe_usia == dewasa_anakan)
            
        sub_query = sub_query.subquery()
        
        query = db.query(func.sum(sub_query.c.jumlah).label('total_populasi'))
        
        data = query.scalar()

    if data:
        return data
    else:
        return 0
    
def get_table_data(db, tahun:int=None, provinsi:str=None, kabupaten_kota:str=None, kecamatan:str=None, perah_pedaging:str=None, jantan_betina:str=None, dewasa_anakan:str=None, db_type='stream'):
    
    if db_type == 'stream':
        sub_query = (
            db.query(DimWaktu.tahun,
                     DimLokasi.provinsi,
                     DimLokasi.kabupaten_kota,
                     DimLokasi.kecamatan,
                     FactPopulasiStream.tipe_ternak,
                     FactPopulasiStream.jenis_kelamin,
                     FactPopulasiStream.tipe_usia,
                     FactPopulasiStream.jumlah)
            .join(DimWaktu, DimWaktu.id == FactPopulasiStream.id_waktu)
            .join(DimLokasi, DimLokasi.id == FactPopulasiStream.id_lokasi)
        )
        
        if tahun:
            sub_query = sub_query.where(DimWaktu.tahun == tahun)
        else:
            sub_query = sub_query.where(DimWaktu.tahun > 2022)
        if provinsi:
            sub_query = sub_query.where(DimLokasi.provinsi == provinsi)
        if kabupaten_kota:
            sub_query = sub_query.where(DimLokasi.kabupaten_kota == kabupaten_kota)
        if kecamatan:
            sub_query = sub_query.where(DimLokasi.kecamatan == kecamatan)
        if perah_pedaging:
            sub_query = sub_query.where(FactPopulasiStream.tipe_ternak == perah_pedaging)
        if jantan_betina:
            sub_query = sub_query.where(FactPopulasiStream.jenis_kelamin == jantan_betina)
        if dewasa_anakan:
            sub_query = sub_query.where(FactPopulasiStream.tipe_usia == dewasa_anakan)
        
    else:
        sub_query = (
            db.query(DimWaktu.tahun,
                     DimLokasi.provinsi,
                     DimLokasi.kabupaten_kota,
                     DimLokasi.kecamatan,
                     FactPopulasi.tipe_ternak,
                     FactPopulasi.jenis_kelamin,
                     FactPopulasi.tipe_usia,
                     FactPopulasi.jumlah)
            .join(DimWaktu, DimWaktu.id == FactPopulasi.id_waktu)
            .join(DimLokasi, DimLokasi.id == FactPopulasi.id_lokasi)
        )
    
        if tahun:
            sub_query = sub_query.where(DimWaktu.tahun == tahun)
        else:
            sub_query = sub_query.where(DimWaktu.tahun > 2022)
        if provinsi:
            sub_query = sub_query.where(DimLokasi.provinsi == provinsi)
        if kabupaten_kota:
            sub_query = sub_query.where(DimLokasi.kabupaten_kota == kabupaten_kota)
        if kecamatan:
            sub_query = sub_query.where(DimLokasi.kecamatan == kecamatan)
        if perah_pedaging:
            sub_query = sub_query.where(FactPopulasi.tipe_ternak == perah_pedaging)
        if jantan_betina:
            sub_query = sub_query.where(FactPopulasi.jenis_kelamin == jantan_betina)
        if dewasa_anakan:
            sub_query = sub_query.where(FactPopulasi.tipe_usia == dewasa_anakan)
        
    sub_query = sub_query.subquery()
    
    query = db.query(func.sum(sub_query.c.jumlah).label('total_populasi'))
    
    data = query.scalar()
    
    if data:
        return data
    else:
        return 0
    
def get_total_populasi(db, tahun:int=None, provinsi:str=None, kabupaten_kota:str=None, kecamatan:str=None, db_type='stream'):
    
    if db_type == 'stream':
        sub_query = (
            db.query(FactPopulasiStream.jumlah)
            .join(DimWaktu, DimWaktu.id == FactPopulasiStream.id_waktu)
            .join(DimLokasi, DimLokasi.id == FactPopulasiStream.id_lokasi)
        )
    else:
        sub_query = (
            db.query(FactPopulasi.jumlah)
            .join(DimWaktu, DimWaktu.id == FactPopulasi.id_waktu)
            .join(DimLokasi, DimLokasi.id == FactPopulasi.id_lokasi)
        )
    
    if tahun:
        sub_query = sub_query.where(DimWaktu.tahun == tahun)
    
    if provinsi:
        sub_query = sub_query.where(DimLokasi.provinsi == provinsi)
        
    if kabupaten_kota:
        sub_query = sub_query.where(DimLokasi.kabupaten_kota == kabupaten_kota)
    else:
        sub_query = sub_query.where(DimLokasi.kabupaten_kota.is_(None))
    
    if kecamatan:
        sub_query = sub_query.where(DimLokasi.kecamatan == kecamatan)
    else:
        sub_query = sub_query.where(DimLokasi.kecamatan.is_(None))
        
    sub_query = sub_query.subquery()
    
    query = db.query(func.sum(sub_query.c.jumlah).label('total_populasi'))
    
    data = query.scalar()
    
    if data:
        return data
    else:
        return 0
     
def get_table(db, tahun:int=None, provinsi:str=None, kabupaten_kota:str=None, perah_pedaging:str=None, dewasa_anakan:str=None, jantan_betina:str=None):
    sub_query = (
        db.query(DimWaktu.tahun,
                 DimLokasi.provinsi,
                 DimLokasi.kabupaten_kota,
                 DimLokasi.kecamatan,
                 FactPopulasiStream.jumlah)
        .join(DimWaktu, DimWaktu.id == FactPopulasiStream.id_waktu)
        .join(DimLokasi, DimLokasi.id == FactPopulasiStream.id_lokasi)
    )
    
    if tahun:
        sub_query = sub_query.where(DimWaktu.tahun == tahun)
    if provinsi:
        sub_query = sub_query.where(DimLokasi.provinsi == provinsi)
    if kabupaten_kota:
        sub_query = sub_query.where(DimLokasi.kabupaten_kota == kabupaten_kota)
        
    sub_query = sub_query.subquery()
    
    if provinsi:
        if kabupaten_kota:
            query = db.query(sub_query.c.kecamatan)
            
            locations = (
                db.query(DimLokasi.kecamatan)
                .where(DimLokasi.provinsi == provinsi)
                .where(DimLokasi.kabupaten_kota == kabupaten_kota)
                .distinct()
            ).all()
        else:
            query = db.query(sub_query.c.kabupaten_kota)
            
            locations = (
                db.query(DimLokasi.kabupaten_kota)
                .where(DimLokasi.provinsi == provinsi)
                .distinct()
            ).all()
    else:
        query = db.query(sub_query.c.provinsi)
        
        locations = (
            db.query(DimLokasi.provinsi)
            .distinct()
        ).all()
        
    wilayah_list = [data[0] for data in query.distinct().all()]
    
    table_populasi = []
    for wilayah in wilayah_list:
        data = {}
        data['wilayah'] = wilayah
        
        if provinsi:
            if kabupaten_kota:
                data['perah_dewasa_jantan'] = get_table_data(db, tahun, provinsi, kabupaten_kota, wilayah, 'Perah', 'Jantan', 'Dewasa', 'stream')
                data['perah_dewasa_betina'] = get_table_data(db, tahun, provinsi, kabupaten_kota, wilayah, 'Perah', 'Betina', 'Dewasa', 'stream')
                data['perah_anakan_jantan'] = get_table_data(db, tahun, provinsi, kabupaten_kota, wilayah, 'Perah', 'Jantan', 'Anakan', 'stream')
                data['perah_anakan_betina'] = get_table_data(db, tahun, provinsi, kabupaten_kota, wilayah, 'Perah', 'Betina', 'Anakan', 'stream')
                data['pedaging_dewasa_jantan'] = get_table_data(db, tahun, provinsi, kabupaten_kota, wilayah, 'Pedaging', 'Jantan', 'Dewasa', 'stream')
                data['pedaging_dewasa_betina'] = get_table_data(db, tahun, provinsi, kabupaten_kota, wilayah, 'Pedaging', 'Betina', 'Dewasa', 'stream')
                data['pedaging_anakan_jantan'] = get_table_data(db, tahun, provinsi, kabupaten_kota, wilayah, 'Pedaging', 'Jantan', 'Anakan', 'stream')
                data['pedaging_anakan_betina'] = get_table_data(db, tahun, provinsi, kabupaten_kota, wilayah, 'Pedaging', 'Betina', 'Anakan', 'stream') 
                
                if tahun is None:
                    data['total_populasi'] = data['perah_dewasa_jantan'] + data['perah_dewasa_betina'] + data['perah_anakan_jantan'] + data['perah_anakan_betina'] + data['pedaging_dewasa_jantan'] + data['pedaging_dewasa_betina'] + data['pedaging_anakan_jantan'] + data['pedaging_anakan_betina']
                else:
                    if tahun >= 2023:
                        data['total_populasi'] = data['perah_dewasa_jantan'] + data['perah_dewasa_betina'] + data['perah_anakan_jantan'] + data['perah_anakan_betina'] + data['pedaging_dewasa_jantan'] + data['pedaging_dewasa_betina'] + data['pedaging_anakan_jantan'] + data['pedaging_anakan_betina']
                    else:
                        data['total_populasi'] = get_total_populasi(db, tahun, provinsi, kabupaten_kota, wilayah, 'stream')
                    
            else:
                data['perah_dewasa_jantan'] = get_table_data(db, tahun, provinsi, wilayah, None, 'Perah', 'Jantan', 'Dewasa', 'stream')
                data['perah_dewasa_betina'] = get_table_data(db, tahun, provinsi, wilayah, None, 'Perah', 'Betina', 'Dewasa', 'stream')
                data['perah_anakan_jantan'] = get_table_data(db, tahun, provinsi, wilayah, None, 'Perah', 'Jantan', 'Anakan', 'stream')
                data['perah_anakan_betina'] = get_table_data(db, tahun, provinsi, wilayah, None, 'Perah', 'Betina', 'Anakan', 'stream')
                data['pedaging_dewasa_jantan'] = get_table_data(db, tahun, provinsi, wilayah, None, 'Pedaging', 'Jantan', 'Dewasa', 'stream')
                data['pedaging_dewasa_betina'] = get_table_data(db, tahun, provinsi, wilayah, None, 'Pedaging', 'Betina', 'Dewasa', 'stream')
                data['pedaging_anakan_jantan'] = get_table_data(db, tahun, provinsi, wilayah, None, 'Pedaging', 'Jantan', 'Anakan', 'stream')
                data['pedaging_anakan_betina'] = get_table_data(db, tahun, provinsi, wilayah, None, 'Pedaging', 'Betina', 'Anakan', 'stream')
                
                if tahun is None:
                    data['total_populasi'] = data['perah_dewasa_jantan'] + data['perah_dewasa_betina'] + data['perah_anakan_jantan'] + data['perah_anakan_betina'] + data['pedaging_dewasa_jantan'] + data['pedaging_dewasa_betina'] + data['pedaging_anakan_jantan'] + data['pedaging_anakan_betina']
                else:
                    if tahun >= 2023:
                        data['total_populasi'] = data['perah_dewasa_jantan'] + data['perah_dewasa_betina'] + data['perah_anakan_jantan'] + data['perah_anakan_betina'] + data['pedaging_dewasa_jantan'] + data['pedaging_dewasa_betina'] + data['pedaging_anakan_jantan'] + data['pedaging_anakan_betina']
                    else:
                        data['total_populasi'] = get_total_populasi(db, tahun, provinsi, wilayah, None, 'stream')
        else:
            data['perah_dewasa_jantan'] = get_table_data(db, tahun, wilayah, None, None, 'Perah', 'Jantan', 'Dewasa', 'stream')
            data['perah_dewasa_betina'] = get_table_data(db, tahun, wilayah, None, None, 'Perah', 'Betina', 'Dewasa', 'stream')
            data['perah_anakan_jantan'] = get_table_data(db, tahun, wilayah, None, None, 'Perah', 'Jantan', 'Anakan', 'stream')
            data['perah_anakan_betina'] = get_table_data(db, tahun, wilayah, None, None, 'Perah', 'Betina', 'Anakan', 'stream')
            data['pedaging_dewasa_jantan'] = get_table_data(db, tahun, wilayah, None, None, 'Pedaging', 'Jantan', 'Dewasa', 'stream')
            data['pedaging_dewasa_betina'] = get_table_data(db, tahun, wilayah, None, None, 'Pedaging', 'Betina', 'Dewasa', 'stream')
            data['pedaging_anakan_jantan'] = get_table_data(db, tahun, wilayah, None, None, 'Pedaging', 'Jantan', 'Anakan', 'stream')
            data['pedaging_anakan_betina'] = get_table_data(db, tahun, wilayah, None, None, 'Pedaging', 'Betina', 'Anakan', 'stream')
            
            if tahun is None:
                data['total_populasi'] = data['perah_dewasa_jantan'] + data['perah_dewasa_betina'] + data['perah_anakan_jantan'] + data['perah_anakan_betina'] + data['pedaging_dewasa_jantan'] + data['pedaging_dewasa_betina'] + data['pedaging_anakan_jantan'] + data['pedaging_anakan_betina']
            else:
                if tahun >= 2023:
                    data['total_populasi'] = data['perah_dewasa_jantan'] + data['perah_dewasa_betina'] + data['perah_anakan_jantan'] + data['perah_anakan_betina'] + data['pedaging_dewasa_jantan'] + data['pedaging_dewasa_betina'] + data['pedaging_anakan_jantan'] + data['pedaging_anakan_betina']
                else:
                    data['total_populasi'] = get_total_populasi(db, tahun, wilayah, None, None, 'stream')
            
        table_populasi.append(data)
    
    locations = [item[0] for item in locations if item[0] is not None]
    not_found_locations = set(locations) - set(wilayah_list)
    
    if len(not_found_locations) > 0:
        for location in not_found_locations:
            data = {}
            data['wilayah'] = location
            
            if provinsi:
                if kabupaten_kota:
                    data['perah_dewasa_jantan'] = get_table_data(db, tahun, provinsi, kabupaten_kota, location, 'Perah', 'Jantan', 'Dewasa', 'batch')
                    data['perah_dewasa_betina'] = get_table_data(db, tahun, provinsi, kabupaten_kota, location, 'Perah', 'Betina', 'Dewasa', 'batch')
                    data['perah_anakan_jantan'] = get_table_data(db, tahun, provinsi, kabupaten_kota, location, 'Perah', 'Jantan', 'Anakan', 'batch')
                    data['perah_anakan_betina'] = get_table_data(db, tahun, provinsi, kabupaten_kota, location, 'Perah', 'Betina', 'Anakan', 'batch')
                    data['pedaging_dewasa_jantan'] = get_table_data(db, tahun, provinsi, kabupaten_kota, location, 'Pedaging', 'Jantan', 'Dewasa', 'batch')
                    data['pedaging_dewasa_betina'] = get_table_data(db, tahun, provinsi, kabupaten_kota, location, 'Pedaging', 'Betina', 'Dewasa', 'batch')
                    data['pedaging_anakan_jantan'] = get_table_data(db, tahun, provinsi, kabupaten_kota, location, 'Pedaging', 'Jantan', 'Anakan', 'batch')
                    data['pedaging_anakan_betina'] = get_table_data(db, tahun, provinsi, kabupaten_kota, location, 'Pedaging', 'Betina', 'Anakan', 'batch')
                else:
                    data['perah_dewasa_jantan'] = get_table_data(db, tahun, provinsi, location, None, 'Perah', 'Jantan', 'Dewasa', 'batch')
                    data['perah_dewasa_betina'] = get_table_data(db, tahun, provinsi, location, None, 'Perah', 'Betina', 'Dewasa', 'batch')
                    data['perah_anakan_jantan'] = get_table_data(db, tahun, provinsi, location, None, 'Perah', 'Jantan', 'Anakan', 'batch')
                    data['perah_anakan_betina'] = get_table_data(db, tahun, provinsi, location, None, 'Perah', 'Betina', 'Anakan', 'batch')
                    data['pedaging_dewasa_jantan'] = get_table_data(db, tahun, provinsi, location, None, 'Pedaging', 'Jantan', 'Dewasa', 'batch')
                    data['pedaging_dewasa_betina'] = get_table_data(db, tahun, provinsi, location, None, 'Pedaging', 'Betina', 'Dewasa', 'batch')
                    data['pedaging_anakan_jantan'] = get_table_data(db, tahun, provinsi, location, None, 'Pedaging', 'Jantan', 'Anakan', 'batch')
                    data['pedaging_anakan_betina'] = get_table_data(db, tahun, provinsi, location, None, 'Pedaging', 'Betina', 'Anakan', 'batch')
            else:
                data['perah_dewasa_jantan'] = get_table_data(db, tahun, location, None, None, 'Perah', 'Jantan', 'Dewasa', 'batch')
                data['perah_dewasa_betina'] = get_table_data(db, tahun, location, None, None, 'Perah', 'Betina', 'Dewasa', 'batch')
                data['perah_anakan_jantan'] = get_table_data(db, tahun, location, None, None, 'Perah', 'Jantan', 'Anakan', 'batch')
                data['perah_anakan_betina'] = get_table_data(db, tahun, location, None, None, 'Perah', 'Betina', 'Anakan', 'batch')
                data['pedaging_dewasa_jantan'] = get_table_data(db, tahun, location, None, None, 'Pedaging', 'Jantan', 'Dewasa', 'batch')
                data['pedaging_dewasa_betina'] = get_table_data(db, tahun, location, None, None, 'Pedaging', 'Betina', 'Dewasa', 'batch')
                data['pedaging_anakan_jantan'] = get_table_data(db, tahun, location, None, None, 'Pedaging', 'Jantan', 'Anakan', 'batch')
                data['pedaging_anakan_betina'] = get_table_data(db, tahun, location, None, None, 'Pedaging', 'Betina', 'Anakan', 'batch')
            
            if (data['perah_dewasa_jantan'] == 0) and (data['perah_dewasa_betina'] == 0) and (data['perah_anakan_jantan'] == 0) and (data['perah_anakan_betina'] == 0) and (data['pedaging_dewasa_jantan'] == 0) and (data['pedaging_dewasa_betina'] == 0) and (data['pedaging_anakan_jantan'] == 0) and (data['pedaging_anakan_betina'] == 0):
                continue
            
            table_populasi.append(data)
    
    if perah_pedaging != None:
        if perah_pedaging == 'Perah':
            for row in table_populasi:
                for key in row.keys():
                    if 'pedaging' in key:
                        row[key] = -1
        elif perah_pedaging == 'Pedaging':
            for row in table_populasi:
                for key in row.keys():
                    if 'perah' in key:
                        row[key] = -1
        
        if dewasa_anakan != None:
            if dewasa_anakan == 'Dewasa':
                for row in table_populasi:
                    for key in row.keys():
                        if 'anakan' in key:
                            row[key] = -1
            elif dewasa_anakan == 'Anakan':
                for row in table_populasi:
                    for key in row.keys():
                        if 'dewasa' in key:
                            row[key] = -1
            
            if jantan_betina != None:
                if jantan_betina == 'Jantan':
                    for row in table_populasi:
                        for key in row.keys():
                            if 'betina' in key:
                                row[key] = -1
                elif jantan_betina == 'Betina':
                    for row in table_populasi:
                        for key in row.keys():
                            if 'jantan' in key:
                                row[key] = -1
        
    return table_populasi
                
def convert_decimals(obj):
    if isinstance(obj, dict):
        return {k: convert_decimals(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_decimals(i) for i in obj]
    elif isinstance(obj, Decimal):
        return float(obj)
    else:
        return obj    

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
    
    try:
        responses = {}
        
        # Ternak Potong
        responses['ternak_potong'] = {}
        responses['ternak_potong']['total_produksi'] = get_produksi_data(db, 2)
        responses['ternak_potong']['total_distribusi'] = get_distribusi_data(db, 2)
        
        if responses['ternak_potong']['total_produksi']:
            if responses['ternak_potong']['total_produksi'] == 0:
                responses['ternak_potong']['persentase'] = 0
            else:
                responses['ternak_potong']['persentase'] = round(
                    ((responses['ternak_potong']['total_distribusi'] or 0) / responses['ternak_potong']['total_produksi']) * 100, 2
                )
        else:
            responses['ternak_potong']['persentase'] = 0
            
        # Daging Ternak
        responses['daging_ternak'] = {}
        responses['daging_ternak']['total_produksi'] = get_produksi_data(db, 1)
        responses['daging_ternak']['total_distribusi'] = get_distribusi_data(db, 1)
        
        if responses['daging_ternak']['total_produksi']:
            if responses['daging_ternak']['total_produksi'] == 0:
                responses['daging_ternak']['persentase'] = 0
            else:
                responses['daging_ternak']['persentase'] = round(
                    ((responses['daging_ternak']['total_distribusi'] or 0) / responses['daging_ternak']['total_produksi']) * 100, 2
                )
        else:
            responses['daging_ternak']['persentase'] = 0
            
        # Susu Segar
        responses['susu_segar'] = {}
        responses['susu_segar']['total_produksi'] = get_produksi_data(db, 3)
        responses['susu_segar']['total_distribusi'] = get_distribusi_data(db, 3)
        
        if responses['susu_segar']['total_produksi']:
            if responses['susu_segar']['total_produksi'] == 0:
                responses['susu_segar']['persentase'] = 0
            else:
                responses['susu_segar']['persentase'] = round(
                    ((responses['susu_segar']['total_distribusi'] or 0) / responses['susu_segar']['total_produksi']) * 100, 2
                )
        else:
            responses['susu_segar']['persentase'] = 0
            
        # Produksi dan Distribusi Ternak Potong
        produksi = get_produksi_series_by_interval(db, 2, days=365)
        distribusi = get_distribusi_series_by_interval(db, 2, days=365)
        pro_dis_ternak_potong_list = []
        for i in range(len(produksi)):
            pro_dis_ternak_potong_list.append({
                'label': list(produksi.keys())[i],
                'produksi': list(produksi.values())[i],
                'distribusi': list(distribusi.values())[i]
            })
            
        responses['pro_dis_ternak_potong'] = pro_dis_ternak_potong_list
        
        # Produksi dan Distribusi Daging Ternak
        produksi = get_produksi_series_by_interval(db, 1, days=365)
        distribusi = get_distribusi_series_by_interval(db, 1, days=365)
        pro_dis_daging_ternak_list = []
        for i in range(len(produksi)):
            pro_dis_daging_ternak_list.append({
                'label': list(produksi.keys())[i],
                'produksi': list(produksi.values())[i],
                'distribusi': list(distribusi.values())[i]
            })
            
        responses['pro_dis_daging_ternak'] = pro_dis_daging_ternak_list
        
        # Produksi dan Distribusi Susu Segar
        produksi = get_produksi_series_by_interval(db, 3, days=365)
        distribusi = get_distribusi_series_by_interval(db, 3, days=365)
        pro_dis_susu_segar_list = []
        for i in range(len(produksi)):
            pro_dis_susu_segar_list.append({
                'label': list(produksi.keys())[i],
                'produksi': list(produksi.values())[i],
                'distribusi': list(distribusi.values())[i]
            })
            
        responses['pro_dis_susu_segar'] = pro_dis_susu_segar_list
        
        # Sebaran Populasi
        responses['sebaran_populasi_all'] = get_sebaran_populasi_all(db, tahun, provinsi, kabupaten_kota, perah_pedaging, jantan_betina, dewasa_anakan)
       
        # Ringkasan Populasi
        responses['ringkasan_populasi'] = {}
        responses['ringkasan_populasi']['jumlah_perah_dewasa'] = get_ringkasan_populasi(db, tahun, provinsi, kabupaten_kota, 'Perah', jantan_betina, 'Dewasa')
        responses['ringkasan_populasi']['jumlah_perah_anakan'] = get_ringkasan_populasi(db, tahun, provinsi, kabupaten_kota, 'Perah', jantan_betina, 'Anakan')
        responses['ringkasan_populasi']['jumlah_pedaging_dewasa'] = get_ringkasan_populasi(db, tahun, provinsi, kabupaten_kota, 'Pedaging', jantan_betina, 'Dewasa')
        responses['ringkasan_populasi']['jumlah_pedaging_anakan'] = get_ringkasan_populasi(db, tahun, provinsi, kabupaten_kota, 'Pedaging', jantan_betina, 'Anakan')
        
        # Table Populasi
        responses['table'] = get_table(db, tahun, provinsi, kabupaten_kota, perah_pedaging, dewasa_anakan, jantan_betina)
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=convert_decimals(responses)
        )
    
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": str(e)}
    )
    