from fastapi import APIRouter

from app.database.connection import SessionLocal


router = APIRouter(redirect_slashes=False)

def get_db():   
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        

@router.get(path='/')
async def get_susu_data():
    print('Masuk ke get_susu_data')
