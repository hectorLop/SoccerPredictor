import streamlit as st
import pandas as pd
import json
import boto3
import os

from dotenv import load_dotenv

load_dotenv()

def get_data():
    bucket = os.getenv('AWS_BUCKET')
    s3 = boto3.client('s3')

    result = s3.get_object(Bucket=bucket, Key='predictions/predictions.json')

    data = result["Body"].read()
    data = json.loads(data)

    return data

# Writing App Title and Description
st.title(f'Spanish LaLiga Prediction')
st.write('This is a web app to predict the outcome of LaLiga soccer matches.')

if st.button('Get Results'):
    data = get_data()
    league_match = data["league_match"]

    st.subheader(f'League Match {league_match}')

    df_data = []

    for i in range(10):
        #st.markdown(f'## Match {i+1}')
        team_1 = data[f'match_{i}']['team_1']
        team_2 = data[f'match_{i}']['team_2']
        outcome = data[f'match_{i}']['outcome']

        df_data.append((team_1, team_2, outcome))

    df = pd.DataFrame(df_data, columns=['team_1', 'team_2', 'outcome'])

    st.dataframe(df)