from typing import Any, Tuple

import colorama


def error(arg: Any, *args: Tuple[Any, ...]):
    print(f"{colorama.Fore.LIGHTRED_EX}[!]", arg, *args)


def debug(arg: Any, *args: Tuple[Any, ...]):
    print(f"{colorama.Fore.LIGHTBLACK_EX}[D] {arg} {' '.join([str(x) for x in args])}")
