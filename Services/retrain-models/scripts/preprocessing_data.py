import os
import pandas as pd

from constants import CLEANED_PATH, RAW_PATH, TOTAL_DAY_TO_FILL_MISSING_VALUES


def preprocess_data():
    
    print('Preprocessing data...')
    
    for filename in os.listdir(RAW_PATH):
    
        if not filename.endswith(".csv"):
            continue
        
        data_df = pd.read_csv(os.path.join(RAW_PATH, filename))
        
        data_df['date'] = pd.to_datetime(data_df['date'], format='%Y-%m-%d')
        
        date_range_series = pd.date_range(
            start=data_df['date'].min(),
            end=data_df['date'].max(),
            freq='D'
        )
        
        lost_date_list = date_range_series.difference(data_df['date']).tolist()
        
        # check if there is any lost date
        if len(lost_date_list) > 0:
            for date in lost_date_list:
                
                data_df.loc[len(data_df)] = {
                    'date': date,
                    'jumlah_produksi': 0
                }
                
            data_df = data_df.sort_values(by='date').reset_index(drop=True)

        # check if there is any missing value
        data_df = data_df.fillna(0)
        if len(data_df[data_df['jumlah_produksi'] == 0]) > 0:
            
            for index, row in data_df.iterrows():
                
                if row['jumlah_produksi'] != 0:
                    continue
                
                if index > (TOTAL_DAY_TO_FILL_MISSING_VALUES - 1):
                    start_index = index - TOTAL_DAY_TO_FILL_MISSING_VALUES
                    end_index = index - 1
                    
                    temp_df = data_df.loc[start_index:end_index, :]
                else:
                    temp_df = data_df.loc[:index, :]
                    
                avg = round(temp_df['jumlah_produksi'].mean(), 2)
                data_df.loc[index, 'jumlah_produksi'] = avg
        
        if data_df['id_unit_ternak'].unique().tolist()[0] == 0:
            data_df['id_unit_ternak'] = None 
                
        data_df.to_csv(os.path.join(CLEANED_PATH, filename), index=False)

if __name__ == '__main__':
    preprocess_data()