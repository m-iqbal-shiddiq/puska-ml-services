import os
import pandas as pd

from sqlalchemy import create_engine

from constants import DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_TABLE, DB_USER, PREDICTION_PATH

def upload_prediction():
    
    for filename in os.listdir(PREDICTION_PATH):
        
        if not filename.endswith('.csv'):
            continue
        
        print(f'Uploading {filename} to database...')
        
        database_url = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
        engine = create_engine(database_url)
        
        data = pd.read_csv(os.path.join(PREDICTION_PATH, filename))
        
        data.to_sql(DB_TABLE, engine, if_exists='append', index=False)
        
        engine.dispose()

if __name__ == '__main__':
    upload_prediction()