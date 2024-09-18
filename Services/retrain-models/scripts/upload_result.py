import os
import numpy as np
import pandas as pd

from sqlalchemy import create_engine
from sshtunnel import SSHTunnelForwarder
from typing import Optional
from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

from constants import DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_TABLE, DB_USER, IS_LOKAL, PREDICTION_PATH

class Config(BaseSettings):
    DB_USER: str = Field(alias="DB_USER")
    DB_PASS: SecretStr = Field(alias="DB_PASS")
    DB_HOST: str = Field(alias="DB_HOST")
    DB_PORT: int = Field(alias="DB_PORT")
    DB_DB: str = Field(alias="DB_DB")
    SSH_TUNNEL_FLAG: int = Field(alias="SSH_TUNNEL_FLAG", default=0)
    SSH_HOST: Optional[str] = Field(alias="SSH_HOST", default=None)
    SSH_USER: Optional[str] = Field(alias="SSH_USER", default=None)
    SSH_PORT: Optional[int] = Field(alias="SSH_PORT", default=None)
    SSH_PASS: Optional[SecretStr] = Field(alias="SSH_PASS", default=None)
    SSH_CLIENT_PORT: Optional[int] = Field(alias="SSH_CLIENT_PORT", default=None)

def upload_prediction(C=Config()):
    
    for filename in os.listdir(PREDICTION_PATH):
        
        if not filename.endswith('.csv'):
            continue
        
        print(f'Uploading {filename} to database...')
        
        if IS_LOKAL:
            database_url = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
            engine = create_engine(database_url)
        else:
            tunnel = SSHTunnelForwarder(
                (C.SSH_HOST, C.SSH_PORT),
                ssh_username = C.SSH_USER,
                ssh_password = C.SSH_PASS.get_secret_value(),
                remote_bind_address = (C.DB_HOST, C.DB_PORT),
                local_bind_address = ('127.0.0.1', C.SSH_CLIENT_PORT)
            )
            tunnel.start()
        
            database_url = f"postgresql://{C.DB_USER}:{C.DB_PASS.get_secret_value()}@{C.DB_HOST}:{C.SSH_CLIENT_PORT if C.SSH_TUNNEL_FLAG else C.DB_PORT}/{C.DB_DB}"
            engine = create_engine(database_url)
            
        data = pd.read_csv(os.path.join(PREDICTION_PATH, filename))
        
        data['id_waktu'] = data['id_waktu'].fillna(0).replace([np.inf, -np.inf], 0)
        data['id_waktu'] = data['id_waktu'].astype(int)
        data['id_lokasi'] = data['id_lokasi'].fillna(0).replace([np.inf, -np.inf], 0)
        data['id_lokasi'] = data['id_lokasi'].astype(int)
        data['id_unit_peternakan'] = data['id_unit_peternakan'].fillna(0).replace([np.inf, -np.inf], 0)
        data['id_unit_peternakan'] = data['id_unit_peternakan'].astype(int)
        
        data['prediction'] = data['prediction'].fillna(0).replace([np.inf, -np.inf], 0)
        data['prediction'] = data['prediction'].round(10)

        # data['latencity'] = data['latencity'].round(10)
        data['mape'] = data['mape'].fillna(0).replace([np.inf, -np.inf], 0)
        data['mape'] = data['mape'].round(10)
        
        data.to_sql(DB_TABLE, engine, if_exists='append', index=False)
        
        engine.dispose()

if __name__ == '__main__':
    upload_prediction()