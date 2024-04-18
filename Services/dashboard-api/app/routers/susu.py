from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database.connection import SessionLocal
from app.database.models import DistribusiSusu, DistribusiTernak, \
                                ProduksiSusu, ProduksiTernak, \
                                UnitTernak


router = APIRouter(redirect_slashes=False)

def get_db():   
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        

@router.get(path='/')
async def get_susu_data(db: Session = Depends(get_db)):
    
    responses = {}
    
    dist_year = (
        db.query(func.extract('year', DistribusiSusu.tgl_distribusi))
        .distinct()
        .all()
    )
    
    prod_year = (
        db.query(func.extract('year', ProduksiSusu.tgl_produksi))
        .distinct()
        .all()
    )
    
    for year in dist_year + prod_year:
        if str(int(year[0])) not in responses.keys():
            responses[str(int(year[0]))] = {}
          
    # Get wilayah data  
    for year in responses.keys():
        
        # Get id_unit_ternak data
        dist_id_unit_ternak = (
            db.query(DistribusiSusu.id_unit_ternak)
            .distinct()
            .all()
        )
        
        prod_id_unit_ternak = (
            db.query(ProduksiSusu.id_unit_ternak)
            .distinct()
            .all()
        )
        
        id_unit_ternak_list = []
        for id_unit_ternak in dist_id_unit_ternak + prod_id_unit_ternak:
            if id_unit_ternak[0] not in id_unit_ternak_list:
                id_unit_ternak_list.append(id_unit_ternak[0])
                
        
        # Get id_wilayah data
        id_wilayah_dict = {}
        for id_unit_ternak in id_unit_ternak_list:
            id_wilayah = (
                db.query(UnitTernak.id,
                         UnitTernak.provinsi_id)
                .where(UnitTernak.id == id_unit_ternak)
                .all()
            )[0]
                
            if id_wilayah[1] not in id_wilayah_dict.keys():
                id_wilayah_dict[id_wilayah[1]] = {}
                
            if id_wilayah[0] not in id_wilayah_dict[id_wilayah[1]].keys():
                id_wilayah_dict[id_wilayah[1]][id_wilayah[0]] = {}
        
        responses[year] = id_wilayah_dict
        
    # Get Susu Data
    for year in responses.keys():
        for provinsi in responses[year].keys():
            for id_unit_ternak in responses[year][provinsi].keys():
                
                # Get Susu Segar Data
                responses[year][provinsi][id_unit_ternak]['susu_segar'] = {}
                
                dist_susu_segar = (
                    db.query(func.sum(DistribusiSusu.jumlah))
                    .where(func.extract('year', DistribusiSusu.tgl_distribusi) == year)
                    .where(DistribusiSusu.id_unit_ternak == id_unit_ternak)
                    .where(DistribusiSusu.id_jenis_produk == 3)
                    .scalar()
                )
                
                if dist_susu_segar is None:
                    responses[year][provinsi][id_unit_ternak]['susu_segar']['distribusi'] = 0
                else:
                    responses[year][provinsi][id_unit_ternak]['susu_segar']['distribusi'] = dist_susu_segar
                    
                prod_susu_segar = (
                    db.query(func.sum(ProduksiSusu.jumlah))
                    .where(func.extract('year', ProduksiSusu.tgl_produksi) == year)
                    .where(ProduksiSusu.id_unit_ternak == id_unit_ternak)
                    .where(ProduksiSusu.id_jenis_produk == 3)
                    .scalar()
                )
                
                if prod_susu_segar is None:
                    responses[year][provinsi][id_unit_ternak]['susu_segar']['produksi'] = 0
                else:
                    responses[year][provinsi][id_unit_ternak]['susu_segar']['produksi'] = prod_susu_segar
                    
                # Get Susu Pasteurisasi Data
                responses[year][provinsi][id_unit_ternak]['susu_pasteurisasi'] = {}
                
                dist_susu_pasteurisasi = (
                    db.query(func.sum(DistribusiSusu.jumlah))
                    .where(func.extract('year', DistribusiSusu.tgl_distribusi) == year)
                    .where(DistribusiSusu.id_unit_ternak == id_unit_ternak)
                    .where(DistribusiSusu.id_jenis_produk == 4)
                    .scalar()
                )
                
                if dist_susu_pasteurisasi is None:
                    responses[year][provinsi][id_unit_ternak]['susu_pasteurisasi']['distribusi'] = 0
                else:
                    responses[year][provinsi][id_unit_ternak]['susu_pasteurisasi']['distribusi'] = dist_susu_pasteurisasi
                    
                prod_susu_pasteurisasi = (
                    db.query(func.sum(ProduksiSusu.jumlah))
                    .where(func.extract('year', ProduksiSusu.tgl_produksi) == year)
                    .where(ProduksiSusu.id_unit_ternak == id_unit_ternak)
                    .where(ProduksiSusu.id_jenis_produk == 4)
                    .scalar()
                )
                
                if prod_susu_pasteurisasi is None:
                    responses[year][provinsi][id_unit_ternak]['susu_pasteurisasi']['produksi'] = 0
                else:
                    responses[year][provinsi][id_unit_ternak]['susu_pasteurisasi']['produksi'] = prod_susu_pasteurisasi
                
                # Get Susu Kefir Data
                responses[year][provinsi][id_unit_ternak]['susu_kefir'] = {}
                
                dist_susu_kefir = (
                    db.query(func.sum(DistribusiSusu.jumlah))
                    .where(func.extract('year', DistribusiSusu.tgl_distribusi) == year)
                    .where(DistribusiSusu.id_unit_ternak == id_unit_ternak)
                    .where(DistribusiSusu.id_jenis_produk == 5)
                    .scalar()
                )
                
                if dist_susu_kefir is None:
                    responses[year][provinsi][id_unit_ternak]['susu_kefir']['distribusi'] = 0
                else:
                    responses[year][provinsi][id_unit_ternak]['susu_kefir']['distribusi'] = dist_susu_kefir
                    
                prod_susu_kefir = (
                    db.query(func.sum(ProduksiSusu.jumlah))
                    .where(func.extract('year', ProduksiSusu.tgl_produksi) == year)
                    .where(ProduksiSusu.id_unit_ternak == id_unit_ternak)
                    .where(ProduksiSusu.id_jenis_produk == 5)
                    .scalar()
                )
                
                if prod_susu_kefir is None:
                    responses[year][provinsi][id_unit_ternak]['susu_kefir']['produksi'] = 0
                else:
                    responses[year][provinsi][id_unit_ternak]['susu_kefir']['produksi'] = prod_susu_kefir
                
                # Get Yogurt Data
                responses[year][provinsi][id_unit_ternak]['yogurt'] = {}
                
                dist_yogurt = (
                    db.query(func.sum(DistribusiSusu.jumlah))
                    .where(func.extract('year', DistribusiSusu.tgl_distribusi) == year)
                    .where(DistribusiSusu.id_unit_ternak == id_unit_ternak)
                    .where(DistribusiSusu.id_jenis_produk == 6)
                    .scalar()
                )
                
                if dist_yogurt is None:
                    responses[year][provinsi][id_unit_ternak]['yogurt']['distribusi'] = 0
                else:
                    responses[year][provinsi][id_unit_ternak]['yogurt']['distribusi'] = dist_yogurt
                    
                prod_yogurt = (
                    db.query(func.sum(ProduksiSusu.jumlah))
                    .where(func.extract('year', ProduksiSusu.tgl_produksi) == year)
                    .where(ProduksiSusu.id_unit_ternak == id_unit_ternak)
                    .where(ProduksiSusu.id_jenis_produk == 6)
                    .scalar()
                )
                
                if prod_yogurt is None:
                    responses[year][provinsi][id_unit_ternak]['yogurt']['produksi'] = 0
                else:
                    responses[year][provinsi][id_unit_ternak]['yogurt']['produksi'] = prod_yogurt                
                
                # Get Keju Data
                responses[year][provinsi][id_unit_ternak]['keju'] = {}
                
                dist_keju = (
                    db.query(func.sum(DistribusiSusu.jumlah))
                    .where(func.extract('year', DistribusiSusu.tgl_distribusi) == year)
                    .where(DistribusiSusu.id_unit_ternak == id_unit_ternak)
                    .where(DistribusiSusu.id_jenis_produk == 7)
                    .scalar()
                )
                
                if dist_keju is None:
                    responses[year][provinsi][id_unit_ternak]['keju']['distribusi'] = 0
                else:
                    responses[year][provinsi][id_unit_ternak]['keju']['distribusi'] = dist_keju
                    
                prod_keju = (
                    db.query(func.sum(ProduksiSusu.jumlah))
                    .where(func.extract('year', ProduksiSusu.tgl_produksi) == year)
                    .where(ProduksiSusu.id_unit_ternak == id_unit_ternak)
                    .where(ProduksiSusu.id_jenis_produk == 7)
                    .scalar()
                )
                
                if prod_keju is None:
                    responses[year][provinsi][id_unit_ternak]['keju']['produksi'] = 0
                else:
                    responses[year][provinsi][id_unit_ternak]['keju']['produksi'] = prod_keju 
                    
                    
                # Get Prediction Data
                responses[year][provinsi][id_unit_ternak]['prediction'] = {}
                
                
                
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=responses
    )
    
   