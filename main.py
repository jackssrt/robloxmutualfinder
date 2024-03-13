from typing import Set, Tuple

import colorama
from tabulate import tabulate

from robloxmutualfinder import roblox
from robloxmutualfinder.args import Args
from robloxmutualfinder.utils import link, natural_list, pluralize

colorama.init(True)


def main() -> None:
    # collect the args
    args = Args()
    print(
        f"{colorama.Fore.LIGHTMAGENTA_EX}Fetching friends for {natural_list(tuple(roblox.get_names_from_user_ids(args.user_ids)))}..."
    )

    # get friends of all users
    each_users_friends = {i: roblox.get_user_friends(i) for i in args.user_ids}
    each_users_friends_tuple = tuple(each_users_friends.values())

    # calculate mutuals
    # can't use the & operator here
    mutuals = set(each_users_friends_tuple[0]).intersection(
        *each_users_friends_tuple[1:]
    )  # yes, it's really that simple :P

    # calculate friendship statuses between the users
    are_friends: Set[Tuple[int, int]] = set()
    are_not_friends: Set[Tuple[int, int]] = set()
    for my_id, my_friends in each_users_friends.items():
        for other_user_id in each_users_friends.keys():
            if (
                other_user_id == my_id
                or (other_user_id, my_id) in are_friends
                or (other_user_id, my_id) in are_not_friends
            ):
                # link is self referencing or already processed this link
                continue

            # add the link
            if any(friend.id == other_user_id for friend in my_friends):
                are_friends.add((my_id, other_user_id))
            else:
                are_not_friends.add((my_id, other_user_id))

    # display output
    print()
    print("---- Results ----")

    ## print friends
    for me, other in are_friends:
        me_username, other_username = roblox.get_names_from_user_ids([me, other])
        print(
            f"{colorama.Fore.LIGHTGREEN_EX}{link(roblox.profile_url(me), me_username)} and {link(roblox.profile_url(other),other_username)} are friends"
        )

    ## print non-friends
    for me, other in are_not_friends:
        me_username, other_username = roblox.get_names_from_user_ids([me, other])

        print(
            f"{colorama.Fore.LIGHTRED_EX}{link(roblox.profile_url(me), me_username)} and {link(roblox.profile_url(other),other_username)} aren't friends"
        )

    ## mutuals table
    print(
        f"{colorama.Fore.LIGHTGREEN_EX if mutuals else colorama.Fore.LIGHTRED_EX}Found {len(mutuals)} {pluralize('mutual friend', mutuals)}{' :(' if not mutuals else ''}"
    )
    if mutuals:
        print(
            tabulate(
                (
                    (
                        i + 1,
                        link(roblox.profile_url(mutual.id), mutual.displayName),
                        link(roblox.profile_url(mutual.id), mutual.name),
                        link(roblox.profile_url(mutual.id), str(mutual.id)),
                    )
                    for i, mutual in enumerate(mutuals)
                ),
                headers=("#", "Display Name", "Username", "UserID"),
                disable_numparse=True,
                tablefmt="presto",
            )
        )


if __name__ == "__main__":
    main()
