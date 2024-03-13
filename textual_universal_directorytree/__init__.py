"""
Textual Universal Directory Tree
"""

from upath import UPath, registry

from textual_universal_directorytree.alternate_paths import (
    GitHubTextualPath,
    S3TextualPath,
    SFTPTextualPath,
)
from textual_universal_directorytree.universal_directory_tree import (
    UniversalDirectoryTree,
)
from textual_universal_directorytree.utils import is_local_path, is_remote_path

registry.register_implementation(protocol="github", cls=GitHubTextualPath, clobber=True)
registry.register_implementation(protocol="s3", cls=S3TextualPath, clobber=True)
registry.register_implementation(protocol="s3a", cls=S3TextualPath, clobber=True)
registry.register_implementation(protocol="ssh", cls=SFTPTextualPath, clobber=True)
registry.register_implementation(protocol="sftp", cls=SFTPTextualPath, clobber=True)

__all__ = [
    "UniversalDirectoryTree",
    "is_local_path",
    "is_remote_path",
    "GitHubTextualPath",
    "S3TextualPath",
    "UPath",
    "SFTPTextualPath",
]
