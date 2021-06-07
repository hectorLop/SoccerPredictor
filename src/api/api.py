import streamlit as st
import pandas as pd

# Writing App Title and Description
st.title('Spanish LaLiga Prediction')
st.write('This is a web app to predict the outcome of LaLiga soccer matches.')

# Making Sliders and Feature Variables
team_1 = st.text_input('Write the name of Team 1:')
team_2 = st.text_input('Write the name of Team 2:')

goals_conceded_t1 = st.sidebar.slider(label='goals_conceded_t1',
                                    min_value=0,
                                    max_value=200,
                                    step=1)

goals_conceded_t2 = st.sidebar.slider(label='goals_conceded_t2',
                                    min_value=0,
                                    max_value=200,
                                    step=1)

goals_scored_t1 = st.sidebar.slider(label='goals_scored_t1',
                                    min_value=0,
                                    max_value=200,
                                    step=1)

goals_scored_t2 = st.sidebar.slider(label='goals_scored_t2',
                                    min_value=0,
                                    max_value=200,
                                    step=1)

# Mapping Feature Labels with Slider Values
features = {
    'team_1': team_1,
    'team_2': team_2,
    'goals_conceded_t1': goals_conceded_t1,
    'goals_conceded_t2': goals_conceded_t2,
    'goals_scored_t1': goals_scored_t1,
    'goals_scored_t2': goals_scored_t2
}

features_df = pd.DataFrame([features])
st.table(features_df)

# Predicting Star Rating

if st.button('Predict'):
    st.write('TODO: Prediction')