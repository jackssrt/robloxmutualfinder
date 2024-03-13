from typing import Any

import colorama


def error(arg: Any, *args):
    print(f"{colorama.Fore.LIGHTRED_EX}[!]", arg, *args)


def debug(arg: Any, *args):
    print(f"{colorama.Fore.LIGHTBLACK_EX}[D] {arg} {' '.join([str(x) for x in args])}")
