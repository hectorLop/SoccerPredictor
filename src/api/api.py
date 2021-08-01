from fastapi import requests
from xgboost import XGBClassifier
from src.preprocessing.model_preprocessing import ModelPreprocesser
from src.preprocessing.model_preprocessing import FeatureSelector
from sklearn.pipeline import Pipeline
from fastapi import FastAPI
from http import HTTPStatus
from fastapi.requests import Request
from datetime import datetime
from functools import wraps
from src.config.logger_config import logger
from typing import Dict
from src.api.schemas import Item

import pickle
import os
import pandas as pd
import sys

PIPELINE_PATH = os.path.join(sys.path[0], 'src/models_pipelines/pipeline.pkl')
MODEL_PATH = os.path.join(sys.path[0], 'src/models_pipelines/xgboost_model.pkl')

# Define application
app = FastAPI(
    title="Spanish LaLiga Predictor",
    description="Predict spanish LaLiga matches outcome.",
    version="0.1",
)

@app.on_event("startup")
def load_artifacts():
    global model, pipeline
    logger.info("Loading model...")
    model = pickle.load(open(MODEL_PATH, 'rb'))
    logger.info("Loading preprocessing pipeline...")
    pipeline = pickle.load(open(PIPELINE_PATH, 'rb'))

def construct_response(f):
    """Construct a JSON response for an endpoint's results."""

    @wraps(f)
    def wrap(request: Request, *args, **kwargs):
        results = f(request, *args, **kwargs)

        # Construct response
        response = {
            "message": results["message"],
            "method": request.method,
            "status-code": results["status-code"],
            "timestamp": datetime.now().isoformat(),
            "url": request.url._url,
        }

        # Add data
        if "data" in results:
            response["data"] = results["data"]

        return response

    return wrap

@app.get("/", tags=['General'])
@construct_response
def _index(request: Request):
    """Health check."""
    response = {
        "message": HTTPStatus.OK.phrase,
        "status-code": HTTPStatus.OK,
        "data": {},
    }
    return response

@app.post("/predict", tags=["Prediction"])
@construct_response
def _predict(request: Request, features: Item) -> Dict:
    """Predict tags for a list of texts using the best run. """
    logger.info('Creating DataFrame...')
    df = pd.DataFrame(features.__dict__, index=[0])
    logger.info('Preprocessing data...')
    transformed_data = pipeline.transform(df)
    logger.info('Making predictions...')
    pred = model.predict(transformed_data)[0]

    if pred == 0:
        winner = 'team_1'
    elif pred == 1:
        winner = 'draw'
    else:
        winner = 'team_2'

    response = {
        "message": HTTPStatus.OK.phrase,
        "status-code": HTTPStatus.OK,
        "data": {"winner": winner, "class_id": str(pred)}
    }

    return response