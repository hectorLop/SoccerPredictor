from test.data.data_fixtures import get_features_df
import pytest

from src.preprocessing.features_preprocesses import (
    ComputeLeagueRankPosition,
    ComputeWins,
    ComputeDraws,
    ComputeLosses,
    ComputeGoalsConceded,
    ComputeGoalsScored,
    FeaturePipeline,
)
from pandas._testing import assert_frame_equal

from test.data.data_fixtures import get_features_df

def test_feature_pipeline(get_features_df):
    results, general, home, away, expected_results = get_features_df

    # Compute general, home and away wins
    wins_pipeline = FeaturePipeline([
        ComputeWins(general,
                    ['team_1', 'team_2'],
                    ['general_wins_t1', 'general_wins_t2']),
        ComputeWins(home,
                    ['team_1', 'team_2'],
                    ['home_wins_t1', 'home_wins_t2']),
        ComputeWins(away,
                    ['team_1', 'team_2'],
                    ['away_wins_t1', 'away_wins_t2']),
    ])
    # General, home and away draws
    draws_pipeline = FeaturePipeline([
        ComputeDraws(general,
                    ['team_1', 'team_2'],
                    ['general_draws_t1', 'general_draws_t2']),
        ComputeDraws(home,
                    ['team_1', 'team_2'],
                        ['home_draws_t1', 'home_draws_t2']),
        ComputeDraws(away,
                    ['team_1', 'team_2'],
                    ['away_draws_t1', 'away_draws_t2']),
    ])
    # General, home and away losses
    loss_pipeline = FeaturePipeline([
        ComputeLosses(general,
                    ['team_1', 'team_2'],
                    ['general_losses_t1', 'general_losses_t2']),
        ComputeLosses(home,
                    ['team_1', 'team_2'],
                    ['home_losses_t1', 'home_losses_t2']),
        ComputeLosses(away,
                    ['team_1', 'team_2'],
                    ['away_losses_t1', 'away_losses_t2']),      
    ])
    # General, home and away goals scored
    goals_scored_pipeline = FeaturePipeline([
        ComputeGoalsScored(
                general,
                ['team_1', 'team_2'],
                ['general_goals_scored_t1', 'general_goals_scored_t2']),
        ComputeGoalsScored(
                home,
                ['team_1', 'team_2'],
                ['home_goals_scored_t1', 'home_goals_scored_t2']),
        ComputeGoalsScored(
                away,
                ['team_1', 'team_2'],
                ['away_goals_scored_t1', 'away_goals_scored_t2'])
    ])
    # General, home and away goals conceded
    goals_conceded_pipeline = FeaturePipeline([
        ComputeGoalsConceded(
                general,
                ['team_1', 'team_2'],
                ['general_goals_conceded_t1', 'general_goals_conceded_t2']),
        ComputeGoalsConceded(
                home,
                ['team_1', 'team_2'],
                ['home_goals_conceded_t1', 'home_goals_conceded_t2']),
        ComputeGoalsConceded(
                away,
                ['team_1', 'team_2'],
                ['away_goals_conceded_t1', 'away_goals_conceded_t2'])
    ])

    # Feature preprocessing pipeline
    pipeline = FeaturePipeline([
        ComputeLeagueRankPosition(general, ['team_1', 'team_2'],
                                ['rank_t1', 'rank_t2']),
        wins_pipeline,
        draws_pipeline,
        loss_pipeline,
        goals_scored_pipeline,
        goals_conceded_pipeline
    ])

    results_trans = pipeline(results)

    assert_frame_equal(results_trans, expected_results)