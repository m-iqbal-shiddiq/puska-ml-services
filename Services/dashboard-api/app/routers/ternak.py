import datetime

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database.connection import SessionLocal
from app.database.models import DimWaktu, FactDistribusi, FactProduksi
# from app.database.models import DistribusiSusu, DistribusiTernak, \
#                                 ProduksiSusu, ProduksiTernak 


router = APIRouter(redirect_slashes=False)

def get_db(): 
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        

@router.get(path='/ternak')
async def get_ternak_data(db: Session = Depends(get_db)):
    
    responses = {}
    
    # Get ternak_potong data
    responses['ternak_potong'] = {}
    
    # Ternak potong
    responses['ternak_potong']['total_distribusi'] = (
        db.query(func.sum(FactDistribusi.jumlah_distribusi))
        .where(FactDistribusi.id_jenis_produk == 2)
        .scalar()
    )
    
    if responses['ternak_potong']['total_distribusi'] is None:
        responses['ternak_potong']['total_distribusi'] = 0
    
    responses['ternak_potong']['total_produksi'] = (
        db.query(func.sum(FactDistribusi.jumlah_penjualan))
        .where(FactDistribusi.id_jenis_produk == 2)
        .scalar()
    )
    
    if responses['ternak_potong']['total_produksi'] is None:
        responses['ternak_potong']['total_produksi'] = 0
        
    
    # Get daging_ternak data
    responses['daging_ternak'] = {}
    
    # Daging ternak
    responses['daging_ternak']['total_distribusi'] = (
        db.query(func.sum(FactDistribusi.jumlah_distribusi))
        .where(FactDistribusi.id_jenis_produk == 1)
        .scalar()
    )
    
    if responses['daging_ternak']['total_distribusi'] is None:
        responses['daging_ternak']['total_distribusi'] = 0
        
    responses['daging_ternak']['total_produksi'] = (
        db.query(func.sum(FactDistribusi.jumlah_penjualan))
        .where(FactDistribusi.id_jenis_produk == 1)
        .scalar()
    )
    
    if responses['daging_ternak']['total_produksi'] is None:
        responses['daging_ternak']['total_produksi'] = 0
    
    
    # Get susu_segar data
    responses['susu_segar'] = {}
    
    # Susu segar
    responses['susu_segar']['total_distribusi'] = (
        db.query(func.sum(FactDistribusi.jumlah_distribusi))
        .where(FactDistribusi.id_jenis_produk == 3)
        .scalar()
    )
    
    if responses['susu_segar']['total_distribusi'] is None:
        responses['susu_segar']['total_distribusi'] = 0
    
    responses['susu_segar']['total_produksi'] = (
        db.query(func.sum(FactDistribusi.jumlah_penjualan))
        .where(FactDistribusi.id_jenis_produk == 3)
        .scalar()
    )
    
    if responses['susu_segar']['total_produksi'] is None:
        responses['susu_segar']['total_produksi'] = 0
        
        
        
    # Get first date in database and current date
    start_date = (
        db.query(DimWaktu.tanggal)
        .order_by(DimWaktu.tanggal)
        .first()
    )[0]
    
    end_date = datetime.date.today()
    
    all_dates = {
        (start_date + datetime.timedelta(days=x)).strftime("%Y-%m-%d"): 0
        for x in range((end_date - start_date).days + 1)
    }
    
        
    # Get Produksi dan Distribusi Ternak Potong
    responses['pro_dis_ternak_potong'] = {}
    
    # Distribusi
    dis_ternak_potong = (
        db.query(FactDistribusi.id_waktu, func.sum(FactDistribusi.jumlah_distribusi))
        .where(FactDistribusi.id_jenis_produk == 2)
        .group_by(FactDistribusi.id_waktu)
        .order_by(FactDistribusi.id_waktu)
        .all()
    )
    
    dis_tanggal_ternak_potong = (
        db.query(DimWaktu.id, DimWaktu.tanggal)
        .where(DimWaktu.id.in_([item[0] for item in dis_ternak_potong]))
        .order_by(DimWaktu.id)
        .all()
    )
    
    dis_available_ternak_potong = {
        dis_tanggal_ternak_potong[i][1].strftime("%Y-%m-%d"): dis_ternak_potong[i][1] 
        for i in range(len(dis_tanggal_ternak_potong))
    }
    
    responses['pro_dis_ternak_potong']['distribusi'] = all_dates.copy()
    responses['pro_dis_ternak_potong']['distribusi'].update(dis_available_ternak_potong)
    
    # Produksi
    pro_ternak_potong = (
        db.query(FactProduksi.id_waktu, func.sum(FactProduksi.jumlah_produksi))
        .where(FactProduksi.id_jenis_produk == 2)
        .group_by(FactProduksi.id_waktu)
        .order_by(FactProduksi.id_waktu)
        .all()
    )
    
    pro_tanggal_ternak_potong = (
        db.query(DimWaktu.id, DimWaktu.tanggal)
        .where(DimWaktu.id.in_([item[0] for item in pro_ternak_potong]))
        .order_by(DimWaktu.id)
        .all()
    )
    
    pro_available_ternak_potong = {
        pro_tanggal_ternak_potong[i][1].strftime("%Y-%m-%d"): pro_ternak_potong[i][1] 
        for i in range(len(pro_tanggal_ternak_potong))
    }
    
    responses['pro_dis_ternak_potong']['produksi'] = all_dates.copy()
    responses['pro_dis_ternak_potong']['produksi'].update(pro_available_ternak_potong)
    
    
    # Get Produksi dan Distribusi Daging Ternak
    responses['pro_dis_daging_ternak'] = {}
    
    # Distribusi
    dis_daging_ternak = (
        db.query(FactDistribusi.id_waktu, func.sum(FactDistribusi.jumlah_distribusi))
        .where(FactDistribusi.id_jenis_produk == 1)
        .group_by(FactDistribusi.id_waktu)
        .order_by(FactDistribusi.id_waktu)
        .all()
    )
    
    dis_tanggal_daging_ternak = (
        db.query(DimWaktu.id, DimWaktu.tanggal)
        .where(DimWaktu.id.in_([item[0] for item in dis_daging_ternak]))
        .order_by(DimWaktu.id)
        .all()
    )
    
    dis_available_daging_ternak = {
        dis_tanggal_daging_ternak[i][1].strftime("%Y-%m-%d"): dis_daging_ternak[i][1] 
        for i in range(len(dis_tanggal_daging_ternak))
    }
    
    responses['pro_dis_daging_ternak']['distribusi'] = all_dates.copy()
    responses['pro_dis_daging_ternak']['distribusi'].update(dis_available_daging_ternak)
    
    # Produksi
    pro_daging_ternak = (
        db.query(FactProduksi.id_waktu, func.sum(FactProduksi.jumlah_produksi))
        .where(FactProduksi.id_jenis_produk == 1)
        .group_by(FactProduksi.id_waktu)
        .order_by(FactProduksi.id_waktu)
        .all()
    )
    
    pro_tanggal_daging_ternak = (
        db.query(DimWaktu.id, DimWaktu.tanggal)
        .where(DimWaktu.id.in_([item[0] for item in pro_daging_ternak]))
        .order_by(DimWaktu.id)
        .all()
    )
    
    pro_available_daging_ternak = {
        pro_tanggal_daging_ternak[i][1].strftime("%Y-%m-%d"): pro_daging_ternak[i][1] 
        for i in range(len(pro_tanggal_daging_ternak))
    }
    
    responses['pro_dis_daging_ternak']['produksi'] = all_dates.copy()
    responses['pro_dis_daging_ternak']['produksi'].update(pro_available_daging_ternak)
    
    # Get Produksi dan Distribusi Susu Segar
    responses['pro_dis_susu_segar'] = {}
    
    # Distribusi
    dis_susu_segar = (
        db.query(FactDistribusi.id_waktu, func.sum(FactDistribusi.jumlah_distribusi))
        .where(FactDistribusi.id_jenis_produk == 3)
        .group_by(FactDistribusi.id_waktu)
        .order_by(FactDistribusi.id_waktu)
        .all()
    )
    
    dis_tanggal_susu_segar = (
        db.query(DimWaktu.id, DimWaktu.tanggal)
        .where(DimWaktu.id.in_([item[0] for item in dis_susu_segar]))
        .order_by(DimWaktu.id)
        .all()
    )
    
    dis_available_susu_segar = {
        dis_tanggal_susu_segar[i][1].strftime("%Y-%m-%d"): dis_susu_segar[i][1] 
        for i in range(len(dis_tanggal_susu_segar))
    }
    
    responses['pro_dis_susu_segar']['distribusi'] = all_dates.copy()
    responses['pro_dis_susu_segar']['distribusi'].update(dis_available_susu_segar)
    
    # Produksi
    pro_susu_segar = (
        db.query(FactProduksi.id_waktu, func.sum(FactProduksi.jumlah_produksi))
        .where(FactProduksi.id_jenis_produk == 3)
        .group_by(FactProduksi.id_waktu)
        .order_by(FactProduksi.id_waktu)
        .all()
    )
    
    pro_tanggal_susu_segar = (
        db.query(DimWaktu.id, DimWaktu.tanggal)
        .where(DimWaktu.id.in_([item[0] for item in pro_susu_segar]))
        .order_by(DimWaktu.id)
        .all()
    )
    
    pro_available_susu_segar = {
        pro_tanggal_susu_segar[i][1].strftime("%Y-%m-%d"): pro_susu_segar[i][1] 
        for i in range(len(pro_tanggal_susu_segar))
    }
    
    responses['pro_dis_susu_segar']['produksi'] = all_dates.copy()
    responses['pro_dis_susu_segar']['produksi'].update(pro_available_susu_segar)
    
    
    # Get available year
    
    
    
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=responses
    )