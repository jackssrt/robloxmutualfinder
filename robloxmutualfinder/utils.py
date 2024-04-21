import sys
import traceback
from typing import Any, Optional, Sequence, Sized
from typing_extensions import Never
from robloxmutualfinder.console import error


def link(url: str, text: str) -> str:
    return f"\033]8;;{url}\033\\{text}\033]8;;\033\\"


def natural_list(items: Sequence[Any]) -> str:
    """
    Returns a natural list of the passed in items.
    For example: eggs, milk and butter
    """
    if len(items) == 1:
        return str(items[0])
    return f"{', '.join(map(str, items[:-1]))} and {items[-1]}"


def pluralize(word: str, obj: Sized) -> str:
    """
    Pluralizes word based on obj.
    """
    return f"{word}{'s' if len(obj) != 1 else ''}"


def handle_error(description: str, additional_data: Optional[Any] = None) -> Never:
    error(description)
    traceback.print_exc()
    if additional_data is not None:
        error(additional_data)
    sys.exit(1)
