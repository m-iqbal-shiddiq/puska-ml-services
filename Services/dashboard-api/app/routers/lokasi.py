from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy import distinct, func
from sqlalchemy.orm import aliased

from app.database.connection import SessionLocal
from app.database.models import DimUnitPeternakan, FactProduksi, DimLokasi, FactPopulasi

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
    
    sub_query = (
        db.query(FactPopulasi.id_peternakan,
                 func.max(FactPopulasi.id_waktu).label('max_id_waktu'))
        .group_by(FactPopulasi.id_peternakan)
    )
    
    sub_query = sub_query.subquery()
    
    populasi_cte = (
        db.query(FactPopulasi.id_peternakan, 
                 FactPopulasi.id_waktu,
                 func.sum(FactPopulasi.jumlah).label('total_jumlah'))
        .join(sub_query, (FactPopulasi.id_peternakan == sub_query.c.id_peternakan) & (FactPopulasi.id_waktu == sub_query.c.max_id_waktu))
        .group_by(FactPopulasi.id_peternakan, FactPopulasi.id_waktu)
    ).cte('populasi_cte')
    
    datas = (
        db.query(distinct(DimUnitPeternakan.nama_unit),
                 DimUnitPeternakan.longitude,
                 DimUnitPeternakan.latitude,
                 DimLokasi.kecamatan,
                 DimLokasi.kabupaten_kota,
                 DimLokasi.provinsi,
                 populasi_cte.c.total_jumlah)
        .join(FactProduksi, FactProduksi.id_unit_peternakan == DimUnitPeternakan.id)
        .join(DimLokasi, DimLokasi.id == DimUnitPeternakan.id_lokasi)
        .join(populasi_cte, populasi_cte.c.id_peternakan == DimUnitPeternakan.id)
        .where(DimUnitPeternakan.nama_unit != None)
        .where(FactProduksi.jumlah_produksi > 0)
        .all()
    )
    
    for data in datas:
        if data[6] is None:
            responses.append({
                'nama unit': data[0],
                'longitude': data[1],
                'latitude': data[2],
                'lokasi': f'{data[3].lower()}, {data[4].lower()}, {data[5].lower()}',
                'populasi': 0,
                'point': [data[1], data[2]]
            })
        else:
            responses.append({
                'nama unit': data[0],
                'longitude': data[1],
                'latitude': data[2],
                'lokasi': f'{data[3].lower()}, {data[4].lower()}, {data[5].lower()}',
                'populasi': float(data[6]),
                'point': [data[1], data[2]]
            })
    
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=responses
    )
    