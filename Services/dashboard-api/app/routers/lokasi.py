from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy import distinct

from app.database.connection import SessionLocal
from app.database.models import DimUnitPeternakan, FactProduksi, DimLokasi

router = APIRouter(redirect_slashes=False)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
@router.get('/lokasi', status_code=status.HTTP_200_OK)
async def get_lokasi_data(db = Depends(get_db)):
    responses = []
    
    datas = (
        db.query(distinct(DimUnitPeternakan.nama_unit),
                 DimUnitPeternakan.longitude,
                 DimUnitPeternakan.latitude)
        .join(FactProduksi, FactProduksi.id_unit_peternakan == DimUnitPeternakan.id)
        .where(DimUnitPeternakan.nama_unit != None)
        .where(FactProduksi.jumlah_produksi > 0)
        .all()
    )
    
    for data in datas:
        responses.append({
            'nama unit': data[0],
            'point': [data[1], data[2]]
        })
    
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=responses
    )
    