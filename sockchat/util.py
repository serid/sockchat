from typing import Tuple, TypeVar, Callable


def split_first(s: str, separator: str) -> Tuple[str, str]:
    index = s.index(separator)
    return s[:index], s[index + 1:]


def remove_prefix(s: str, prefix: str) -> str | None:
    if s.startswith(prefix):
        return s[len(prefix):]
    return None


T = TypeVar("T")
U = TypeVar("U")


def apply_if_some(f: Callable[[T], U], option: T | None) -> U | None:
    if option is None:
        return None
    return f(option)
