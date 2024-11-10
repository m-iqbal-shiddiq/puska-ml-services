from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from sshtunnel import SSHTunnelForwarder

from app.database.config import Config
    
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