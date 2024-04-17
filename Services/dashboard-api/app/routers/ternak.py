from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database.connection import SessionLocal
from app.database.models import DistribusiSusu, DistribusiTernak, \
                                ProduksiSusu, ProduksiTernak 


router = APIRouter(redirect_slashes=False)

def get_db(): 
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        

@router.get(path='/')
async def get_ternak_data(db: Session = Depends(get_db)):
    
    responses = {}
    
    # Get ternak_potong data
    responses['ternak_potong'] = {}

    responses['ternak_potong']['distribusi'] = (
        db.query(func.sum(DistribusiTernak.jumlah))
                .where(DistribusiTernak.satuan == 'ekor')
                .scalar()
    )
    
    responses['ternak_potong']['produksi'] = (
        db.query(func.sum(ProduksiTernak.jumlah))
                .where(ProduksiTernak.satuan == 'ekor')
                .scalar()
    )
    
    responses['ternak_potong']['persentase'] = (
        round(responses['ternak_potong']['distribusi'] / responses['ternak_potong']['produksi'], 2)
    )
    
    # Get daging_ternak data
    responses['daging_ternak'] = {}
    
    responses['daging_ternak']['distribusi'] = (
        db.query(func.sum(DistribusiTernak.jumlah))
                .where(DistribusiTernak.satuan == 'kg')
                .scalar()
    )
    
    responses['daging_ternak']['produksi'] = (
        db.query(func.sum(ProduksiTernak.jumlah))
                .where(ProduksiTernak.satuan == 'kg')
                .scalar()
    )
    
    responses['daging_ternak']['persentase'] = (
        round(responses['daging_ternak']['distribusi'] / responses['daging_ternak']['produksi'], 2)
    )
    
    # Get susu_segar data
    responses['susu_segar'] = {}
    
    responses['susu_segar']['distribusi'] = (
        db.query(func.sum(DistribusiSusu.jumlah))
                .where(DistribusiSusu.satuan == 'liter')
                .scalar()
    )
    
    responses['susu_segar']['produksi'] = (
        db.query(func.sum(ProduksiSusu.jumlah))
                .where(ProduksiSusu.satuan == 'liter')
                .scalar()
    )
    
    responses['susu_segar']['persentase'] = (
        round(responses['susu_segar']['distribusi'] / responses['susu_segar']['produksi'], 2)
    )
    
    # Get pro_dis_ternak_potong data
    responses['pro_dis_ternak_potong'] = {}
    
    items = (
        db.query(DistribusiTernak.tgl_distribusi, func.sum(DistribusiTernak.jumlah))
                .where(DistribusiTernak.satuan == 'ekor')
                .group_by(DistribusiTernak.tgl_distribusi)
                .order_by(DistribusiTernak.tgl_distribusi)
                .all()
    )
    res = {}
    for item in items:
        res[item[0].strftime('%Y-%m-%d')] = item[1]
    responses['pro_dis_ternak_potong']['distribusi'] = res
    
    items = (
        db.query(ProduksiTernak.tgl_produksi, func.sum(ProduksiTernak.jumlah))
                .where(ProduksiTernak.satuan == 'ekor')
                .group_by(ProduksiTernak.tgl_produksi)
                .order_by(ProduksiTernak.tgl_produksi)
                .all()
    )
    res = {}
    for item in items:
        res[item[0].strftime('%Y-%m-%d')] = item[1]
    responses['pro_dis_ternak_potong']['produksi'] = res
    
    # Get pro_dis_daging_ternak data
    responses['pro_dis_daging_ternak'] = {}
    
    items = (
        db.query(DistribusiTernak.tgl_distribusi, func.sum(DistribusiTernak.jumlah))
                .where(DistribusiTernak.satuan == 'kg')
                .group_by(DistribusiTernak.tgl_distribusi)
                .order_by(DistribusiTernak.tgl_distribusi)
                .all()
    )
    res = {}
    for item in items:
        res[item[0].strftime('%Y-%m-%d')] = item[1]
    responses['pro_dis_daging_ternak']['distribusi'] = res
    
    items = (
        db.query(ProduksiTernak.tgl_produksi, func.sum(ProduksiTernak.jumlah))
                .where(ProduksiTernak.satuan == 'kg')
                .group_by(ProduksiTernak.tgl_produksi)
                .order_by(ProduksiTernak.tgl_produksi)
                .all()
    )
    res = {}
    for item in items:
        res[item[0].strftime('%Y-%m-%d')] = item[1]
    responses['pro_dis_daging_ternak']['produksi'] = res
    
    # Get pro_dis_susu_segar data
    responses['pro_dis_susu_segar'] = {}
    
    items = (
        db.query(DistribusiSusu.tgl_distribusi, func.sum(DistribusiSusu.jumlah))
                .where(DistribusiSusu.satuan == 'liter')
                .group_by(DistribusiSusu.tgl_distribusi)
                .order_by(DistribusiSusu.tgl_distribusi)
                .all()
    )
    res = {}
    for item in items:
        res[item[0].strftime('%Y-%m-%d')] = item[1]
    responses['pro_dis_susu_segar']['distribusi'] = res
    
    items = (
        db.query(ProduksiSusu.tgl_produksi, func.sum(ProduksiSusu.jumlah))
                .where(ProduksiSusu.satuan == 'liter')
                .group_by(ProduksiSusu.tgl_produksi)
                .order_by(ProduksiSusu.tgl_produksi)
                .all()
    )
    res = {}
    for item in items:
        res[item[0].strftime('%Y-%m-%d')] = item[1]
    responses['pro_dis_susu_segar']['produksi'] = res
    
    
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=responses
    )