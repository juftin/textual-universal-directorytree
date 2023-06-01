"""
Textual's Implementation of Pathlib, Powered by fsspec
"""

from __future__ import annotations

from os import getenv
from typing import Any

from upath import UPath
from upath.core import _FSSpecAccessor
from upath.implementations.cloud import S3Path


class _GitHubAccessor(_FSSpecAccessor):
    """
    FSSpec Accessor for GitHub
    """

    def __init__(self, *args: Any, **kwargs: Any):
        """
        Initialize the GitHub Accessor
        """
        token = getenv("GITHUB_TOKEN")
        if token is not None:
            kwargs.update({"username": "Bearer", "token": token})
        super().__init__(*args, **kwargs)


class GitHubPath(UPath):
    """
    GitHubPath

    UPath implementation for GitHub to be compatible with
    the Directory Tree
    """

    _default_accessor = _GitHubAccessor

    def __new__(cls, path: str | "GitHubPath") -> "GitHubPath":
        """
        New GitHub Path
        """
        file_path = cls.handle_github_url(path)
        return super().__new__(cls, file_path)

    @property
    def path(self) -> str:
        """
        Paths get their leading slash stripped
        """
        return super().path.strip("/")

    @property
    def name(self) -> str:
        """
        Override the name for top level repo
        """
        if self.path == "":
            org = self._accessor._fs.org
            repo = self._accessor._fs.repo
            sha = self._accessor._fs.storage_options["sha"]
            github_name = f"{org}:{repo}@{sha}"
            return github_name
        else:
            return super().name

    @classmethod
    def handle_github_url(cls, url: str | "GitHubPath") -> str:
        """
        Handle GitHub URLs

        GitHub URLs are handled by converting them to the raw URL.
        """
        try:
            import requests  # type: ignore[import]
        except ImportError as e:
            raise ImportError(
                "The requests library is required to browse GitHub files. "
                "Install `textual-universal-directorytree` with the `remote` "
                "extra to install requests."
            ) from e

        url = str(url)
        gitub_prefix = "github://"
        if gitub_prefix in url and "@" not in url:
            _, user_password = url.split("github://")
            org, repo_str = user_password.split(":")
            repo, *args = repo_str.split("/")
        elif gitub_prefix in url and "@" in url:
            return url
        else:
            raise ValueError(f"Invalid GitHub URL: {url}")
        token = getenv("GITHUB_TOKEN")
        auth = {"auth": ("Bearer", token)} if token is not None else {}
        resp = requests.get(
            f"https://api.github.com/repos/{org}/{repo}",
            headers={"Accept": "application/vnd.github.v3+json"},
            **auth,  # type: ignore[arg-type]
        )
        resp.raise_for_status()
        default_branch = resp.json()["default_branch"]
        arg_str = "/".join(args)
        github_uri = f"{gitub_prefix}{org}:{repo}@{default_branch}/{arg_str}".rstrip(
            "/"
        )
        return github_uri


class S3TextualPath(S3Path):
    """
    S3TextualPath
    """

    def _is_top_level_bucket(self) -> bool:
        """
        Check if the path is a top level bucket
        """
        return len(self.parts) == 1 and self.parts[0] == "/"

    @property
    def name(self) -> str:
        """
        Override the name for top level repo
        """
        if self._is_top_level_bucket():
            return f"{self._url.scheme}://{self._url.netloc}"  # type: ignore[union-attr]
        else:
            return super().name
