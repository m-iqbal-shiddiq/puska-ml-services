import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sshtunnel import SSHTunnelForwarder


is_local = False

CWD_PATH = os.path.join(os.path.dirname(__file__), os.pardir)
ENV_PATH = os.path.join(CWD_PATH, '.env')

load_dotenv(ENV_PATH)

if is_local:
    db_host = os.getenv('DB_HOST_LOCAL')
    db_port = int(os.getenv('DB_PORT_LOCAL'))
    db_name = os.getenv('DB_NAME_LOCAL')
    db_user = os.getenv('DB_USER_LOCAL')
    db_pass = os.getenv('DB_PASS_LOCAL')
    
    used_port = db_port
else:
    db_host = os.getenv('DB_HOST')
    db_port = int(os.getenv('DB_PORT'))
    db_name = os.getenv('DB_NAME')
    db_user = os.getenv('DB_USER')
    db_pass = os.getenv('DB_PASS')

    ssh_host = os.getenv('SSH_HOST')
    ssh_user = os.getenv('SSH_USERNAME')
    ssh_port = int(os.getenv('SSH_PORT'))
    ssh_pass = os.getenv('SSH_PASSWORD')

    tunnel = SSHTunnelForwarder(
        (ssh_host, ssh_port),
        ssh_username=ssh_user,
        ssh_password=ssh_pass,
        remote_bind_address=(db_host, db_port),
        local_bind_address=('localhost', 5433)
    )

    tunnel.start()

    used_port = tunnel.local_bind_port

db_url = f"postgresql://{db_user}:{db_pass}@{db_host}:{used_port}/{db_name}"
engine = create_engine(db_url)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)