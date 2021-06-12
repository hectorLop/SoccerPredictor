from test.data.data_fixtures import get_features_df
import pytest

from src.preprocessing.features_preprocesses import (
    ComputeGoalsConceded, ComputeGoalsScored,
    ComputeHomeWins, ComputeAwayWins,
    ComputeHomeDraws, ComputeAwayDraws,
    ComputeHomeLosses, ComputeAwayLosses,
    ComputeDrawsStreak, ComputeLossesStreak,
    ComputeWinsStreak, ComputeLeagueRankPosition,
    FeaturePipeline
)
from pandas._testing import assert_frame_equal

from test.data.data_fixtures import get_features_df, get_cleaned_df

def test_feature_pipeline(get_cleaned_df, get_features_df):
    matches_df, rank_df = get_cleaned_df
    expected_matches_df = get_features_df
    columns = ['team_1', 'team_2']

    pipeline = FeaturePipeline([
        ComputeGoalsConceded(rank_df, columns,
                        ['goals_conceded_t1', 'goals_conceded_t2']),
        ComputeGoalsScored(rank_df, columns,
                        ['goals_scored_t1', 'goals_scored_t2']),
        ComputeHomeWins(rank_df, columns,
                        ['home_wins_t1', 'home_wins_t2']),
        ComputeAwayWins(rank_df, columns,
                        ['away_wins_t1', 'away_wins_t2']),
        ComputeHomeLosses(rank_df, columns,
                        ['home_losses_t1', 'home_losses_t2']),
        ComputeAwayLosses(rank_df, columns,
                        ['away_losses_t1', 'away_losses_t2']),
        ComputeHomeDraws(rank_df, columns,
                        ['home_draws_t1', 'home_draws_t2']),
        ComputeAwayDraws(rank_df, columns,
                        ['away_draws_t1', 'away_draws_t2']),
        ComputeLeagueRankPosition(rank_df, columns,
                        ['rank_position_t1', 'rank_position_t2']),
        ComputeWinsStreak(rank_df, columns,
                        ['wins_streak_t1', 'wins_streak_t2']),
        ComputeDrawsStreak(rank_df, columns,
                        ['draws_streak_t1', 'draws_streak_t2']),
        ComputeLossesStreak(rank_df, columns,
                        ['losses_streak_t1', 'losses_streak_t2'])
    ])

    matches_df_trans = pipeline.transform(matches_df)

    assert_frame_equal(matches_df_trans, expected_matches_df)