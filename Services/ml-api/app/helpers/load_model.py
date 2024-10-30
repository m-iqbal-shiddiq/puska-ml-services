import os
import pandas as pd
import tensorflow as tf


CWD_PATH = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)

def load_model(log_df, model_path: str):
    model_path = os.path.join(CWD_PATH, model_path)
    
    model_list = []
    for idx, row in log_df.iterrows():
        model_list.append({
            'id_lokasi': row['id_lokasi'],
            'id_unit_peternakan': row['id_unit_peternakan'],
            'model': tf.keras.models.load_model(
                os.path.join(model_path, row['model'])
            )
        })
        
    model_df = pd.DataFrame(model_list)
    
    return model_df
    