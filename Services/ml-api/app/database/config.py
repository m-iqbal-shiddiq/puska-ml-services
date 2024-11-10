from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field, SecretStr

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
    LOG_PATH: str = Field(alias="LOG_PATH")

    LOOK_BACK: int = Field(default=2)

    ID_SUSU: int = Field(default=3)
    
    IS_LOKAL: bool = Field(alias="IS_LOKAL")
    
    DB_USER_LOCAL: str = Field(alias="DB_USER_LOCAL")
    DB_PASS_LOCAL: SecretStr = Field(alias="DB_PASS_LOCAL")
    DB_HOST_LOCAL: str = Field(alias="DB_HOST_LOCAL")
    DB_PORT_LOCAL: int = Field(alias="DB_PORT_LOCAL")
    DB_NAME_LOCAL: str = Field(alias="DB_NAME_LOCAL")