from flask import Flask, jsonify, request
from xgboost import XGBClassifier
from src.preprocessing.model_preprocessing import ModelPreprocesser
from src.preprocessing.model_preprocessing import *
from sklearn.pipeline import Pipeline

import pickle
import os
import pandas as pd

app = Flask(__name__)

THIS_DIR = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(THIS_DIR, 'xgb_model.pkl'), 'rb') as file:
    model = pickle.load(file)

# TODO: How to serialize the pipeline used in training in order to be able
# to load it here without pickle AttributeErrors
pipeline = ModelPreprocesser()
df = pd.read_csv(os.path.join(THIS_DIR, 'soccer_dataset.csv'))
df = df.drop('outcome', axis=1)
df = df.rename(columns={'goals_conceced_t2': 'goals_conceded_t2'})
_ = pipeline.fit_transform(df)

@app.route('/')
def hello():
    return 'Hello World!'

@app.route('/predict', methods=['POST'])
def predict():
    json_data = request.json
    df = pd.DataFrame(json_data, index=[0])
    transformed_data = pipeline.transform(df)

    pred = model.predict(transformed_data)[0]

    if pred == 0:
        winner = 'team_1'
    elif pred == 1:
        winner = 'draw'
    else:
        winner = 'team_2'

    return jsonify({'class_id': str(pred), 'winner': str(winner)})