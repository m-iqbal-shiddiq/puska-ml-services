from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.routers import prediction


app = FastAPI()
app.include_router(prediction.router, tags=["predict"])


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            'status': "error",
            'type': "REQUEST_VALIDATION_ERROR",
            'message': f"{exc.errors()[0]['loc'][1]}: {exc.errors()[0]['msg']}"
        }
    )

@app.exception_handler(500)
async def internal_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
        content={
            'status': "error",
            'type': "INTERNAL_SERVER_ERROR",
            'message': "something went wrong."        
        }
    )
