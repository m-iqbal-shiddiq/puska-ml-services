import os
import pandas as pd

from database.connection import Config
from helpers.log import update_log

def clean_data(engine, C=Config()):
    
    print('Cleaning data...')
    
    for filename in os.listdir(C.DATASET_RAW_PATH):
        if not filename.endswith(".csv"):
            continue
        
        data_df = pd.read_csv(os.path.join(C.DATASET_RAW_PATH, filename))
        data_df['date'] = pd.to_datetime(data_df['date'], format='%Y-%m-%d')
        
        date_ranges = pd.date_range(start=data_df['date'].min(), end=data_df['date'].max(), freq='D')
        lost_dates = date_ranges.difference(data_df['date']).tolist()
        
        # check if there is any lost date
        if len(lost_dates) > 0:
            id_location = data_df['id_lokasi'].unique().tolist()[0]
            id_unit_peternakan = data_df['id_unit_peternakan'].unique().tolist()[0]
            for date in lost_dates:
                
                query_time = f"""
                    SELECT * 
                    FROM dim_waktu
                    WHERE tanggal = '{date.date()}'
                """
                
                id_time = pd.read_sql(query_time, engine)
                id_time = id_time['id'].values[0]
                
                data_df.loc[len(data_df)] = {
                    'id_waktu': id_time,
                    'id_lokasi': id_location,
                    'id_unit_peternakan': id_unit_peternakan,
                    'date': date, 
                    'jumlah_produksi': None
                }

            data_df = data_df.sort_values(by='date').reset_index(drop=True)

        # check if there is any missing value
        if data_df['jumlah_produksi'].isna().sum() > 0:
            for index, row in data_df.iterrows():
                if not pd.isnull(row['jumlah_produksi']):
                    continue
        
                if index > (C.TOTAL_DAY_TO_FILL_MISSING_VALUES - 1):
                    start_index = index - C.TOTAL_DAY_TO_FILL_MISSING_VALUES
                    end_index = index - 1
                    
                    temp_df = data_df.loc[start_index:end_index, :]
                else:
                    temp_df = data_df.loc[:index, :]
                    
                avg = round(temp_df['jumlah_produksi'].mean(), 2)
                data_df.loc[index, 'jumlah_produksi'] = avg
                
        data_df['jumlah_produksi'] = data_df['jumlah_produksi'].round(2)
        data_df.to_csv(os.path.join(C.DATASET_CLEANED_PATH, filename), index=False)
        
        update_log('raw', filename, 'cleaned', filename)
            