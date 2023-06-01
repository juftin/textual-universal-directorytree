"""
Universal Directory Tree Widget
"""

from textual.widgets import DirectoryTree
from upath import UPath, registry

registry._registry.known_implementations[
    "github"
] = "textual_universal_directorytree.alternate_paths.GitHubPath"
registry._registry.known_implementations[
    "s3"
] = "textual_universal_directorytree.alternate_paths.S3TextualPath"
registry._registry.known_implementations[
    "s3a"
] = "textual_universal_directorytree.alternate_paths.S3TextualPath"


class UniversalDirectoryTree(DirectoryTree):
    """
    Universal Directory Tree Widget
    """

    PATH = UPath
