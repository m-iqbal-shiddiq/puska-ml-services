from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings

class Config(BaseSettings):
    # DB Config
    DB_USER: str = Field(default="postgres")
    DB_PASS: SecretStr = Field()
    DB_HOST: str = Field()
    DB_PORT: int = Field(default=5432)
    DB_NAME: str = Field(default="postgres")

    # Path Config
    MODEL_PATH: str = Field(default="models")
    SCALER_PATH: str = Field(default="scalers")

    # Timestamp
    LOOK_BACK: int = Field(default=7)

    # ID Jenis Produk = Susu
    ID_SUSU: int = Field(default=3)