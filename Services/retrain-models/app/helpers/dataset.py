import os
import numpy as np
import pandas as pd

from sqlalchemy import text

from database.connection import Config

def load_data(engine, C=Config()):
    
    log_df = pd.read_csv(C.LOG_PATH)
    logs = []
    
    print('Loading data from database...')
    
    query = """
        SELECT 
            waktu.id as id_waktu,
            waktu.hari as hari,
            waktu.bulan as bulan,
            waktu.tahun as tahun,
            lokasi.id as id_lokasi,
            lokasi.provinsi as provinsi,
            lokasi.kabupaten_kota as kabupaten_kota,
            unit_ternak.id as id_unit_peternakan,
            unit_ternak.nama_unit as nama_unit,
            fact.jumlah_produksi 
        FROM fact_produksi as fact
        JOIN dim_unit_peternakan as unit_ternak ON fact.id_unit_peternakan = unit_ternak.id
        JOIN dim_lokasi as lokasi ON fact.id_lokasi = lokasi.id
        JOIN dim_waktu as waktu ON fact.id_waktu = waktu.id
    """
    
    data_df = pd.read_sql(query, engine)
    
    data_df['tahun'] = data_df['tahun'].astype(int)
    data_df['bulan'] = data_df['bulan'].astype(int)
    data_df['hari'] = data_df['hari'].astype(int)
    data_df['date'] = pd.to_datetime(data_df['tahun'] * 10000 + data_df['bulan'] * 100 + data_df['hari'], format='%Y%m%d')
    
    data_df = data_df[['id_waktu', 'id_lokasi', 'id_unit_peternakan', 'date', 'provinsi', 'kabupaten_kota', 'nama_unit', 'jumlah_produksi']]
    time_df = data_df[['id_waktu', 'date']].copy().drop_duplicates().reset_index(drop=True)

    # Get provinces data
    provinces = data_df['provinsi'].unique().tolist()
    available_provinces = []
    for province in provinces:
        province_df = data_df[data_df['provinsi'] == province].copy()
        province_df_agg = province_df.copy().groupby('date')['jumlah_produksi'].mean().reset_index()
        province_df_agg = province_df_agg.sort_values('date')
        
        if len(province_df_agg) < C.SAVE_THRESHOLD:
            continue
        
        province_df_result = pd.merge(time_df, province_df_agg, on='date')
        
        query_province = f"""
            SELECT id FROM dim_lokasi
            WHERE
                provinsi = '{province}' AND
                kabupaten_kota IS NULL AND
                kecamatan IS NULL
        """
        
        id_provinsi = pd.read_sql(query_province, engine)
        id_provinsi = id_provinsi['id'].values[0]
        
        province_df_result['id_lokasi'] = id_provinsi
        province_df_result['id_waktu'] = province_df_result['id_waktu'].astype(int)
        province_df_result['id_unit_peternakan'] = None
        
        province_df_result = province_df_result[['id_waktu', 'id_lokasi', 'id_unit_peternakan', 'date', 'jumlah_produksi']]
        province_df_result = province_df_result.sort_values('date')
        province_df_result.to_csv(os.path.join(C.DATASET_RAW_PATH, f'{province}.csv'), index=False)
        
        available_provinces.append(province)
        logs.append({
            'id_lokasi': id_provinsi,
            'id_unit_peternakan': None,
            'raw': f'{province}.csv'
        })
    
    
    # Get regencies data
    if len(available_provinces) == 0:
        print('No regency data to load')
        return
    
    available_regencies = {}
    for province in available_provinces:
        regencies = data_df[data_df['provinsi'] == province]['kabupaten_kota'].unique().tolist()
        
        for regency in regencies:
            regency_df = data_df[(data_df['provinsi'] == province) & (data_df['kabupaten_kota'] == regency)].copy()
            regency_df_agg = regency_df.copy().groupby('date')['jumlah_produksi'].mean().reset_index()
            regency_df_agg = regency_df_agg.sort_values('date')
            
            if len(regency_df_agg) < C.SAVE_THRESHOLD:
                continue
            
            regency_df_result = pd.merge(time_df, regency_df_agg, on='date')
            
            query_regency = f"""
                SELECT id FROM dim_lokasi
                WHERE
                    provinsi = '{province}' AND
                    kabupaten_kota = '{regency}' AND
                    kecamatan IS NULL
            """
            
            id_regency = pd.read_sql(query_regency, engine)
            id_regency = id_regency['id'].values[0]
            
            regency_df_result['id_lokasi'] = id_regency
            regency_df_result['id_waktu'] = regency_df_result['id_waktu'].astype(int)
            regency_df_result['id_unit_peternakan'] = None
            
            regency_df_result = regency_df_result[['id_waktu', 'id_lokasi', 'id_unit_peternakan', 'date', 'jumlah_produksi']]
            regency_df_result = regency_df_result.sort_values('date')
            regency_df_result.to_csv(os.path.join(C.DATASET_RAW_PATH, f'{province}_{regency}.csv'), index=False)
            
            available_regencies[regency] = id_regency
            logs.append({
                'id_lokasi': id_regency,
                'id_unit_peternakan': None,
                'raw': f'{province}_{regency}.csv'
            })
            
    # Get units data
    if len(available_regencies) == 0:
        print('No unit peternakan data to load')
        return
            
    for regency, id_regency in available_regencies.items():
        units = data_df[data_df['kabupaten_kota'] == regency]['nama_unit'].unique().tolist()
        
        for unit in units:
            unit_df = data_df[(data_df['kabupaten_kota'] == regency) & (data_df['nama_unit'] == unit)].copy()
            unit_df_agg = unit_df.copy().groupby('date')['jumlah_produksi'].mean().reset_index()
            unit_df_agg = unit_df_agg.sort_values('date')
            
            if len(unit_df_agg) < C.SAVE_THRESHOLD:
                continue
            
            unit_df_result = pd.merge(time_df, unit_df_agg, on='date')
            
            query_unit = f"""
                SELECT id, id_lokasi FROM dim_unit_peternakan
                WHERE
                    nama_unit = '{unit}'
            """
            
            temp = pd.read_sql(query_unit, engine)
            id_unit = temp['id'].values[0]
            id_location = temp['id_lokasi'].values[0]
            
            unit_df_result['id_lokasi'] = id_location
            unit_df_result['id_waktu'] = unit_df_result['id_waktu'].astype(int)
            unit_df_result['id_unit_peternakan'] = id_unit
            
            unit_df_result = unit_df_result[['id_waktu', 'id_lokasi', 'id_unit_peternakan', 'date', 'jumlah_produksi']]
            unit_df_result = unit_df_result.sort_values('date')
            unit_df_result.to_csv(os.path.join(C.DATASET_RAW_PATH, f'{regency}_{unit}.csv'), index=False)
            
            logs.append({
                'id_lokasi': id_location,
                'id_unit_peternakan': id_unit,
                'raw': f'{regency}_{unit}.csv'
            })
    
    if len(logs) > 0:
        log_df = pd.concat([log_df, pd.DataFrame(logs)], ignore_index=True)
        log_df.to_csv(C.LOG_PATH, index=False)
        
def upload_data(engine, C=Config()):
    
    with engine.connect() as conn:
        conn.execute(text('TRUNCATE TABLE pred_susu'))
        conn.commit()
        
    print(f'Uploading prediction result to database...')
    for filename in os.listdir(C.DATASET_PREDICTION_PATH):
        if not filename.endswith('.csv'):
            continue
        
        data_df = pd.read_csv(os.path.join(C.DATASET_PREDICTION_PATH, filename))
        data_df['id_waktu'] = data_df['id_waktu'].fillna(0).replace([np.inf, -np.inf], 0)
        data_df['id_waktu'] = data_df['id_waktu'].astype(int)
        data_df['id_lokasi'] = data_df['id_lokasi'].fillna(0).replace([np.inf, -np.inf], 0)
        data_df['id_lokasi'] = data_df['id_lokasi'].astype(int)
        data_df['id_unit_peternakan'] = data_df['id_unit_peternakan'].fillna(0).replace([np.inf, -np.inf], 0)
        data_df['id_unit_peternakan'] = data_df['id_unit_peternakan'].astype(int)
        
        data_df['prediction'] = data_df['prediction'].round(2)
        data_df['mape'] = data_df['mape'].round(2)
        
        data_df.to_sql('pred_susu', engine, if_exists='append', index=False)
        engine.dispose()
        