from fastapi import FastAPI

from app.routers import susu, ternak

# Base.metadata.create_all(bind=engine)

app = FastAPI(redirect_slashes=False)

app.include_router(susu.router, tags=['susu'])
app.include_router(ternak.router, tags=['ternak'])