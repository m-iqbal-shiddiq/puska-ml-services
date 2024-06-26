import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.config import Config

CWD_PATH = os.path.join(os.path.dirname(__file__), os.pardir)
CONFIG = Config()
# ENV_PATH = os.path.join(CWD_PATH, '.env')

# load_dotenv(ENV_PATH)

# db_user = os.getenv('DB_USER')
# db_pass = os.getenv('DB_PASS')
# db_host = os.getenv('DB_HOST')
# db_name = os.getenv('DB_NAME')


SQLALCHEMY_DATABASE_URL = f"postgresql://{CONFIG.DB_USER}:{CONFIG.DB_PASS.get_secret_value()}@{CONFIG.DB_HOST}/{CONFIG.DB_NAME}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()