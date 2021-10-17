from sklearn.model_selection import train_test_split
from typing import List

class FeaturePipeline():
    def __init__(self, preprocesses: List[object]) -> None:
        self.preprocesses = preprocesses

    def transform(self, dataframe):
        for preprocess in self.preprocesses:
            dataframe = preprocess(dataframe)

        return dataframe

    def __call__(self, dataframe):
        return self.transform(dataframe)

def get_training_test_sets(df):
    y = df['outcome'].replace({
        'team_1': 0,
        'team_2': 1,
        'draw': 2
    }).values

    X = df.drop('outcome', axis=1)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2,
                                                        random_state=42,
                                                        stratify=y)

    return X_train, X_test, y_train, y_test

