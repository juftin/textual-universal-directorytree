"""
Pytest Fixtures Shared Across all Unit Tests
"""

import pathlib
from typing import Any, Dict, List

import pytest
from upath import UPath

from tests.helpers import Screenshotter


@pytest.fixture
def repo_dir() -> pathlib.Path:
    """
    Return the path to the repository root
    """
    return pathlib.Path(__file__).parent.parent.resolve()


@pytest.fixture
def screenshot_dir(repo_dir: pathlib.Path) -> pathlib.Path:
    """
    Return the path to the screenshot directory
    """
    return repo_dir / "tests" / "screenshots"


@pytest.fixture
def github_release_path() -> UPath:
    """
    Return the path to the GitHub Release
    """
    release = "v1.0.0"
    uri = f"github://juftin:textual-universal-directorytree@{release}"
    return UPath(uri)


@pytest.fixture(scope="module")
def vcr_config() -> Dict[str, List[Any]]:
    """
    VCR Cassette Privacy Enforcer

    This fixture ensures the API Credentials are obfuscated

    Returns
    -------
    Dict[str, List[Any]]:
        The VCR Config
    """
    return {
        "filter_headers": [("authorization", "XXXXXXXXXX")],
        "filter_query_parameters": [("user", "XXXXXXXXXX"), ("token", "XXXXXXXXXX")],
    }


@pytest.fixture
def screenshotter(github_release_path: UPath) -> Screenshotter:
    """
    Return a Screenshotter

    Parameters
    ----------
    github_release_path : UPath
        The path to the GitHub Release

    Returns
    -------
    Screenshotter:
        The Screenshotter
    """
    return Screenshotter(file_path=github_release_path)


cassette = pytest.mark.vcr(scope="module")
