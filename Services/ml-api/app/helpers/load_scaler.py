import os
import joblib
import pandas as pd

CWD_PATH = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)

def load_scaler(log_df, scaler_path: str):
    scaler_path = os.path.join(CWD_PATH, scaler_path)
    
    scaler_list = []
    for idx, row in log_df.iterrows():
        scaler_list.append({
            'id_lokasi': row['id_lokasi'],
            'id_unit_peternakan': row['id_unit_peternakan'],
            'scaler': joblib.load(
                os.path.join(scaler_path, row['scaler'])
            )
        })
        
    scaler_df = pd.DataFrame(scaler_list)
        
    return scaler_df
        