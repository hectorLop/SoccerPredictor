# Feature definition
import sys
sys.path.insert(0, '../')

from datetime import datetime
from pathlib import Path

from feast import Entity, Feature, FeatureView, ValueType, FileSource
from google.protobuf.duration_pb2 import Duration

from src.config import config

# Read data
START_TIME = "2021-9-30"
training_data = FileSource(
    path=str(Path(config.DATA_DIR, "training_data.parquet")),
    event_timestamp_column="created_on",
)

# Define an entity for the project
training = Entity(
    name="training_id",
    value_type=ValueType.INT64,
    description="training ids",
)

# Define a Feature View for each project
# Can be used for fetching historical data and online serving
training_data_view = FeatureView(
    name="training_data",
    entities=['training_id'],
    ttl=Duration(
       seconds=(datetime.today() - datetime.strptime(START_TIME, "%Y-%m-%d")).days * 24 * 60 * 60
    ),
    features=[
        Feature(name="team_1", dtype=ValueType.FLOAT),
        Feature(name='team_2', dtype=ValueType.FLOAT),
        Feature(name="rank_t1", dtype=ValueType.FLOAT),
        Feature(name='tank_t2', dtype=ValueType.FLOAT),
        Feature(name='general_wins_t1', dtype=ValueType.FLOAT),
        Feature(name='general_wins_t2', dtype=ValueType.FLOAT),
        Feature(name='home_wins_t1', dtype=ValueType.FLOAT),
        Feature(name='home_wins_t2', dtype=ValueType.FLOAT),
        Feature(name='away_wins_t1', dtype=ValueType.FLOAT),
        Feature(name='away_wins_t2', dtype=ValueType.FLOAT),
        Feature(name='general_draws_t1', dtype=ValueType.FLOAT),
        Feature(name='general_draws_t2', dtype=ValueType.FLOAT),
        Feature(name='home_draws_t1', dtype=ValueType.FLOAT),
        Feature(name='home_draws_t2', dtype=ValueType.FLOAT),
        Feature(name='away_draws_t1', dtype=ValueType.FLOAT),
        Feature(name='away_draws_t2', dtype=ValueType.FLOAT),
        Feature(name='general_losses_t1', dtype=ValueType.FLOAT),
        Feature(name='general_losses_t2', dtype=ValueType.FLOAT),
        Feature(name='home_losses_t1', dtype=ValueType.FLOAT),
        Feature(name='home_losses_t2', dtype=ValueType.FLOAT),
        Feature(name='away_losses_t1', dtype=ValueType.FLOAT),
        Feature(name='away_losses_t2', dtype=ValueType.FLOAT),
        Feature(name='general_goals_scored_t1', dtype=ValueType.FLOAT),
        Feature(name='general_goals_scored_t2', dtype=ValueType.FLOAT),
        Feature(name='home_goals_scored_t1', dtype=ValueType.FLOAT),
        Feature(name='home_goals_scored_t2', dtype=ValueType.FLOAT),
        Feature(name='away_goals_scored_t1', dtype=ValueType.FLOAT),
        Feature(name='away_goals_scored_t2', dtype=ValueType.FLOAT),
        Feature(name='general_goals_conceded_t1', dtype=ValueType.FLOAT),
        Feature(name='general_goals_conceded_t2', dtype=ValueType.FLOAT),
        Feature(name='home_goals_conceded_t1', dtype=ValueType.FLOAT),
        Feature(name='home_goals_conceded_t2', dtype=ValueType.FLOAT),
        Feature(name='away_goals_conceded_t1', dtype=ValueType.FLOAT),
        Feature(name='away_goals_conceded_t2', dtype=ValueType.FLOAT),
        Feature(name='outcome', dtype=ValueType.INT32)
    ],
    online=True,
    batch_source=training_data,
    tags={},
)

test_data = FileSource(
    path=str(Path(config.DATA_DIR, "test_data.parquet")),
    event_timestamp_column="created_on",
)

# Define an entity for the project
test = Entity(
    name="test_id",
    value_type=ValueType.INT64,
    description="test ids",
)

test_data_view = FeatureView(
    name="test_data",
    entities=['test_id'],
    ttl=Duration(
       seconds=(datetime.today() - datetime.strptime(START_TIME, "%Y-%m-%d")).days * 24 * 60 * 60
    ),
    features=[
        Feature(name="team_1", dtype=ValueType.FLOAT),
        Feature(name='team_2', dtype=ValueType.FLOAT),
        Feature(name="rank_t1", dtype=ValueType.FLOAT),
        Feature(name='tank_t2', dtype=ValueType.FLOAT),
        Feature(name='general_wins_t1', dtype=ValueType.FLOAT),
        Feature(name='general_wins_t2', dtype=ValueType.FLOAT),
        Feature(name='home_wins_t1', dtype=ValueType.FLOAT),
        Feature(name='home_wins_t2', dtype=ValueType.FLOAT),
        Feature(name='away_wins_t1', dtype=ValueType.FLOAT),
        Feature(name='away_wins_t2', dtype=ValueType.FLOAT),
        Feature(name='general_draws_t1', dtype=ValueType.FLOAT),
        Feature(name='general_draws_t2', dtype=ValueType.FLOAT),
        Feature(name='home_draws_t1', dtype=ValueType.FLOAT),
        Feature(name='home_draws_t2', dtype=ValueType.FLOAT),
        Feature(name='away_draws_t1', dtype=ValueType.FLOAT),
        Feature(name='away_draws_t2', dtype=ValueType.FLOAT),
        Feature(name='general_losses_t1', dtype=ValueType.FLOAT),
        Feature(name='general_losses_t2', dtype=ValueType.FLOAT),
        Feature(name='home_losses_t1', dtype=ValueType.FLOAT),
        Feature(name='home_losses_t2', dtype=ValueType.FLOAT),
        Feature(name='away_losses_t1', dtype=ValueType.FLOAT),
        Feature(name='away_losses_t2', dtype=ValueType.FLOAT),
        Feature(name='general_goals_scored_t1', dtype=ValueType.FLOAT),
        Feature(name='general_goals_scored_t2', dtype=ValueType.FLOAT),
        Feature(name='home_goals_scored_t1', dtype=ValueType.FLOAT),
        Feature(name='home_goals_scored_t2', dtype=ValueType.FLOAT),
        Feature(name='away_goals_scored_t1', dtype=ValueType.FLOAT),
        Feature(name='away_goals_scored_t2', dtype=ValueType.FLOAT),
        Feature(name='general_goals_conceded_t1', dtype=ValueType.FLOAT),
        Feature(name='general_goals_conceded_t2', dtype=ValueType.FLOAT),
        Feature(name='home_goals_conceded_t1', dtype=ValueType.FLOAT),
        Feature(name='home_goals_conceded_t2', dtype=ValueType.FLOAT),
        Feature(name='away_goals_conceded_t1', dtype=ValueType.FLOAT),
        Feature(name='away_goals_conceded_t2', dtype=ValueType.FLOAT),
        Feature(name='outcome', dtype=ValueType.INT32)
    ],
    online=True,
    batch_source=test_data,
    tags={},
)