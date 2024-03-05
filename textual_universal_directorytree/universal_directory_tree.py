"""
Universal Directory Tree Widget
"""

from textual.widgets import DirectoryTree
from upath import UPath, registry

from textual_universal_directorytree.alternate_paths import GitHubPath, S3TextualPath

registry.register_implementation(protocol="github", cls=GitHubPath, clobber=True)
registry.register_implementation(protocol="s3", cls=S3TextualPath, clobber=True)
registry.register_implementation(protocol="s3a", cls=S3TextualPath, clobber=True)


class UniversalDirectoryTree(DirectoryTree):
    """
    Universal Directory Tree Widget
    """

    PATH = UPath
