from abc import ABC
import dataclasses
from typing import Any, Dict


class DynamicDataclass(ABC):
    """
    Dataclass base that takes in any amount of arguments, but only applies ones that have fields.
    """

    def __init__(self, **kwargs: Dict[str, Any]):
        for key, value in kwargs.items():
            if any(field.name == key for field in dataclasses.fields(type(self))):  # type: ignore
                setattr(self, key, value)
