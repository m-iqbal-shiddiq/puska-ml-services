import os
import joblib
import numpy as np
import pandas as pd
import tensorflow as tf

from datetime import datetime
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM
from sklearn.preprocessing import MinMaxScaler

from helpers.constant import DATASET_CLEANED_PATH, DATASET_PREDICTION_PATH, MODEL_PATH, SCALER_PATH, TIMESTEP, TRAIN_PERCENTAGE, EPOCHS
from helpers.log import update_log


def calculate_mape(row):
    actual = row['actual']
    predicted = row['prediction']
    return round(np.abs((actual - predicted) / (actual + 1e-10)) * 100, 2)

def train_data():
    print('Training model...')
    
    for filename in os.listdir(DATASET_CLEANED_PATH):
        if not filename.endswith('.csv'):
            continue
        
        data_df = pd.read_csv(os.path.join(DATASET_CLEANED_PATH, filename))
        data_df = data_df.rename(columns={'jumlah_produksi': 'y'})
        
        # scaling data
        scaler = MinMaxScaler(feature_range=(0, 1), clip=True)
        data_df[['y']] = scaler.fit_transform(data_df[['y']])
        
        joblib.dump(scaler, os.path.join(SCALER_PATH, filename.replace('.csv', '.pkl')))
        update_log('cleaned', filename, 'scaler', filename.replace('.csv', '.pkl'))
        
        # create timesteps
        for i in range(1, TIMESTEP + 1):
            data_df[f'y-{i}'] = data_df['y'].shift(i)
            
        data_df = data_df.iloc[TIMESTEP:, :].reset_index(drop=True)
        
        # split data
        split_index = int(len(data_df) * TRAIN_PERCENTAGE)
        
        train_df = data_df.iloc[:split_index, :]
        test_df = data_df.iloc[split_index:, :]
        
        x_columns = data_df.columns[5:].tolist()
        
        x_train = train_df[x_columns].values
        x_test = test_df[x_columns].values
        
        y_train = train_df['y'].values
        y_test = test_df['y'].values
        
        x_train = x_train.reshape(x_train.shape[0], 1, x_train.shape[1])
        x_test = x_test.reshape(x_test.shape[0], 1, x_test.shape[1])
        
        # create model
        model = Sequential()
        model.add(LSTM(2, input_shape=(1, TIMESTEP)))
        model.add(Dense(1))
        model.compile(loss='mean_squared_error', optimizer='adam')
        model.fit(x_train, y_train, epochs=EPOCHS, batch_size=1, verbose=2)
        
        # prediction
        train_pred = model.predict(x_train)
        test_pred = model.predict(x_test)
        
        train_pred = scaler.inverse_transform(train_pred)
        y_train = scaler.inverse_transform([y_train])
        
        test_pred = scaler.inverse_transform(test_pred)
        y_test = scaler.inverse_transform([y_test])
        
        y_act = list(y_train[0]) + list(y_test[0])
        y_pred = list(train_pred[:, 0]) + list(test_pred[:, 0])
        y_pred = [round(y, 2) for y in y_pred]
        
        evaluation_df = pd.DataFrame(columns=['date', 'actual', 'prediction'])
        evaluation_df['date'] = data_df['date']
        evaluation_df['id_waktu'] = data_df['id_waktu']
        evaluation_df['id_lokasi'] = data_df['id_lokasi']
        evaluation_df['id_unit_peternakan'] = data_df['id_unit_peternakan']
        evaluation_df['actual'] = y_act
        evaluation_df['prediction'] = y_pred
        evaluation_df['mape'] = evaluation_df.apply(calculate_mape, axis=1)
        evaluation_df['created_at'] = datetime.now()
        evaluation_df['latency'] = None
        evaluation_df = evaluation_df[['id_waktu', 'id_lokasi', 'id_unit_peternakan', 'prediction', 'latency', 'mape', 'created_at']]
        evaluation_df.to_csv(os.path.join(DATASET_PREDICTION_PATH, filename), index=False)
        
        model.save(os.path.join(MODEL_PATH, filename.replace('.csv', '.keras')))
        
        update_log('cleaned', filename, 'prediction', filename)
        update_log('cleaned', filename, 'model', filename.replace('.csv', '.keras'))
        update_log('cleaned', filename, 'last_training_update', datetime.now())
        
        