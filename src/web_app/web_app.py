import streamlit as st
import pandas as pd
import requests
import json
import boto3
import os

from dotenv import load_dotenv
from src.config.config import DATA_DIR

load_dotenv()
bucket = os.getenv('AWS_BUCKET')

s3 = boto3.client('s3')
result = s3.get_object(Bucket=bucket, Key='predictions/predictions.json')
data = result["Body"].read()
data = json.loads(data)

league_match = data["league_match"]
# Writing App Title and Description
st.title(f'Spanish LaLiga Prediction - League Match {league_match}')
st.write('This is a web app to predict the outcome of LaLiga soccer matches.')

for i in range(10):
    st.markdown(f'## Match {i+1}')
    team_1 = data[f'match_{i}']['team_1']
    team_2 = data[f'match_{i}']['team_2']
    outcome = data[f'match_{i}']['outcome']

    st.write(f'{team_1} vs {team_2} ----> {outcome}')