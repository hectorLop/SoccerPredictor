RESULTS_COLS = ['season', 'league_match', 'home', 'team_1', 'team_2',
                    'outcome']
RANKING_COLS = ['season', 'league_match', 'rank_pos', 'team',
                'matches', 'wins', 'draws', 'losses', 'goals_scored',
                'goals_conceded', 'goals_difference']

FEATURES_TO_DROP = [
    'season', 'team_1', 'team_2', 'league_match', 'home_wins_t1', 'home_wins_t2',
    'away_wins_t1', 'away_wins_t2', 'general_wins_t1', 'general_wins_t2',
    'home_draws_t1', 'home_draws_t2', 'away_draws_t1', 'away_draws_t2', 
    'general_draws_t1', 'general_draws_t2', 'home_losses_t1', 'home_losses_t2',
    'away_losses_t1', 'away_losses_t2', 'general_losses_t1', 'general_losses_t2'
]