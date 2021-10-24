from dagster import solid, Output, OutputDefinition, pipeline, execute_pipeline
from src.inference.utils import (
    get_last_data,
    preprocess_for_inference,
    generate_preds,
    parse_preds
)

@solid(
    output_defs=[
        OutputDefinition(name='results', is_required=True),
        OutputDefinition(name='general', is_required=True),
        OutputDefinition(name='home', is_required=True),
        OutputDefinition(name='away', is_required=True)
    ]
)
def load_data(context):
    results, general, home, away = get_last_data()

    yield Output(results, 'results')
    yield Output(general, 'general')
    yield Output(home, 'home')
    yield Output(away, 'away')

@solid(
    output_defs=[
        OutputDefinition(name='data', is_required=True),
        OutputDefinition(name='teams', is_required=True),
        OutputDefinition(name='league_match', is_required=True)
    ]
)
def preprocess(context, results, general, home, away):
    data, teams, league_match = preprocess_for_inference(results, general, 
                                                        home, away)

    yield Output(data, 'data')
    yield Output(teams, 'teams')
    yield Output(league_match, 'league_match')

@solid
def predict(context, data, teams, league_match):
    preds = generate_preds(data)

    parse_preds(preds, teams, league_match)

@pipeline
def predict_pipeline():
    results, general, home, away = load_data()
    data, teams, league_match = preprocess(results, general, home, away)
    predict(data, teams, league_match)

if __name__ == '__main__':
    execute_pipeline(predict_pipeline)