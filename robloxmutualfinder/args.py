import sys
from typing import List

import colorama

from robloxmutualfinder import roblox


class Args:

    user_ids: List[int] = []

    def __init__(self) -> None:
        usernames: List[str] = []

        # take usernames and userIDs from argv
        for i, arg in enumerate(sys.argv):
            if i == 0:
                continue
            if arg.isnumeric():
                self.user_ids.append(int(arg))
            else:
                usernames.append(arg)

        # if there are less than 2 arguments then prompt for the rest of them
        num_users = len(self.user_ids) + len(usernames)

        if num_users < 2:
            # prompt for more users
            for i in range(2 - num_users):
                print(
                    f"{colorama.Fore.LIGHTBLUE_EX}[:] Enter user #{num_users+1+i} (userID or username)"
                )
                uid = input(f"{colorama.Fore.LIGHTBLUE_EX}[:] >")
                if not uid.isnumeric():
                    usernames.append(uid)
                else:
                    self.user_ids.append(int(uid))

        # convert all usernames to userIDs
        if usernames:
            self.user_ids += list(roblox.get_user_ids_from_names(usernames))
