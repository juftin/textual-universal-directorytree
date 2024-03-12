"""
Universal Directory Tree Utils
"""

import pathlib

from upath import UPath
from upath.implementations.local import LocalPath


def is_local_path(path: pathlib.Path) -> bool:
    """
    Check if the path is a local path
    """
    return isinstance(path, LocalPath)


def is_remote_path(path: UPath) -> bool:
    """
    Check if the path is a remote path
    """
    return not is_local_path(path)
