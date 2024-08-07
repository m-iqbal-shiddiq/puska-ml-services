import datetime as dt

from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from sqlalchemy import func, and_, text
from sqlalchemy.orm import Session

from app.database.connection import SessionLocal
from app.database.models import DimLokasi, DimWaktu, FactDistribusi, FactProduksi, FactPopulasi
from app.schemas.ternak import TernakMasterData


router = APIRouter(redirect_slashes=False)

def get_db(): 
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_produksi_data(db, id_jenis_produk):
    query = (
        db.query(func.sum(FactProduksi.jumlah_produksi))
        .where(FactProduksi.id_jenis_produk == id_jenis_produk)
    )
    return query.scalar()

def get_distribusi_data(db, id_jenis_produk):
    query = (
        db.query(func.sum(FactDistribusi.jumlah_distribusi))
        .where(FactDistribusi.id_jenis_produk == id_jenis_produk)
    )
    return query.scalar()

def get_produksi_series_by_interval(db, id_jenis_produk:int, days=365):
    start_date = datetime.today() - timedelta(days=days)
    end_date = datetime.today()
    
    sub_query = (
        db.query(DimWaktu.tanggal,
                 FactProduksi.jumlah_produksi)
        .join(DimWaktu, DimWaktu.id == FactProduksi.id_waktu)
        .where(DimWaktu.tanggal >= start_date)
        .where(FactProduksi.id_jenis_produk == id_jenis_produk)
    )
    
    sub_query = sub_query.subquery()
    
    query = (
        db.query(sub_query.c.tanggal,
                 func.sum(sub_query.c.jumlah_produksi).label('total_distribusi'))
        .group_by(sub_query.c.tanggal)
        .order_by(sub_query.c.tanggal)
    )
    
    data_dict = {item[0].strftime('%d-%m-%Y'): int(item[1]) for item in query.all()}
    all_dates = {(start_date + timedelta(days=i)).strftime('%d-%m-%Y') for i in range((end_date - start_date).days)}
    complete_data = {date: data_dict.get(date, 0) for date in all_dates}
    sorted_data = sorted(complete_data.items(), key=lambda x: datetime.strptime(x[0], '%d-%m-%Y'))
    sorted_data_dict = dict(sorted_data)
    
    return sorted_data_dict

def get_distribusi_series_by_interval(db, id_jenis_produk:int, days=365):
    start_date = datetime.today() - timedelta(days=days)
    end_date = datetime.today()
    
    sub_query = (
        db.query(DimWaktu.tanggal,
                 FactDistribusi.jumlah_distribusi)
        .join(DimWaktu, DimWaktu.id == FactDistribusi.id_waktu)
        .where(DimWaktu.tanggal >= start_date)
        .where(FactDistribusi.id_jenis_produk == id_jenis_produk)
    )
    
    sub_query = sub_query.subquery()
    
    query = (
        db.query(sub_query.c.tanggal,
                 func.sum(sub_query.c.jumlah_distribusi).label('total_distribusi'))
        .group_by(sub_query.c.tanggal)
        .order_by(sub_query.c.tanggal)
    )
    
    data_dict = {item[0].strftime('%d-%m-%Y'): int(item[1]) for item in query.all()}
    all_dates = {(start_date + timedelta(days=i)).strftime('%d-%m-%Y') for i in range((end_date - start_date).days)}
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
                .group_by(sub_query.c.kecamatan)
            )
        else:
            query = (
                db.query(sub_query.c.kabupaten_kota,
                         func.sum(sub_query.c.jumlah).label('total_populasi'))
                .group_by(sub_query.c.kabupaten_kota)
            )
    else:
        query = (
            db.query(sub_query.c.provinsi,
                     func.sum(sub_query.c.jumlah).label('total_populasi'))
            .group_by(sub_query.c.provinsi)
        )
    
    data_dict = {item[0]: int(item[1]) for item in query.all()}
    print(data_dict)
    return data_dict
    



@router.get(path='/ternak', 
            # response_model=TernakMasterData, 
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
        produksi = get_produksi_series_by_interval(db, 2)
        distribusi = get_distribusi_series_by_interval(db, 2)
        pro_dis_ternak_potong_list = []
        for i in range(len(produksi)):
            pro_dis_ternak_potong_list.append({
                'label': list(produksi.keys())[i],
                'produksi': list(produksi.values())[i],
                'distribusi': list(distribusi.values())[i]
            })
            
        responses['pro_dis_ternak_potong'] = pro_dis_ternak_potong_list
        
        # Produksi dan Distribusi Daging Ternak
        produksi = get_produksi_series_by_interval(db, 1)
        distribusi = get_distribusi_series_by_interval(db, 1)
        pro_dis_daging_ternak_list = []
        for i in range(len(produksi)):
            pro_dis_daging_ternak_list.append({
                'label': list(produksi.keys())[i],
                'produksi': list(produksi.values())[i],
                'distribusi': list(distribusi.values())[i]
            })
            
        responses['pro_dis_daging_ternak'] = pro_dis_daging_ternak_list
        
        # Produksi dan Distribusi Susu Segar
        produksi = get_produksi_series_by_interval(db, 3)
        distribusi = get_distribusi_series_by_interval(db, 3)
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
        
        return responses
    
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": str(e)}
    )
    
 
    # ### Get sebaran_populasi_all ###
    # if  (tahun is None) and (provinsi is None) and \
    #     (kabupaten_kota is None) and (perah_pedaging is None) and \
    #     (jantan_betina is None) and (dewasa_anakan is None):
            
    #         query = (
    #             db.query(DimWaktu.tahun,
    #                      DimLokasi.provinsi,
    #                      func.sum(FactPopulasi.jumlah).label('total_populasi'))
    #             .join(DimWaktu, FactPopulasi.id_waktu == DimWaktu.id)
    #             .join(DimLokasi, FactPopulasi.id_lokasi == DimLokasi.id)
    #             .group_by(DimWaktu.tahun, DimLokasi.provinsi)
    #             .order_by(DimWaktu.tahun)
    #         )
            
    #         results = query.all()
            
    #         results_dict = {}
    #         lonlat_dict = {}
    #         for year, provinsi, total_populasi in results:
                
    #             if year not in results_dict:
    #                 results_dict[year] = {
    #                     'year': year,
    #                     'sebaran_populasi': []
    #                 }
                    
    #             if provinsi not in lonlat_dict:
    #                 lonlat_dict[provinsi] = {}
                    
    #                 query = text(
    #                     """
    #                         SELECT ST_AsText(ST_Centroid(region))
    #                         FROM dim_lokasi
    #                         WHERE
    #                             provinsi = :provinsi AND
    #                             kabupaten_kota IS NULL AND
    #                             kecamatan IS NULL
    #                     """
    #                 )
                    
    #                 lonlat = db.execute(query, {'provinsi': provinsi}).fetchone()
    #                 lonlat = lonlat[0]
                
    #             if total_populasi is not None:
    #                 results_dict[year]['sebaran_populasi'].append({
    #                     'region': lonlat, 
    #                     'title': provinsi,
    #                     'populasi': int(total_populasi)
    #                 })
                    
    #         responses['sebaran_populasi_all'] = list(results_dict.values())  
                
    # else:
        
    #     if provinsi:
    #         query = (
    #             db.query(DimWaktu.tahun,
    #                      DimLokasi.provinsi,
    #                      DimLokasi.kabupaten_kota,
    #                      FactPopulasi.tipe_ternak,
    #                      FactPopulasi.jenis_kelamin,
    #                      FactPopulasi.tipe_usia,
    #                      func.sum(FactPopulasi.jumlah).label('total_populasi'))
    #             .join(DimWaktu, FactPopulasi.id_waktu == DimWaktu.id)
    #             .join(DimLokasi, FactPopulasi.id_lokasi == DimLokasi.id)
    #         )
    #     else:
    #         query = (
    #             db.query(DimWaktu.tahun,
    #                      DimLokasi.provinsi,
    #                      FactPopulasi.tipe_ternak,
    #                      FactPopulasi.jenis_kelamin,
    #                      FactPopulasi.tipe_usia,
    #                      func.sum(FactPopulasi.jumlah).label('total_populasi'))
    #             .join(DimWaktu, FactPopulasi.id_waktu == DimWaktu.id)
    #             .join(DimLokasi, FactPopulasi.id_lokasi == DimLokasi.id)
    #         )
        
    #     if tahun:
    #         query = query.where(DimWaktu.tahun == tahun)
        
    #     if provinsi:
    #         query = query.where(DimLokasi.provinsi == provinsi)
        
    #     if kabupaten_kota:
    #         query = query.where(DimLokasi.kabupaten_kota == kabupaten_kota)
            
    #     if perah_pedaging:
    #         query = query.where(FactPopulasi.tipe_ternak == perah_pedaging)
            
    #     if jantan_betina:
    #         query = query.where(FactPopulasi.jenis_kelamin == jantan_betina)
            
    #     if dewasa_anakan:
    #         query = query.where(FactPopulasi.tipe_usia == dewasa_anakan)
        
    #     if provinsi:
    #         results = query.group_by(DimWaktu.tahun,
    #                                  DimLokasi.provinsi,
    #                                  DimLokasi.kabupaten_kota,
    #                                  FactPopulasi.tipe_ternak,
    #                                  FactPopulasi.jenis_kelamin,
    #                                  FactPopulasi.tipe_usia).all()
            
    #         results_dict = {}
    #         lonlat_dict = {}
    #         for year, provinsi, kabupaten_kota, tipe_ternak, jenis_kelamin, tipe_usia, total_populasi in results:
                    
    #             if year not in results_dict:
    #                 results_dict[year] = {
    #                     'year': year,
    #                     'sebaran_populasi': []
    #                 }
                    
    #             if kabupaten_kota not in lonlat_dict:
    #                 lonlat_dict[kabupaten_kota] = {}
                    
    #                 query = text(
    #                     """
    #                         SELECT ST_AsText(ST_Centroid(region))
    #                         FROM dim_lokasi
    #                         WHERE
    #                             kabupaten_kota = :kabupaten_kota AND
    #                             kecamatan IS NULL
    #                     """
    #                 )
    #                 lonlat = db.execute(query, {'kabupaten_kota': kabupaten_kota}).fetchone()
    #                 lonlat = lonlat[0]
                
    #             if total_populasi is not None:
    #                 results_dict[year]['sebaran_populasi'].append({
    #                     'region': lonlat,
    #                     'title': kabupaten_kota,
    #                     'populasi': int(total_populasi)
    #                 })
            
    #         responses['sebaran_populasi'] = list(results_dict.values())
            
    #     else:     
    #         results = query.group_by(DimWaktu.tahun,
    #                                  DimLokasi.provinsi,
    #                                  FactPopulasi.tipe_ternak,
    #                                  FactPopulasi.jenis_kelamin,
    #                                  FactPopulasi.tipe_usia).all()
            
    #         results_dict = {}
    #         lonlat_dict = {}
    #         for year, provinsi, tipe_ternak, jenis_kelamin, tipe_usia, total_populasi in results:
                        
    #             if year not in results_dict:
    #                 results_dict[year] = {
    #                     'year': year,
    #                     'sebaran_populasi': []
    #                 }
                    
    #             if provinsi not in lonlat_dict:
    #                 lonlat_dict[provinsi] = {}
                    
    #                 query = text(
    #                     """
    #                         SELECT ST_AsText(ST_Centroid(region))
    #                         FROM dim_lokasi
    #                         WHERE
    #                             provinsi = :provinsi AND
    #                             kabupaten_kota IS NULL AND
    #                             kecamatan IS NULL
    #                     """
    #                 )
    #                 lonlat = db.execute(query, {'provinsi': provinsi}).fetchone()
    #                 lonlat = lonlat[0]
                
    #             if total_populasi is not None:
    #                 results_dict[year]['sebaran_populasi'].append({
    #                     'region': lonlat,
    #                     'title': provinsi,
    #                     'populasi': int(total_populasi)
    #                 })  
                
    #         responses['sebaran_populasi'] = list(results_dict.values())
    
    
    # ### Get ringkasan_populasi ###
    # responses['ringkasan_populasi'] = {
    #     'jumlah_perah_dewasa': {
    #         'produksi': 0,
    #         'distribusi': 0
    #     },
    #     'jumlah_perah_anakan': {
    #         'produksi': 0,
    #         'distribusi': 0
    #     },
    #     'jumlah_pedaging_dewasa': {
    #         'produksi': 0,
    #         'distribusi': 0
    #     },
    #     'jumlah_pedaging_anakan': {
    #         'produksi': 0,
    #         'distribusi': 0
        
    #     }
    # }
    
    
    # ### Get table ###
    # responses['table'] = [
    #     {
    #         'wilayah': 'Aceh',
    #         'perah_dewasa_jantan': 0,
    #         'perah_dewasa_betina': 0,
    #         'perah_anakan_jantan': 0,
    #         'perah_anakan_betina': 0,
    #         'pedaging_dewasa_jantan': 0,
    #         'pedaging_dewasa_betina': 0,
    #         'pedaging_anakan_jantan': 0,
    #         'pedaging_anakan_betina': 0
    #     }
    # ]
    
    
    # return JSONResponse(
    #     status_code=status.HTTP_200_OK,
    #     content=responses
    # )