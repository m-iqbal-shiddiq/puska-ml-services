from database.connection import get_connection
from helpers.dataset import load_data, upload_data
from helpers.log import create_log
from helpers.modelling import train_data
from helpers.preprocessing import clean_data

engine = get_connection()

create_log()
load_data(engine)
clean_data(engine)
train_data()
upload_data(engine)