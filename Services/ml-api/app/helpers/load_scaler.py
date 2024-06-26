import joblib
import os


CWD_PATH = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)

def load_scaler(scaler_path: str):
    
    scaler_path = os.path.join(CWD_PATH, scaler_path)
    
    scaler_dict = {}
    
    for scaler in os.listdir(scaler_path):
        
        if scaler == '.DS_Store':
            continue
        
        scaler_dict[scaler.replace('.pkl', '')] = joblib.load(
            os.path.join(scaler_path, scaler)
        )
        
    return scaler_dict
        