from fastapi import FastAPI

from app.routers import lokasi, susu, ternak, filter
from fastapi.middleware.cors import CORSMiddleware

# Base.metadata.create_all(bind=engine)

app = FastAPI(redirect_slashes=False)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"], 
)

app.include_router(susu.router, tags=['susu'])
app.include_router(lokasi.router, tags=['lokasi'])
app.include_router(ternak.router, tags=['ternak'])
app.include_router(filter.router, tags=['filter'])