from pydantic import BaseModel, Field, validator


class PredictionRequest(BaseModel):
    time_type: str = Field(...,
                           description="Time type for prediction",
                           examples=["daily", "weekly"])
    id_waktu: int = Field(..., 
                          description="Date for prediction",
                          examples=[453])
    id_lokasi: int = Field(...,
                           description="Location ID for prediction",
                           examples=[47346])
    id_unit_peternakan: int = Field(None,
                                    description="Unit Peternakan ID for prediction",
                                    examples=[23])
    
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
    
    def __init__(
        self,
        time_type: str,
        id_waktu: int,
        id_lokasi: int,
        id_unit_peternakan: int,
        look_back: int =  2,
    ):
        
        self.time_type = time_type
        self.id_waktu = id_waktu
        self.id_lokasi = id_lokasi
        self.id_unit_peternakan = id_unit_peternakan
        
        key_name_list = [str(self.id_lokasi)]
        
        if self.id_unit_peternakan is not None:
            key_name_list.append(str(self.id_unit_peternakan))
        
        # if regency is not None:
        #     self.regency = regency
        #     folder_name_list.append(self.regency)
        # else:
        #     self.regency = None
        
        # if unit is not None:
        #     self.unit = unit
        #     folder_name_list.append(self.unit)
        # else:
        #     self.unit = None
        
        self.model_name = f"{'_'.join(key_name_list)}"
        self.scaler_name = f"{'_'.join(key_name_list)}"
        
        if self.time_type == 'daily':
            start_date = self.id_waktu - look_back
            end_date = self.id_waktu - 1
            
            self.id_waktu_list = list(range(start_date, end_date + 1))
       
        else:
            self.start_week = None
            self.end_week = None