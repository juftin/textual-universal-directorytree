"""
Textual Universal Directory Tree
"""

from textual_universal_directorytree.alternate_paths import GitHubPath, S3TextualPath
from textual_universal_directorytree.universal_directory_tree import (
    UniversalDirectoryTree,
)
from textual_universal_directorytree.utils import is_local_path, is_remote_path

__all__ = [
    "UniversalDirectoryTree",
    "is_local_path",
    "is_remote_path",
    "GitHubPath",
    "S3TextualPath",
]
