import pickle
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Any
with open('./lin_rdge.bin', 'rb') as f_in:
    (dv,model)=pickle.load( f_in)
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