from typing import List, Tuple
import pandas as pd

from src.preprocessing.config import RANKING_COLS, RESULTS_COLS
from src.db.manager import DBManager
from src.db.data import Results, GeneralRanking, HomeRanking, AwayRanking

class DataRetriever:
    def __init__(self, db_config : str) -> None:
        self._db_manager = DBManager(db_config)

    def get_historical_data(self):
        results = self._db_manager.select(Results)
        general_ranking = self._db_manager.select(GeneralRanking)
        home_ranking = self._db_manager.select(HomeRanking)
        away_ranking = self._db_manager.select(AwayRanking)

        results_df = self.get_result_dataframe(results)
        general_df, home_df, away_df = self.get_ranking_dataframes([general_ranking,
                                                                    home_ranking,
                                                                    away_ranking])

        return results_df, general_df, home_df, away_df

    def get_result_dataframe(self, raw_results : List[Tuple]) -> pd.DataFrame:
        results_df = pd.DataFrame(raw_results, columns=RESULTS_COLS)

        return results_df

    def get_ranking_dataframes(self, datasets: List[List[Tuple]]) -> pd.DataFrame:
        dfs = (pd.DataFrame(dataset, columns=RANKING_COLS) for dataset in datasets)

        return dfs