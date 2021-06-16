import streamlit as st
import pandas as pd

# Writing App Title and Description
st.title('Spanish LaLiga Prediction')
st.write('This is a web app to predict the outcome of LaLiga soccer matches.')

# Making Sliders and Feature Variables
team_1 = st.text_input('Write the name of Team 1:')
team_2 = st.text_input('Write the name of Team 2:')

home = st.sidebar.selectbox('Which team plays in home:', ('team_1', 'team_2'))

goals_conceded_t1 = st.sidebar.slider(label='Team 1: Goals conceded',
                                    min_value=0,
                                    max_value=200,
                                    step=1)

goals_conceded_t2 = st.sidebar.slider(label='Team 2: Goals conceded',
                                    min_value=0,
                                    max_value=200,
                                    step=1)

goals_scored_t1 = st.sidebar.slider(label='Team 1: Goals scored',
                                    min_value=0,
                                    max_value=200,
                                    step=1)

goals_scored_t2 = st.sidebar.slider(label='Team 2: Goals scored',
                                    min_value=0,
                                    max_value=200,
                                    step=1)

home_wins_t1 = st.sidebar.slider(label='Team 1: Home wins',
                                    min_value=0,
                                    max_value=40,
                                    step=1)

home_wins_t2 = st.sidebar.slider(label='Team 2: Home wins',
                                    min_value=0,
                                    max_value=40,
                                    step=1)

away_wins_t1 = st.sidebar.slider(label='Team 1: Away wins',
                                    min_value=0,
                                    max_value=40,
                                    step=1)

away_wins_t2 = st.sidebar.slider(label='Team 2: Away wins',
                                    min_value=0,
                                    max_value=40,
                                    step=1)

home_losses_t1 = st.sidebar.slider(label='Team 1: Home losses',
                                    min_value=0,
                                    max_value=40,
                                    step=1)

home_losses_t2 = st.sidebar.slider(label='Team 2: Home losses',
                                    min_value=0,
                                    max_value=40,
                                    step=1)

away_losses_t1 = st.sidebar.slider(label='Team 1: Away losses',
                                    min_value=0,
                                    max_value=40,
                                    step=1)

away_losses_t2 = st.sidebar.slider(label='Team 2: Away losses',
                                    min_value=0,
                                    max_value=40,
                                    step=1)

home_draws_t1 = st.sidebar.slider(label='Team 1: Home draws',
                                    min_value=0,
                                    max_value=40,
                                    step=1)

home_draws_t2 = st.sidebar.slider(label='Team 2: Home draws',
                                    min_value=0,
                                    max_value=40,
                                    step=1)

away_draws_t1 = st.sidebar.slider(label='Team 1: Away draws',
                                    min_value=0,
                                    max_value=40,
                                    step=1)

away_draws_t2 = st.sidebar.slider(label='Team 2: Away draws',
                                    min_value=0,
                                    max_value=40,
                                    step=1)

rank_position_t1 = st.sidebar.slider(label='Team 1: Rank position',
                                    min_value=0,
                                    max_value=20,
                                    step=1)

rank_position_t2 = st.sidebar.slider(label='Team 2: Rank position',
                                    min_value=0,
                                    max_value=20,
                                    step=1) 

wins_streak_t1 = st.sidebar.slider(label='Team 1: Wins streak',
                                    min_value=0,
                                    max_value=20,
                                    step=1)

wins_streak_t2 = st.sidebar.slider(label='Team 2: Wins streak',
                                    min_value=0,
                                    max_value=20,
                                    step=1)   

draws_streak_t1 = st.sidebar.slider(label='Team 1: Draws streak',
                                    min_value=0,
                                    max_value=20,
                                    step=1)

draws_streak_t2 = st.sidebar.slider(label='Team 2: Draws streak',
                                    min_value=0,
                                    max_value=20,
                                    step=1)  

losses_streak_t1 = st.sidebar.slider(label='Team 1: Losses streak',
                                    min_value=0,
                                    max_value=20,
                                    step=1)

losses_streak_t2 = st.sidebar.slider(label='Team 2: Losses streak',
                                    min_value=0,
                                    max_value=20,
                                    step=1)                          

# Mapping Feature Labels with Slider Values
features = {
    'season': 2020,
    'league_match': 15,
    'team_1': team_1,
    'team_2': team_2,
    'home': home,
    'goals_conceded_t1': goals_conceded_t1,
    'goals_conceded_t2': goals_conceded_t2,
    'goals_scored_t1': goals_scored_t1,
    'goals_scored_t2': goals_scored_t2,
    'home_wins_t1': home_wins_t1,
    'home_wins_t2': home_wins_t2,
    'away_wins_t1': away_wins_t1,
    'away_wins_t2': away_wins_t2,
    'home_losses_t1': home_losses_t1,
    'home_losses_t2': home_losses_t2,
    'away_losses_t1': away_losses_t1,
    'away_losses_t2': away_losses_t2,
    'home_draws_t1': home_draws_t1,
    'home_draws_t2': home_draws_t2,
    'away_draws_t1': away_draws_t1,
    'away_draws_t2': away_draws_t2,
    'rank_position_t1': rank_position_t1,
    'rank_position_t2': rank_position_t1,
    'wins_streak_t1': wins_streak_t1,
    'wins_streak_t2': wins_streak_t2,
    'draws_streak_t1': draws_streak_t1,
    'draws_streak_t2': draws_streak_t2,
    'losses_streak_t1': losses_streak_t1,
    'losses_streak_t2': losses_streak_t2 
}

features_df = pd.DataFrame([features])

# Predicting Star Rating

if st.button('Predict'):
    st.write('TODO: Prediction')