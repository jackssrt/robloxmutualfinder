from typing import Dict, Generic, Optional, TypeVar

from robloxmutualfinder.double_ended_dict import DoubleEndedDict


K = TypeVar("K")


class StringDoubleEndedDict(Generic[K], DoubleEndedDict[K, str]):
    """
    Modified version of DoubleEndedDict to have case insensitive string values.
    """

    def __setitem__(self, key, value):
        self.key_to_value[key] = value
        self.value_to_key[value.lower()] = key

    def get_by_value(self, value: str) -> Optional[K]:
        return self.value_to_key.get(value.lower())

    def remove_by_value(self, value: str):
        if value.lower() in self.value_to_key:
            key = self.value_to_key[value.lower()]
            del self.value_to_key[value.lower()]
            del self.key_to_value[key]
        else:
            raise KeyError("Value not found")

    def replace_internal_dicts(
        self, key_to_value: Dict[K, str], value_to_key: Dict[str, K]
    ):
        self.key_to_value = key_to_value
        self.value_to_key = {v.lower(): k for v, k in value_to_key.items()}
