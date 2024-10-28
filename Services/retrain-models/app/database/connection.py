from sqlalchemy import create_engine
from sshtunnel import SSHTunnelForwarder
from typing import Optional
from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings

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
    
    DB_USER_LOCAL: str = Field(alias="DB_USER_LOCAL")
    DB_PASS_LOCAL: SecretStr = Field(alias="DB_PASS_LOCAL")
    DB_HOST_LOCAL: str = Field(alias="DB_HOST_LOCAL")
    DB_PORT_LOCAL: int = Field(alias="DB_PORT_LOCAL")
    DB_NAME_LOCAL: str = Field(alias="DB_NAME_LOCAL")

def get_connection(C=Config()):
    
    IS_LOKAL = False
    
    if IS_LOKAL:
        database_url = f'postgresql://{C.DB_USER_LOCAL}:{C.DB_PASS_LOCAL}@{C.DB_HOST_LOCAL}:{C.DB_PORT_LOCAL}/{C.DB_NAME_LOCAL}'
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