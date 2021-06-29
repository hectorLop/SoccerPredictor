from typing import Union, List
from src.db.data import Match, Rank, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import yaml

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
        data = f'{self._config["db_engine"]}://{self._config["user"]}:'\
                f'{self._config["password"]}@{self._config["host"]}:'\
                f'{self._config["port"]}/{self._config["db_name"]}'
        
        engine = create_engine(data)

        return engine

    def insert(self, element: Union[Match, Rank]) -> None:
        self._session.add(element)
        self._session.commit()

    def insert_bulk(self, elements: List[Union[Match, Rank]]) -> None:
        self._session.add_all(elements)
        self._session.commit()

    def close(self) -> None:
        self._session.close()

    def open(self) -> None:
        self._session = sessionmaker(bind=self._engine)()