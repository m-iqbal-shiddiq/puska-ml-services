from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy import desc

from app.database.connection import SessionLocal
from app.database.models import DimWaktu, DimLokasi, DimUnitPeternakan

router = APIRouter(redirect_slashes=False)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
@router.get('/tahun', status_code=status.HTTP_200_OK)
async def get_tahun(db = Depends(get_db)):
    waktu = (
        db.query(DimWaktu.tahun)
        .distinct()
        .order_by(desc(DimWaktu.tahun))
        .all()
    )
    
    waktu = [waktu[0] for waktu in waktu]
    
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=waktu
    )
    
@router.get('/provinsi', status_code=status.HTTP_200_OK)
async def get_provinsi(db = Depends(get_db)):
    try:
        provinsi = (
            db.query(DimLokasi.provinsi)
            .distinct()
            .where(DimLokasi.provinsi != None)
            .order_by(DimLokasi.provinsi)
            .all()
        )
        
        provinsi = [provinsi[0] for provinsi in provinsi]
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=provinsi
        )
        
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=str(e)
        )
    
@router.get('/kabupaten_kota', status_code=status.HTTP_200_OK)
async def get_kabupaten_kota(db = Depends(get_db), 
                             provinsi: str = None):
    
    try:
        if provinsi:
            kabupaten_kota = (
                db.query(DimLokasi.kabupaten_kota)
                .distinct()
                .where(DimLokasi.provinsi == provinsi)
                .where(DimLokasi.kabupaten_kota != None)
                .order_by(DimLokasi.kabupaten_kota)
                .all()
            )
        
            kabupaten_kota = [kabupaten_kota[0] for kabupaten_kota in kabupaten_kota]
            
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content=kabupaten_kota
            )
        else:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content='Provinsi harus diisi'
            )
            
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=str(e)
        )
        
@router.get('/jenis_ternak', status_code=status.HTTP_200_OK)
async def get_jenis_ternak():
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=['Perah', 'Pedaging']
    )
    
@router.get('/jenis_kelamin', status_code=status.HTTP_200_OK)
async def get_jenis_produk():
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=['Jantan', 'Betina']
    )
    
@router.get('/group_usia', status_code=status.HTTP_200_OK)
async def get_group_usia():
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=['Dewasa', 'Anakan']
    )
    
@router.get('/unit_peternakan', status_code=status.HTTP_200_OK)
async def get_unit_peternakan(db = Depends(get_db)):
    try:
        unit_peternakan = (
            db.query(DimUnitPeternakan.nama_unit)
            .distinct()
            .where(DimUnitPeternakan.nama_unit != None)
            .order_by(DimUnitPeternakan.nama_unit)
            .all()
        )
        
        unit_peternakan = [unit_peternakan[0] for unit_peternakan in unit_peternakan]
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=unit_peternakan
        )
        
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=str(e)
        )