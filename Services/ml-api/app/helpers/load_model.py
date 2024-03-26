import os
import tensorflow as tf


CWD_PATH = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)

def load_model():
    
    model_path = os.path.join(CWD_PATH, os.getenv('MODEL_PATH'))
    
    model_dict = {}
    
    for model in os.listdir(model_path):
        
        if model == '.DS_Store':
            continue
        
        model_dict[model.replace('.h5', '')] = tf.keras.models.load_model(
            os.path.join(model_path, model)
        )
        
    return model_dict
    