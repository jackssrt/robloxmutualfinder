from dataclasses import dataclass, field
from typing import Dict, Generic, Optional, TypeVar


K = TypeVar("K")
V = TypeVar("V")


@dataclass
class DoubleEndedDict(Generic[K, V]):
    """
    Double ended dict, access by key and by value in O(1).
    """

    key_to_value: Dict[K, V] = field(default_factory=dict)
    value_to_key: Dict[V, K] = field(default_factory=dict)

    def __setitem__(self, key, value):
        self.key_to_value[key] = value
        self.value_to_key[value] = key

    def __contains__(self, item):
        return item in self.key_to_value or item in self.value_to_key

    def replace_internal_dicts(
        self, key_to_value: Dict[K, V], value_to_key: Dict[V, K]
    ):
        self.key_to_value = key_to_value
        self.value_to_key = value_to_key

    def get_by_value(self, value: V) -> Optional[K]:
        return self.value_to_key.get(value)

    def get_by_key(self, key: K) -> Optional[V]:
        return self.key_to_value.get(key)

    def remove_by_key(self, key: K):
        if key in self.key_to_value:
            value = self.key_to_value[key]
            del self.key_to_value[key]
            del self.value_to_key[value]
        else:
            raise KeyError("Key not found")

    def remove_by_value(self, value: V):
        if value in self.value_to_key:
            key = self.value_to_key[value]
            del self.value_to_key[value]
            del self.key_to_value[key]
        else:
            raise KeyError("Value not found")
