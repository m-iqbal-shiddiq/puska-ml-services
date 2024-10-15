from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from app.database.connection import SessionLocal
from app.database.models import DimUnitPeternakan

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
        db.query(DimUnitPeternakan.nama_unit,
                 DimUnitPeternakan.longitude,
                 DimUnitPeternakan.latitude)
        .where(DimUnitPeternakan.nama_unit != None)
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
    