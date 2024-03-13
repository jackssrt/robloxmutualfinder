from abc import ABC
import dataclasses


class DynamicDataclass(ABC):
    """
    Dataclass base that takes in any amount of arguments, but only applies ones that have fields.
    """

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if any(field.name == key for field in dataclasses.fields(type(self))):
                setattr(self, key, value)
