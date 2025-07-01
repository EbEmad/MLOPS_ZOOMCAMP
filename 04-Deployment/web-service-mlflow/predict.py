import pickle
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Any
import mlflow
from mlflow.tracking import MlflowClient
MLFLOW_TRACKING_URI = 'http://0.0.0.0:5000'
RUN_ID = '2e985055df794a318e2e03e5c8ef2bc6'
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI) # tells mlflow where the tracking server
client=MlflowClient(tracking_uri=MLFLOW_TRACKING_URI)
mlflow.set_experiment("Mlops_ZoomCamp_Experiement") # # creates or selects an experiment to log runs (like training ,metrics,models)
path=client.download_artifacts(run_id=RUN_ID,path='preprocessor/preprocessor.b')
with open(path, 'rb') as f_in:
    dv ,model= pickle.load(f_in)

print("Vectorizer loaded from:", path)


class Ride(BaseModel):
    PULocationID: int
    DOLocationID: int
    trip_distance: float

def prepare_features(ride):
    return {
        'PU_DO': f'{ride.PULocationID}_{ride.DOLocationID}',
        'trip_distance': ride.trip_distance
    }

def predict(features):
    x = dv.transform(features)
    preds = model.predict(x)
    return float(preds[0])

app = FastAPI()

@app.post('/predict')
def predict_endpoint(ride: Ride):
    features = prepare_features(ride)
    pred = predict(features)
    return {'duration': pred,
            'model_version':RUN_ID
            }

@app.get('/')
def root():
    return {'message': 'Welcome Eng Ebrahim'}
