"""
Textual Universal Directory Tree
"""

from .alternate_paths import GitHubPath, S3TextualPath
from .universal_directory_tree import UniversalDirectoryTree
from .utils import is_local_path, is_remote_path

__all__ = [
    "UniversalDirectoryTree",
    "is_local_path",
    "is_remote_path",
    "GitHubPath",
    "S3TextualPath",
]
