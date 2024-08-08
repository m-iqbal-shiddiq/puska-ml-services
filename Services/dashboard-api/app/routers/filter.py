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
        
@router.get('/filter', status_code=status.HTTP_200_OK)
async def get_filter_data(db = Depends(get_db)):
    responses = {}
    
    # Tahun
    tahun = (
        db.query(DimWaktu.tahun)
        .distinct()
        .order_by(desc(DimWaktu.tahun))
        .all()
    )
    responses['tahun'] = [tahun[0] for tahun in tahun]
    
    # Wilayah
    wilayah = (
        db.query(DimLokasi.provinsi,
                 DimLokasi.kabupaten_kota)
        .where(DimLokasi.provinsi != None)
        .order_by(DimLokasi.provinsi, DimLokasi.kabupaten_kota)
        .all()
    )
    
    wilayah_dict = {}
    for wil in wilayah:
        if wil[0] not in wilayah_dict:
            wilayah_dict[wil[0]] = []
        
        if wil[1] is not None:
            wilayah_dict[wil[0]].append(wil[1])
    
    responses['wilayah'] = []
    for key in wilayah_dict:
        responses['wilayah'].append({
            'provinsi': key,
            'kabupaten_kota': wilayah_dict[key]
        })

    # Jenis Ternak
    responses['jenis_ternak'] = ['Perah', 'Pedaging']
    
    # Jenis Kelamin
    responses['jenis_kelamin'] = ['Jantan', 'Betina']
    
    # Group Usia
    responses['group_usia'] = ['Dewasa', 'Anakan']
    
    # Unit Peternakan
    unit_peternakan = (
        db.query(DimUnitPeternakan.nama_unit)
        .distinct()
        .where(DimUnitPeternakan.nama_unit != None)
        .order_by(DimUnitPeternakan.nama_unit)
        .all()
    )
    
    responses['unit_peternakan'] = [unit_peternakan[0] for unit_peternakan in unit_peternakan]
    
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=responses
    )