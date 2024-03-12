"""
Test utils
"""

from textual_universal_directorytree import UPath
from textual_universal_directorytree.alternate_paths import (
    GitHubTextualPath,
    S3TextualPath,
)
from textual_universal_directorytree.utils import is_local_path, is_remote_path


def test_is_local_path() -> None:
    """
    Test is_local_path + is_remote_path
    """
    local_tests_dir = UPath("tests")
    assert is_local_path(local_tests_dir) is True
    assert is_remote_path(local_tests_dir) is False
    local_dot_dir = UPath(".")
    assert is_local_path(local_dot_dir) is True
    assert is_remote_path(local_dot_dir) is False
    github_path = UPath("github://juftin:textual-universal-directorytree@main")
    assert is_local_path(github_path) is False
    assert is_remote_path(github_path) is True
    assert isinstance(github_path, GitHubTextualPath)
    s3_path = UPath("s3://bucket/key")
    assert is_local_path(s3_path) is False
    assert is_remote_path(s3_path) is True
    assert isinstance(s3_path, S3TextualPath)
