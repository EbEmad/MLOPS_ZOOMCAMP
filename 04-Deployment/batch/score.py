#!/usr/bin/env python
# coding: utf-8

import sys
import os
import uuid
import pickle
import pandas as pd
import mlflow
from sklearn.feature_extraction import DictVectorizer
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.pipeline import make_pipeline



mlflow.set_tracking_uri("http://localhost:5000")
RUN_ID = os.getenv('RUN_ID', '02290598e0a64637a630da62db396cb5')
logged_model = f'/home/ebrahim/MLOPS_ZOOMCAMP/02-experiment-tracking/mlruns/2/{RUN_ID}/artifacts/model'
# Load model as a PyFuncModel.
loaded_model = mlflow.pyfunc.load_model(logged_model)

print(loaded_model)


year = 2021
month = 3
taxi_type = 'green'

input_file = f'https://d37ci6vzurychx.cloudfront.net/trip-data/{taxi_type}_tripdata_{year:04d}-{month:02d}.parquet'
output_file = f'output/{taxi_type}/{year:04d}-{month:02d}.parquet'

RUN_ID = os.getenv('RUN_ID', 'c7fa223a63c842868e073d6bf352fb3f')



output_file



def generate_uuids(n):
    ride_ids = []
    for i in range(n):
        ride_ids.append(str(uuid.uuid4()))
    return ride_ids

def read_dataframe(filename: str):
    df = pd.read_parquet(filename)

    df['duration'] = df.lpep_dropoff_datetime - df.lpep_pickup_datetime
    df.duration = df.duration.dt.total_seconds() / 60
    df = df[(df.duration >= 1) & (df.duration <= 60)]

    df['ride_id'] = generate_uuids(len(df))

    return df


def prepare_dictionaries(df: pd.DataFrame):
    categorical = ['PULocationID', 'DOLocationID']
    df[categorical] = df[categorical].astype(str)

    df['PU_DO'] = df['PULocationID'] + '_' + df['DOLocationID']

    categorical = ['PU_DO']
    numerical = ['trip_distance']
    dicts = df[categorical + numerical].to_dict(orient='records')
    return dicts



def load_model(run_id):
    mlflow.set_tracking_uri("http://localhost:5000")
    logged_model = f"runs:/{run_id}/model"
    model = mlflow.pyfunc.load_model(logged_model)

    # Download and load the DictVectorizer
    # client = mlflow.tracking.MlflowClient()
    # dv_path = client.download_artifacts(run_id, "dict_vectorizer.pkl")
    with open("dict_vectorizer.bin", "rb") as f_in:
        dv = pickle.load(f_in)

    return model, dv


def apply_model(input_file, run_id, output_file):

    # df = read_dataframe(input_file)
    df=pd.read_parquet('./data/green_tripdata_2021-03.parquet')
    dicts = prepare_dictionaries(df)

    model, dv = load_model(run_id)

    #x = dv.transform(dicts)  # ✅ Apply the same transformation used in training
    y_pred = loaded_model.predict(dicts)

    df_result = pd.DataFrame()
    # df_result['ride_id'] = df['ride_id']  # Only if this column exists
    df_result['lpep_pickup_datetime'] = df['lpep_pickup_datetime']
    df_result['PULocationID'] = df['PULocationID']
    df_result['DOLocationID'] = df['DOLocationID']
    #df_result['actual_duration'] = df['duration']
    df_result['predicted_duration'] = y_pred
    #df_result['diff'] = df_result['actual_duration'] - df_result['predicted_duration']
    df_result['model_version'] = run_id

    df_result.to_parquet(output_file, index=False)


# In[74]:


df=pd.read_parquet('./data/green_tripdata_2021-03.parquet')
df.columns


# In[75]:


apply_model(input_file=input_file, run_id=RUN_ID, output_file=output_file)


# In[76]:


get_ipython().system('ls output/green/')


# In[ ]:




