import requests
import numpy as np
import pandas as pd

from datetime import datetime, timedelta
from sqlalchemy import create_engine, text
from sshtunnel import SSHTunnelForwarder
from app.database.config import Config

C = Config()


def get_connection():
    if C.IS_LOKAL:
        database_url = f'postgresql://{C.DB_USER_LOCAL}:{C.DB_PASS_LOCAL}@{C.DB_HOST_LOCAL}:{C.DB_PORT_LOCAL}/{C.DB_NAME_LOCAL}'
        engine = create_engine(database_url)
    else:
        tunnel = SSHTunnelForwarder(
            (C.SSH_HOST, C.SSH_PORT),
            ssh_username = C.SSH_USER,
            ssh_password = C.SSH_PASS.get_secret_value(),
            remote_bind_address = (C.DB_HOST, C.DB_PORT),
            local_bind_address = ('127.0.0.1', C.SSH_CLIENT_PORT + 1)
        )
        tunnel.start()
    
        database_url = f"postgresql://{C.DB_USER}:{C.DB_PASS.get_secret_value()}@{C.DB_HOST}:{C.SSH_CLIENT_PORT if C.SSH_TUNNEL_FLAG else C.DB_PORT}/{C.DB_DB}"
        engine = create_engine(database_url)
        
    return engine


def main():
    
    URL = "http://127.0.0.1:8000/predict"
    
    engine = get_connection()
    
    with engine.connect() as connection:
        tanggal = (datetime.now() - timedelta(1)).strftime("%Y-%m-%d")
        query = text("SELECT id FROM dim_waktu WHERE tanggal = :tanggal")
        result = connection.execute(query, {"tanggal": tanggal})
    
        row = result.fetchone()
        
        id_waktu = row[0]
        
    train_log_df = pd.read_csv(C.LOG_PATH)
    train_log_df = train_log_df[['id_lokasi', 'id_unit_peternakan', 'model', 'scaler']]
    train_log_df = train_log_df.replace({np.nan: None})

    for idx, row in train_log_df.iterrows():
        data = {
            'time_type': 'daily',
            'id_waktu': id_waktu,
            'id_lokasi': row['id_lokasi'],
            'id_unit_peternakan': row['id_unit_peternakan']
        }
        response = requests.post(URL, json=data)
        print(response.json())
        
main()