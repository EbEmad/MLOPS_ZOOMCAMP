import pickle
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Any
import mlflow
from mlflow.tracking import MlflowClient
MLFLOW_TACKING_URI='http://0.0.0.0:5000'
client=MlflowClient(tracking_uri=MLFLOW_TACKING_URI)
RUN_ID='m-8343a6add65d420bb08775abc3c8f70b'
logged_model=f'runs://{RUN_ID}/model'
# load model
model=mlflow.pyfunc.load_model(logged_model)


class Ride(BaseModel):
    PULocationID:int
    DOLocationID:int
    trip_distance:float

def prepare_features(ride):
    features={}
    features['PU_DO']='%s_%s'%(ride.PULocationID,ride.DOLocationID)
    features['trip_distance']=ride.trip_distance
    return features


def predict(features):
    x=dv.transform(features)
    preds=model.predict(x)
    return float(preds[0])
app=FastAPI()

@app.post('/predict')
def predict_endpoint(ride:Ride):
    features=prepare_features(ride)
    pred=predict(features)
    result={
        'duration':pred
    }
    return result
@app.get('/')
def root():
    return {'message':'Welcome Eng Ebrahim'}