import os
import time
import numpy as np
import pandas as pd


from datetime import date, datetime, timedelta
from dotenv import load_dotenv
from fastapi import FastAPI, Depends, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy import and_
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field, validator
from typing import Optional
from typing_extensions import Annotated

import app.database.models as models

from app.database.connection import engine, SessionLocal
from app.database.models import *
from app.helpers.date_range import *
from app.helpers.load_model import *
from app.helpers.load_scaler import *
from app.validations.prediction import *



ENV_PATH = '.env'

load_dotenv(ENV_PATH)

# load model and scaler
model_dict = load_model()
scaler_dict = load_scaler()

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]



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
    

@app.post(
    path="/predict", 
    name="run_milk_prediction",
    responses={
        status.HTTP_200_OK: {
            'model': PredictionSuccessResponse,
            'description': "Prediction success"
        },
        status.HTTP_400_BAD_REQUEST: {
            'model': PredictionFailureResponse,
            'description': "There is bad request from client"
        },
        status.HTTP_404_NOT_FOUND: {
            'model': PredictionFailureResponse,
            'description': "Data not found"
        }
    }
)
async def create_prediction(
    predict_request: PredictionRequest, 
    db: Session = Depends(get_db)
):
    
    """
        Example Input:
        
        { \n
            "time_type": "daily", \n
            "id_waktu": "2023-04-01", \n
            "id_lokasi": 44156, \n
            "id_unit_peternakan": 44156, \n
        }
        
        ID Lokasi:
        - JAWA TIMUR : 44156
        - JAWA TIMUR - PROBOLINGGO : 47346
        
        ID Unit Ternak:
        - NYX Farm: 18
        - Prof Farm: 23
        
        Last Date:
        - NYX Farm: 28 Februari 2023
        - Prof Farm: 31 Maret 2023
        
    """
    
    start_time = time.time()
    predict_input = PredictionObj(**predict_request.model_dump())
    
    if predict_input.time_type == 'daily':
        # get data input for prediction
        input_data_list = []
        for id_waktu in predict_input.id_waktu_list:
            if predict_input.id_unit_peternakan is None:
                data = (
                    db.query(FactProduksi.jumlah_produksi)
                    .where(and_(FactProduksi.id_waktu == id_waktu,
                                FactProduksi.id_lokasi == predict_input.id_lokasi))
                    .all()
                )
            else:
                data = (
                    db.query(FactProduksi.jumlah_produksi)
                    .where(and_(FactProduksi.id_waktu == id_waktu,
                                FactProduksi.id_lokasi == predict_input.id_lokasi,
                                FactProduksi.id_unit_ternak == predict_input.id_unit_peternakan))
                    .all()
                )
            
            if len(data) == 0:
                if predict_input.id_unit_peternakan is None:
                    data_pred = (
                        db.query(PredSusu.prediction)
                        .where(and_(PredSusu.id_waktu == id_waktu,
                                    PredSusu.id_lokasi == predict_input.id_lokasi))
                        .first()
                    )
                else:
                    data_pred = (
                        db.query(PredSusu.prediction)
                        .where(and_(PredSusu.id_waktu == id_waktu,
                                    PredSusu.id_lokasi == predict_input.id_lokasi,
                                    PredSusu.id_unit_ternak == predict_input.id_unit_peternakan))
                        .first()
                    )
                if data_pred is None:
                    return JSONResponse(
                        status_code=status.HTTP_404_NOT_FOUND,
                        content={
                            'status': "error",
                            'type': "DATA_NOT_FOUND",
                            'message': "there is missing data for input prediction."
                        }
                    )
                else:
                    input_data_list.append([id_waktu, float(data_pred[0])])
            else:
                sum_data = 0
                for dt in data:
                    sum_data += dt[0]
                input_data_list.append([id_waktu, sum_data])
        
        # format input data 
        input_data_df = pd.DataFrame(input_data_list, columns=['id_tanggal', 'data'])
        
        try:
            model = model_dict[predict_input.model_name]
        except:
            model = None
            
        try:
            scaler = scaler_dict[predict_input.scaler_name]
        except:
            scaler = None
        
        if (model is None) or (scaler is None):
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={
                    'status': "error",
                    'type': "DATA_NOT_FOUND",
                    'message': "model or scaler not found."
                }
            )
        
        input_data_df['dt'] = scaler.transform(input_data_df['data'].values.reshape(-1, 1))
        input_data_model = input_data_df['data'].values.tolist()
        
        input_data_model = np.array(input_data_model).reshape(1, int(os.getenv('LOOK_BACK')))
        input_data_model = np.reshape(input_data_model, (input_data_model.shape[0], 1, input_data_model.shape[1]))
        
        pred_data = model.predict(input_data_model)
        pred_data = scaler.inverse_transform(pred_data)[0][0].item()
        pred_data = round(pred_data, 2)
        
        if predict_input.id_unit_peternakan is None:
            act_data = (
                db.query(FactProduksi.jumlah_produksi)
                .where(and_(FactProduksi.id_waktu == predict_input.id_waktu,
                            FactProduksi.id_lokasi == predict_input.id_lokasi))
                .first()
            )
        else:
            act_data = (
                db.query(FactProduksi.jumlah_produksi)
                .where(and_(FactProduksi.id_waktu == predict_input.id_waktu,
                            FactProduksi.id_lokasi == predict_input.id_lokasi,
                            FactProduksi.id_unit_ternak == predict_input.id_unit_peternakan))
                .first()
            )
            
        if act_data is None:
            mape = None
        else:
            act_data = act_data[0]
            mape = round(abs((act_data - pred_data) / act_data) * 100, 2)
        
        if predict_input.id_unit_peternakan is None:
            pred_in_database = (
                db.query(PredSusu)
                .where(and_(PredSusu.id_waktu == id_waktu,
                            PredSusu.id_lokasi == predict_input.id_lokasi))
                .first()
            )
        else:
            pred_in_database = (
                db.query(PredSusu)
                .where(and_(PredSusu.id_waktu == id_waktu,
                            PredSusu.id_lokasi == predict_input.id_lokasi,
                            PredSusu.id_unit_ternak == predict_input.id_unit_peternakan))
                .first()
            )
        
        if pred_in_database is None:
            latency = round(time.time() - start_time, 4)
            new_prediction = PredSusu(
                id_waktu=predict_input.id_waktu,
                id_lokasi=predict_input.id_lokasi,
                id_unit_ternak=predict_input.id_unit_peternakan,
                prediction=pred_data,
                mape=mape,
                latency=latency
            )
            
            db.add(new_prediction)
            db.commit()
            
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    'status': "success",
                    'prediction': pred_data,
                    'message': "add new prediction result."
                }
            )
            
        else:
            pred_in_database = float(pred_in_database.prediction)
            
            if (round(pred_data, 2) != round(pred_in_database, 2)):
                latency = round(time.time() - start_time, 4)
                
                update_data = (
                    db.query(PredSusu)
                    .where(and_(PredSusu.id_waktu == predict_input.id_waktu,
                                PredSusu.id_lokasi == predict_input.id_lokasi,
                                PredSusu.id_unit_ternak == predict_input.id_unit_peternakan))
                    .first()
                )
                
                update_data.prediction = pred_data
                update_data.latency = latency
                update_data.mape = mape
                db.commit()
                
                return JSONResponse(
                    status_code=status.HTTP_200_OK,
                    content={
                        'status': "success",
                        'prediction': pred_data,
                        'message': "update prediction in database."
                    }
                )
                
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    'status': "success",
                    'prediction': pred_data,
                    'message': "OK"
                }
            )
            
    else:
        # This is for weekly prediction
        pass
        return