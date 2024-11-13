from sqlalchemy import create_engine
from sshtunnel import SSHTunnelForwarder
from typing import Optional
from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings

class Config(BaseSettings):
    
    IS_LOKAL: bool = Field(alias="IS_LOKAL")
    
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
    
    DB_USER_LOCAL: str = Field(alias="DB_USER_LOCAL")
    DB_PASS_LOCAL: SecretStr = Field(alias="DB_PASS_LOCAL")
    DB_HOST_LOCAL: str = Field(alias="DB_HOST_LOCAL")
    DB_PORT_LOCAL: int = Field(alias="DB_PORT_LOCAL")
    DB_NAME_LOCAL: str = Field(alias="DB_NAME_LOCAL")
    
    DATASET_RAW_PATH: str = Field(alias="DATASET_RAW_PATH")
    DATASET_CLEANED_PATH: str = Field(alias="DATASET_CLEANED_PATH")
    DATASET_PREDICTION_PATH: str = Field(alias="DATASET_PREDICTION_PATH")
    LOG_PATH: str = Field(alias="LOG_PATH")
    MODEL_PATH: str = Field(alias="MODEL_PATH")
    SCALER_PATH: str = Field(alias="SCALER_PATH")
    
    SAVE_THRESHOLD: int = Field(default=100)
    TOTAL_DAY_TO_FILL_MISSING_VALUES: int = Field(default=7)
    TIMESTEP: int = Field(default=2)
    TRAIN_PERCENTAGE: float = Field(default=0.8)
    EPOCHS: int = Field(default=100)
    
    

def get_connection(C=Config()):
    
    if C.IS_LOKAL:
        database_url = f'postgresql://{C.DB_USER_LOCAL}:{C.DB_PASS_LOCAL.get_secret_value()}@{C.DB_HOST_LOCAL}:{C.DB_PORT_LOCAL}/{C.DB_NAME_LOCAL}'
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
  
    return engine