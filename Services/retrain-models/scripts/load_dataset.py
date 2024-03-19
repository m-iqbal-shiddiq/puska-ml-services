import os
import pandas as pd

from sqlalchemy import create_engine

from constants import DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME, RAW_PATH, SAVE_THRESHOLD


def load_data():
    
    print('Loading data from database...')
    
    database_url = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    engine = create_engine(database_url)
    
    query = """
        SELECT 
            waktu.id as id_waktu,
            waktu.tanggal as tanggal,
            waktu.bulan as bulan,
            waktu.tahun as tahun,
            lokasi.id as id_lokasi,
            lokasi.provinsi as provinsi,
            lokasi.kabupaten_kota as kabupaten_kota,
            unit_ternak.id as id_unit_ternak,
            unit_ternak.nama_unit as nama_unit,
            fact.jumlah_produksi 
        FROM fact_produksi as fact
        JOIN dim_unit_ternak as unit_ternak ON fact.id_unit_ternak = unit_ternak.id
        JOIN dim_lokasi as lokasi ON fact.id_lokasi = lokasi.id
        JOIN dim_waktu as waktu ON fact.id_waktu = waktu.id
    """
    
    data_df = pd.read_sql(query, engine)
    
    data_df['date'] = pd.to_datetime(data_df['tahun'] * 10000 + data_df['bulan'] * 100 + data_df['tanggal'], format='%Y%m%d')
    data_df = data_df[['id_waktu', 'id_lokasi', 'id_unit_ternak',
                       'date', 'provinsi', 'kabupaten_kota', 
                       'nama_unit', 'jumlah_produksi']]
    
    provinsi_list = data_df['provinsi'].unique().tolist()

    for provinsi in provinsi_list:
        provinsi_df = data_df[data_df['provinsi'] == provinsi].copy()
        agg_provinsi_df = provinsi_df.groupby('date')['jumlah_produksi'].mean().reset_index()
        agg_provinsi_df = agg_provinsi_df.sort_values('date')
        
        if len(agg_provinsi_df) < SAVE_THRESHOLD:
            continue
        
        result_provinsi_df = pd.merge(provinsi_df, agg_provinsi_df, on='date', suffixes=('', '_mean'))
        result_provinsi_df = result_provinsi_df[['id_waktu', 'id_lokasi',
                                                'date', 'jumlah_produksi_mean']]
        result_provinsi_df.rename(columns={'jumlah_produksi_mean': 'jumlah_produksi'}, inplace=True)
        
        result_provinsi_df['id_waktu'] = result_provinsi_df['id_waktu'].astype(int)
        result_provinsi_df['id_lokasi'] = result_provinsi_df['id_lokasi'].astype(int)
        result_provinsi_df['id_unit_ternak'] = None

        result_provinsi_df.to_csv(os.path.join(RAW_PATH, f'{provinsi}.csv'), index=False)

        kabupaten_list = provinsi_df['kabupaten_kota'].unique().tolist()
        
        for kabupaten in kabupaten_list:
            kabupaten_df = provinsi_df[provinsi_df['kabupaten_kota'] == kabupaten].copy()
            agg_kabupaten_df = kabupaten_df.groupby('date')['jumlah_produksi'].mean().reset_index()
            agg_kabupaten_df = agg_kabupaten_df.sort_values('date')
            
            if len(agg_kabupaten_df) < SAVE_THRESHOLD:
                continue
            
            result_kabupaten_df = pd.merge(kabupaten_df, agg_kabupaten_df, on='date', suffixes=('', '_mean'))
            result_kabupaten_df = result_kabupaten_df[['id_waktu', 'id_lokasi',
                                                    'date', 'jumlah_produksi_mean']]
            result_kabupaten_df.rename(columns={'jumlah_produksi_mean': 'jumlah_produksi'}, inplace=True)
            
            result_kabupaten_df['id_waktu'] = result_kabupaten_df['id_waktu'].astype(int)
            result_kabupaten_df['id_lokasi'] = result_kabupaten_df['id_lokasi'].astype(int)
            result_kabupaten_df['id_unit_ternak'] = None
            
            result_kabupaten_df.to_csv(os.path.join(RAW_PATH, f'{provinsi}_{kabupaten}.csv'), index=False)
        
            unit_list = kabupaten_df['nama_unit'].unique().tolist()
            
            for unit in unit_list:
                unit_df = kabupaten_df[kabupaten_df['nama_unit'] == unit].copy()
                agg_unit_df = unit_df.groupby('date')['jumlah_produksi'].mean().reset_index()
                agg_unit_df = agg_unit_df.sort_values('date')
                
                if len(agg_unit_df) < SAVE_THRESHOLD:
                    continue
                
                result_unit_df = pd.merge(unit_df, agg_unit_df, on='date', suffixes=('', '_mean'))
                result_unit_df = result_unit_df[['id_waktu', 'id_lokasi', 'id_unit_ternak',
                                                'date', 'jumlah_produksi_mean']]
                result_unit_df.rename(columns={'jumlah_produksi_mean': 'jumlah_produksi'}, inplace=True)
                
                result_unit_df['id_waktu'] = result_unit_df['id_waktu'].astype(int)
                result_unit_df['id_lokasi'] = result_unit_df['id_lokasi'].astype(int)
                result_unit_df['id_unit_ternak'] = result_unit_df['id_unit_ternak'].astype(int)
                
                result_unit_df.to_csv(os.path.join(RAW_PATH, f'{provinsi}_{kabupaten}_{unit}.csv'), index=False)

if __name__ == '__main__':
    load_data()