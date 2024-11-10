import time
import numpy as np
import pandas as pd

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy import func
from sqlalchemy.orm import Session
from typing_extensions import Annotated

from app.database.config import Config
from app.database.connection import SessionLocal
from app.database.models import DimWaktu, DimLokasi, DimUnitPeternakan, FactProduksi, FactProduksiStream, PredSusu
from app.helpers.load_model import load_model
from app.helpers.load_scaler import load_scaler
from app.schemas.prediction import PredictionRequest, PredictionSuccessResponse, PredictionFailureResponse


CONFIG = Config()

# load model and scaler
log_df = pd.read_csv('./train-log.csv')
log_df = log_df[['id_lokasi', 'id_unit_peternakan', 'model', 'scaler']]

MODEL_DF = load_model(log_df, CONFIG.MODEL_PATH)
MODEL_DF = MODEL_DF.replace({np.nan: None})

SCALER_DF = load_scaler(log_df, CONFIG.SCALER_PATH)
SCALER_DF = SCALER_DF.replace({np.nan: None})

router = APIRouter(redirect_slashes=False)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]


class PredictionObj():
    
    def __init__(self, time_type: str, id_waktu: int, id_lokasi: int, id_unit_peternakan: int, look_back: int =  2):
        
        self.time_type = time_type
        self.id_waktu = id_waktu
        self.id_lokasi = id_lokasi
        self.id_unit_peternakan = id_unit_peternakan
        
        if self.time_type == 'daily':
            start_date = self.id_waktu - look_back
            end_date = self.id_waktu - 1
            
            self.id_waktu_list = list(range(start_date, end_date + 1))


def get_data_from_database(model, db, input_data, is_predict=False):
    
    if is_predict:
        sub_query = (
            db.query(DimWaktu.id,
                    DimWaktu.tanggal,
                    model.prediction)
            .join(DimWaktu, DimWaktu.id == model.id_waktu)
            .join(DimLokasi, DimLokasi.id == model.id_lokasi)
            .join(DimUnitPeternakan, DimUnitPeternakan.id == model.id_unit_peternakan)
            .where(DimWaktu.id.in_(input_data.id_waktu_list))
        ) 
    else:
        sub_query = (
            db.query(DimWaktu.id,
                    DimWaktu.tanggal,
                    model.jumlah_produksi)
            .join(DimWaktu, DimWaktu.id == model.id_waktu)
            .join(DimLokasi, DimLokasi.id == model.id_lokasi)
            .join(DimUnitPeternakan, DimUnitPeternakan.id == model.id_unit_peternakan)
            .where(DimWaktu.id.in_(input_data.id_waktu_list))
        ) 
    
    # Check Location
    location = (
        db.query(DimLokasi.provinsi,
                 DimLokasi.kabupaten_kota,
                 DimLokasi.kecamatan)
        .where(DimLokasi.id == input_data.id_lokasi)
    ).first()
    
    if location is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                'status': "error",
                'type': "NOT_FOUND",
                'message': "Location not found."
            }
        )
    
    if (location[1] is None) and (location[2] is None):
        location_ids = (
            db.query(DimLokasi.id)
            .where(DimLokasi.provinsi == location[0])
        ).all()
        
        location_ids = [location_id[0] for location_id in location_ids]
        
    elif (location[2] is None) and (input_data.id_unit_peternakan is None):
        location_ids = (
            db.query(DimLokasi.id)
            .where(DimLokasi.provinsi == location[0])
            .where(DimLokasi.kabupaten_kota == location[1])
        ).all()
        
        location_ids = [location_id[0] for location_id in location_ids]
    else:
        location_ids = [input_data.id_lokasi]
    
    sub_query = sub_query.where(DimLokasi.id.in_(location_ids))
    
    if input_data.id_unit_peternakan:
        sub_query = sub_query.where(DimUnitPeternakan.id == input_data.id_unit_peternakan)
        
    sub_query = sub_query.subquery()

    if is_predict:
        query = (
            db.query(sub_query.c.id,
                    sub_query.c.tanggal,
                    func.round(func.avg(sub_query.c.prediction), 2).label('jumlah_produksi'))
            .group_by(sub_query.c.id, sub_query.c.tanggal)
            .order_by(sub_query.c.id)
        )
    else:
        query = (
            db.query(sub_query.c.id,
                     func.round(func.avg(sub_query.c.jumlah_produksi), 2).label('jumlah_produksi'))
            .group_by(sub_query.c.id, sub_query.c.tanggal)
            .order_by(sub_query.c.id)
        )
    
    result = query.all()
    
    if is_predict:
        result = [[data[0], data[2]] for data in result]
    else:
        result = [[data[0], float(data[1])] for data in result]
    
    return result
    
    
def get_actual_data_from_database(model, db, input_data):
    sub_query = (
        db.query(model.id_waktu, 
                 model.jumlah_produksi)
        .where(model.id_waktu == input_data.id_waktu)
    )
    
    location = (
        db.query(DimLokasi.provinsi,
                 DimLokasi.kabupaten_kota,
                 DimLokasi.kecamatan)
        .where(DimLokasi.id == input_data.id_lokasi)
    ).first()
    
    if location is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                'status': "error",
                'type': "NOT_FOUND",
                'message': "Location not found."
            }
        )
    
    if (location[1] is None) and (location[2] is None):
        location_ids = (
            db.query(DimLokasi.id)
            .where(DimLokasi.provinsi == location[0])
        ).all()
        
        location_ids = [location_id[0] for location_id in location_ids]
        
    elif (location[2] is None) and (input_data.id_unit_peternakan is None):
        location_ids = (
            db.query(DimLokasi.id)
            .where(DimLokasi.provinsi == location[0])
            .where(DimLokasi.kabupaten_kota == location[1])
        ).all()
        
        location_ids = [location_id[0] for location_id in location_ids]
        
    else:
        location_ids = [input_data.id_lokasi]
        
    sub_query = sub_query.where(model.id_lokasi.in_(location_ids))
    
    if input_data.id_unit_peternakan:
        sub_query = sub_query.where(model.id_unit_peternakan == input_data.id_unit_peternakan)
        
    sub_query = sub_query.subquery()
    
    query = (
        db.query(sub_query.c.id_waktu,
                 func.round(func.avg(sub_query.c.jumlah_produksi), 2).label('jumlah_produksi'))
        .group_by(sub_query.c.id_waktu)
    )
    
    result = query.all()
    
    if len(result) > 0:
        return float(result[0][1])
    else:
        return None
    

@router.post(
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
async def create_prediction(predict_request: PredictionRequest, db: Session = Depends(get_db)):
    try:
        start_time = time.time()
        predict_input = PredictionObj(**predict_request.model_dump())

        if predict_input.time_type == 'daily':   
            
            data_input_final = []
            
            data_input_found = get_data_from_database(FactProduksiStream, db, predict_input)
            for data in data_input_found:
                predict_input.id_waktu_list.remove(data[0])
                data_input_final.append(data)
                
            if len(predict_input.id_waktu_list) > 0:
                data_input_found = get_data_from_database(FactProduksi, db, predict_input)
                for data in data_input_found:
                    predict_input.id_waktu_list.remove(data[0])
                    data_input_final.append(data)
            
            if len(predict_input.id_waktu_list) > 0:
                data_input_found = get_data_from_database(PredSusu, db, predict_input, is_predict=True)
                for data in data_input_found:
                    predict_input.id_waktu_list.remove(data[0])
                    data_input_final.append(data)
             
            if len(predict_input.id_waktu_list) > 0:
                return JSONResponse(
                    status_code=status.HTTP_404_NOT_FOUND,
                    content={
                        'status': "error",
                        'type': "NOT_FOUND",
                        'message': "Data not found."
                    }
                )
                
            input_data_df = pd.DataFrame(data_input_final, columns=['id_waktu', 'jumlah_produksi'])
            input_data_df = input_data_df.sort_values(by='id_waktu')
            
            # Get Model
            if predict_input.id_unit_peternakan:
                model = MODEL_DF.loc[(MODEL_DF['id_lokasi'] == predict_input.id_lokasi) & (MODEL_DF['id_unit_peternakan'] == predict_input.id_unit_peternakan)]['model']
            else:   
                model = MODEL_DF.loc[(MODEL_DF['id_lokasi'] == predict_input.id_lokasi) & (MODEL_DF['id_unit_peternakan'].isnull())]['model']
            if len(model) > 0:
                model = model.values[0]
            else:
                return JSONResponse(
                    status_code=status.HTTP_404_NOT_FOUND,
                    content={
                        'status': "error",
                        'type': "NOT_FOUND",
                        'message': "Model not found."
                    }
                )
            
            # Get Scaler
            if predict_input.id_unit_peternakan:
                scaler = SCALER_DF.loc[(SCALER_DF['id_lokasi'] == predict_input.id_lokasi )& (SCALER_DF['id_unit_peternakan'] == predict_input.id_unit_peternakan)]['scaler']
            else:
                scaler = SCALER_DF.loc[(SCALER_DF['id_lokasi'] == predict_input.id_lokasi) & (SCALER_DF['id_unit_peternakan'].isnull())]['scaler']
            if len(scaler) > 0:
                scaler = scaler.values[0]
            else:
                return JSONResponse(
                    status_code=status.HTTP_404_NOT_FOUND,
                    content={
                        'status': "error",
                        'type': "NOT_FOUND",
                        'message': "Scaler not found."
                    }
                )
                
            input_data_df['dt'] = scaler.transform(input_data_df['jumlah_produksi'].values.reshape(-1, 1))
            
            input_predict = input_data_df['dt'].values
            input_predict = np.array(input_predict).reshape(1, 1, input_predict.shape[0])
            
            output_predict = model.predict(input_predict)
            output_predict = scaler.inverse_transform(output_predict)[0][0].item()
            output_predict = round(output_predict, 3)
            
            # Get actual data for calculate mape
            actual_data = get_actual_data_from_database(FactProduksiStream, db, predict_input)
            
            if actual_data is None:
                actual_data = get_actual_data_from_database(FactProduksi, db, predict_input)
                
            if actual_data is None:
                mape = None
            else:
                mape = round(abs(actual_data - output_predict) / actual_data * 100, 2)
            
            
            # Save to database
            query = (
                db.query(PredSusu.prediction)
                .where(PredSusu.id_waktu == predict_input.id_waktu)
                .where(PredSusu.id_lokasi == predict_input.id_lokasi)
            )
            
            if predict_input.id_unit_peternakan:
                query = query.where(PredSusu.id_unit_peternakan == predict_input.id_unit_peternakan)
                
            prediction_in_db = query.first()
            
            if prediction_in_db:
                prediction_in_db = float(prediction_in_db[0])
                are_not_equal = abs(round(prediction_in_db, 3) - round(output_predict, 3)) > 1e-9
                if are_not_equal:
                    latency = round(time.time() - start_time, 4)
                    
                    query = (
                        db.query(PredSusu)
                        .where(PredSusu.id_waktu == predict_input.id_waktu)
                        .where(PredSusu.id_lokasi == predict_input.id_lokasi)
                    )
                    
                    if predict_input.id_unit_peternakan:
                        query = query.where(PredSusu.id_unit_peternakan == predict_input.id_unit_peternakan)
                        
                    update_prediction = query.first()
                    update_prediction.prediction = output_predict
                    update_prediction.mape = mape
                    update_prediction.latency = latency
                    
                    db.commit()
                    
                    return JSONResponse(
                        status_code=status.HTTP_200_OK,
                        content={
                            'status': "success",
                            'prediction': output_predict,
                            'message': "update prediction result"
                        }
                    )
                else:
                    return JSONResponse(
                        status_code=status.HTTP_200_OK,
                        content={
                            'status': "success",
                            'prediction': output_predict,
                            'message': "OK"
                        }
                    )
                    
            else:
                latency = round(time.time() - start_time, 4)
                new_prediction = PredSusu(
                    id_waktu=predict_input.id_waktu,
                    id_lokasi=predict_input.id_lokasi,
                    id_unit_peternakan=predict_input.id_unit_peternakan,
                    prediction=output_predict,
                    mape=mape,
                    latency=latency
                )
                
                db.add(new_prediction)
                db.commit()
                
                return JSONResponse(
                    status_code=status.HTTP_200_OK,
                    content={
                        'status': "success",
                        'prediction': output_predict,
                        'message': "add new prediction result"
                    }
                )
            
                
        else:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    'status': "error",
                    'type': "BAD_REQUEST",
                    'message': "time_type must be 'daily'."
                }
            )
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                'status': "error",
                'type': "INTERNAL_SERVER_ERROR",
                'message': e
            }
        )
        
