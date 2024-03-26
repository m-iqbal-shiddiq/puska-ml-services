import os
from datetime import datetime, timedelta
from pydantic import BaseModel, Field, validator


class PredictionRequest(BaseModel):
    date: str = Field(..., 
                      description="Date for prediction",
                      examples=["2023-12-06"])
    time_type: str = Field(...,
                           description="Time type for prediction",
                           examples=["daily", "weekly"])
    province: str = Field(...,
                          description="Province for prediction",
                          examples=["Jawa Timur"])
    regency: str = Field(None,
                         description="Regency for prediction",
                         examples=["Probolinggo"])
    unit: str = Field(None,
                      description="Unit for prediction",
                      examples=["NYX Farm"])
    
    @validator('date')
    def validate_date(cls, value):
        try:
            datetime.strptime(value, '%Y-%m-%d')
        except:
            raise ValueError('date must be in YYYY-MM-DD format')
        return value
    
    @validator('time_type')
    def validate_time_type(cls, value):
        if (value.lower() not in ['daily', 'weekly']):
            raise ValueError('time_type must be daily or weekly')
        return value.lower()
    
    
class PredictionSuccessResponse(BaseModel):
    status: str
    message: str
    
class PredictionFailureResponse(BaseModel):
    status: str
    type: str
    message: str
    
class PredictionObj():
    
    def __init__(self, date, time_type, province, regency, unit):
        
        self.date = datetime.strptime(date, '%Y-%m-%d')
        self.time_type = time_type
        
        self.province = province
        folder_name_list = [self.province]
        
        if regency is not None:
            self.regency = regency
            folder_name_list.append(self.regency)
        else:
            self.regency = None
        
        if unit is not None:
            self.unit = unit
            folder_name_list.append(self.unit)
        else:
            self.unit = None
        
        self.model_name = f"{'_'.join(folder_name_list)}"
        self.scaler_name = f"{'_'.join(folder_name_list)}"
        
        if self.time_type == 'daily':
            self.start_date = self.date - timedelta(int(os.getenv('LOOK_BACK')))     
            self.end_date = self.date - timedelta(1)
       
        else:
            self.start_week = None
            self.end_week = None