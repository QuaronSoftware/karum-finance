from pydantic import BaseModel, field_validator
from typing import Any


class OKXBaseModel(BaseModel):
    @field_validator("*", mode="before")
    @classmethod
    def empty_str_to_none(cls, v: Any) -> Any:
        if v == "":
            return None
        return v