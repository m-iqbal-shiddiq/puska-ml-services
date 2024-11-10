import os
import pandas as pd

from database.connection import Config

def create_log(C=Config()):
    LOG_FILE_HEADER = ['id_lokasi', 'id_unit_peternakan', 'raw', 'cleaned', 'prediction', 'model', 'scaler', 'last_training_update']
    
    df = pd.DataFrame(columns=LOG_FILE_HEADER)
    df.to_csv(C.LOG_PATH, index=False)
    
def update_log(search_column, search_value, target_column, target_value, C=Config()):
    df = pd.read_csv(C.LOG_PATH)
    df.loc[df[search_column] == search_value, target_column] = target_value
    df.to_csv(C.LOG_PATH, index=False)