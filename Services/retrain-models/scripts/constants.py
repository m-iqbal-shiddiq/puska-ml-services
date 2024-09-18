# DB connections
IS_LOKAL = False
DB_DATABASE = 'postgres'
DB_USER = 'postgres'
DB_PASSWORD ='123456'
DB_HOST = 'localhost'
DB_PORT = '5432'
DB_NAME = 'puska'
DB_TABLE = 'pred_susu'

# paths
RAW_PATH = '/Users/miqbalshdq/Documents/Projects/PUSKA-Full/Services/retrain-models/datasets/raw'
CLEANED_PATH = '/Users/miqbalshdq/Documents/Projects/PUSKA-Full/Services/retrain-models/datasets/cleaned'
PREDICTION_PATH = '/Users/miqbalshdq/Documents/Projects/PUSKA-Full/Services/retrain-models/datasets/predictions'
MODEL_PATH = '/Users/miqbalshdq/Documents/Projects/PUSKA-Full/Services/retrain-models/models'
SCALER_PATH = '/Users/miqbalshdq/Documents/Projects/PUSKA-Full/Services/retrain-models/scalers'

# threshold
SAVE_THRESHOLD = 100
TOTAL_DAY_TO_FILL_MISSING_VALUES = 7
TIMESTEP = 2
TRAIN_PERCENTAGE = 0.8