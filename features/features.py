# Feature definition
import sys
sys.path.insert(0, '../')

from datetime import datetime
from pathlib import Path

from feast import Entity, Feature, FeatureView, ValueType, FileSource
from google.protobuf.duration_pb2 import Duration

from src.config import config

# Read data
START_TIME = "2021-9-19"
project_details = FileSource(
    path=str(Path(config.DATA_DIR, "features.parquet")),
    event_timestamp_column="created_on",
)

# Define an entity for the project
project = Entity(
    name="id",
    value_type=ValueType.INT64,
    description="project id",
)

# Define a Feature View for each project
# Can be used for fetching historical data and online serving
project_details_view = FeatureView(
    name="project_details",
    entities=["id"],
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
    ],
    online=True,
    input=project_details,
    tags={},
)