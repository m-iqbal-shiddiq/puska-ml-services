from typing import Optional
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from pydantic_settings import BaseSettings
from pydantic import Field, SecretStr
from sshtunnel import SSHTunnelForwarder


class Config(BaseSettings):
    # DB_USER: str = Field(default="postgres")
    # DB_PASS: SecretStr = Field()
    # DB_HOST: str = Field()
    # DB_PORT: int = Field(default=5432)
    # DB_NAME: str = Field(default="postgres")
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

    MODEL_PATH: str = Field(default="models")
    SCALER_PATH: str = Field(default="scalers")

    LOOK_BACK: int = Field(default=2)

    ID_SUSU: int = Field(default=3)

# CWD_PATH = os.path.join(os.path.dirname(__file__), os.pardir)

def session_factory(C: Config):
    if (C.SSH_TUNNEL_FLAG):
        
        tunnel = SSHTunnelForwarder(
            (C.SSH_HOST, C.SSH_PORT),
            ssh_username = C.SSH_USER,
            ssh_password = C.SSH_PASS.get_secret_value(),
            remote_bind_address = (C.DB_HOST, C.DB_PORT),
            local_bind_address = ('127.0.0.1', C.SSH_CLIENT_PORT)
        )
        tunnel.start()

    db_url = f"postgresql://{C.DB_USER}:{C.DB_PASS.get_secret_value()}@{C.DB_HOST}:{C.SSH_CLIENT_PORT if C.SSH_TUNNEL_FLAG else C.DB_PORT}/{C.DB_DB}"
    engine = create_engine(db_url)

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return SessionLocal

SessionLocal = session_factory(C=Config())