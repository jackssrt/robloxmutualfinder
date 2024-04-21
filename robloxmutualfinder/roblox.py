import dataclasses
import json
from pathlib import Path
from typing import Any, Dict, List, Union, cast

import httpx

from robloxmutualfinder.dynamic_dataclass import DynamicDataclass
from robloxmutualfinder.console import debug
from robloxmutualfinder.string_double_ended_dict import StringDoubleEndedDict
from robloxmutualfinder.utils import handle_error, natural_list, pluralize


@dataclasses.dataclass(init=False)
class Friend(DynamicDataclass):
    """
    A friend :D
    """

    id: int
    name: str
    displayName: str

    def __hash__(self) -> int:
        return self.id

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Friend):
            raise TypeError
        return self.id == other.id


def profile_url(user_id: Union[int, str]):
    return f"https://www.roblox.com/users/{user_id}/profile"


# initialize the username and userID cache
cache_path = Path("username_cache.json")
user_id_to_username_cache: StringDoubleEndedDict[str] = StringDoubleEndedDict()
try:
    if cache_path.exists():
        with cache_path.open("r") as f:
            file_contents = json.load(f)
            user_id_to_username_cache.replace_internal_dicts(
                file_contents, {v: k for k, v in file_contents.items()}
            )
            assert user_id_to_username_cache.value_to_key
            assert user_id_to_username_cache.key_to_value
except Exception as e:
    handle_error("Error reading the username and userID cache from disk")


def save_cache():
    """
    Saves the username and userID cache to disk.
    """

    with cache_path.open("w") as f:
        json.dump(user_id_to_username_cache.key_to_value, f)


def cache_user(username: str, user_id: Union[int, str]) -> None:
    """
    Caches a given user's username and userId.
    Remember to call save_cache() after using this.
    """

    user_id_to_username_cache[str(user_id)] = username


def get_user_ids_from_names(names: List[str]):
    """
    Gets the userIDs for the passed list of usernames.
    """

    # lower case all names
    names = [i.lower() for i in names]
    ids: Dict[int, int] = {}

    # early return for empty names list
    if not names:
        return ids.values()  # always empty, used for typehints

    # check the cache
    names_to_request = names.copy()
    for i, x in enumerate(names):
        cached_id = user_id_to_username_cache.get_by_value(x.lower())
        if cached_id:
            ids[i] = int(cached_id)
            # remove the name from the list
            names_to_request.remove(x.lower())

    # check if all requested users were in the cache
    if not names_to_request:
        return ids.values()

    # fetch userIDs from roblox
    debug(f"Fetching the userIDs of {natural_list(names_to_request)}")
    req = cast(None, Dict[str, Any])  # lie about the type of req
    try:
        req = httpx.post(
            "https://users.roblox.com/v1/usernames/users",
            json={"usernames": names_to_request, "excludeBannedUsers": False},
        ).json()
        assert req["data"]
    except Exception:
        handle_error(
            f"Error fetching {pluralize('userID', names_to_request)} of {natural_list(names_to_request)}",
            req,
        )

    # process the received user_ids and update the cache
    for x in req["data"]:
        username = str(cast(Dict[str, str], x)["name"])
        id = int(cast(Dict[str, str], x)["id"])
        ids[names.index(username.lower())] = id
        cache_user(username, id)
    save_cache()

    return ids.values()


def get_names_from_user_ids(ids: List[int]):
    """
    Gets the usernames for the passed list of userIDs.
    """

    names: Dict[int, str] = {}

    # early return for empty ids
    if not ids:
        return names.values()  # always empty, used for typehints

    # check the cache
    ids_to_request = ids.copy()
    for i, x in enumerate(ids):
        cached_name = user_id_to_username_cache.get_by_key(str(x))
        if cached_name:
            names[i] = cached_name
            # remove the id from the list
            ids_to_request.remove(x)

    # check if all requested users were in the cache
    if not ids_to_request:
        return names.values()

    # fetch usernames from roblox
    debug(f"Fetching the usernames of {natural_list(ids_to_request)}")
    req = cast(None, Dict[str, Any])  # lie about the type of req
    try:
        req = httpx.post(
            "https://users.roblox.com/v1/users",
            json={"userIds": ids_to_request, "excludeBannedUsers": False},
        ).json()
        assert req["data"]
    except Exception:
        handle_error(
            f"Error fetching {pluralize('username', ids_to_request)} of {natural_list(ids_to_request)}",
            req,
        )

    # process the received usernames and update the cache
    for x in req["data"]:
        id = int(cast(Dict[str, str], x)["id"])
        username = str(cast(Dict[str, str], x)["name"])
        names[ids.index(id)] = username
        cache_user(username, id)
    save_cache()

    return names.values()


def get_user_friends(user_id: int) -> List[Friend]:
    """
    Fetches a user's friends
    """

    # fetch the friends
    req = cast(None, Dict[str, Any])  # lie about the type of req
    try:
        req = httpx.get(
            f"https://friends.roblox.com/v1/users/{user_id}/friends?userSort=Alphabetical"
        ).json()
    except Exception:
        handle_error(f"Error fetching userID {user_id}'s friends", req)

    # construct Friend instances
    friends = [Friend(**x) for x in req["data"]]

    # update the username and userID cache
    for x in friends:
        cache_user(x.name, x.id)
    save_cache()

    return friends
