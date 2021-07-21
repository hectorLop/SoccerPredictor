from typing import Any

from fastapi import Query
from pydantic import BaseModel, validator

class Text(BaseModel):
    text: str = Query(None, min_length=1)


class Item(BaseModel):
    data: Any

    @validator("data")
    def valid_season(cls, value):
        if not value:
            raise ValueError("Data cannot be empty")

        return value