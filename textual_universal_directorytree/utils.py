"""
Universal Directory Tree Utils
"""

import pathlib

from upath.core import _FSSpecAccessor


def is_remote_path(path: pathlib.Path) -> bool:
    """
    Check if the path is a remote path
    """
    accessor = getattr(path, "_accessor", None)
    return isinstance(accessor, _FSSpecAccessor)


def is_local_path(path: pathlib.Path) -> bool:
    """
    Check if the path is a local path
    """
    return not is_remote_path(path)
