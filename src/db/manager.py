import yaml
import os

from typing import Union, List, Optional
from src.db.data import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import select
from dotenv import load_dotenv

load_dotenv()

class DBManager():
    """
    This class defines a manager to handle SQLAlchemy ORM

    Parameters
    ----------
    config_file : str
        Configuration file path

    Attributes
    ----------
    _config : dict
        Dictionary containing the configuration data
    _engine : object
        SQLAlchemy ORM engine
    _session : sessionmaker.Session
        SQLAlchemy session
    """
    def __init__(self, config_file : str) -> None:
        self._config = self._get_config(config_file)
        self._engine = self._get_engine()
        self._session = sessionmaker(bind=self._engine)()

        Base.metadata.create_all(self._engine)

    def _get_config(self, config_file : str) -> dict:
        with open(config_file) as file:
            data = yaml.full_load(file)

        return data

    def _get_engine(self) -> None:
        data = f'{self._config["db_engine"]}://{os.getenv("DB_USER")}:'\
                f'{os.getenv("DB_PASSWORD")}@{self._config["host"]}:'\
                f'{self._config["port"]}/{self._config["db_name"]}'
        
        engine = create_engine(data)

        return engine

    def insert(self, data, classtype) -> None:
        statement = insert(classtype).values(data).on_conflict_do_nothing()
        self._session.execute(statement)
        self._session.commit()

    def select(self, table: object, limit : Optional[int] = None):
        if limit is None:
            statement = select([table]).\
                    order_by(table.season, table.league_match)
        else:
            statement = select([table]).\
                        order_by(table.season, table.league_match).\
                        limit(limit)

        result = self._session.execute(statement)
        
        return result.fetchall()

    def select_ranking(self, table, team, season, league_match):
        statement = select(table).where((table.team == team) and
                                    (table.season == season) and 
                                    (table.league_match == league_match))

        result = self._session.execute(statement)

        return result.fetchall()

    def select_result(self, table, team_1, team_2, season, league_match):
        statement = select(table).where((table.team_1 == team_1) and
                                    (table.team_2 == team_2) and
                                    (table.season == season) and 
                                    (table.league_match == league_match))

        result = self._session.execute(statement)

        return result.fetchall()

    def close(self) -> None:
        self._session.close()

    def open(self) -> None:
        self._session = sessionmaker(bind=self._engine)()