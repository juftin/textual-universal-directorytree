"""
Textual's Implementation of Pathlib, Powered by fsspec
"""

from __future__ import annotations

from os import getenv
from typing import Any

from upath.implementations.cloud import S3Path
from upath.implementations.github import GitHubPath as UGitHubPath


class GitHubPath(UGitHubPath):
    """
    GitHubPath

    UPath implementation for GitHub to be compatible with
    the Directory Tree
    """

    def __init__(
        self, *args: Any, protocol: str | None = None, **storage_options: Any
    ) -> None:
        """
        Initialize the GitHubPath with GitHub Token Authentication
        """
        if "token" not in storage_options:
            token = getenv("GITHUB_TOKEN")
            if token is not None:
                storage_options.update({"username": "Bearer", "token": token})
        handled_args = args
        if "sha" not in storage_options:
            handled_url = self.handle_github_url(args[0])
            handled_args = (handled_url, *args[1:])
        super().__init__(*handled_args, protocol=protocol, **storage_options)

    def __str__(self) -> str:
        """
        String representation of the GitHubPath
        """
        return (
            f"{self.protocol}://{self.storage_options['org']}:"
            f"{self.storage_options['repo']}@{self.storage_options['sha']}"
        )

    @classmethod
    def handle_github_url(cls, url: str | GitHubPath) -> str:
        """
        Handle GitHub URLs

        GitHub URLs are handled by converting them to the raw URL.
        """
        try:
            import requests
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
            msg = f"Invalid GitHub URL: {url}"
            raise ValueError(msg)
        token = getenv("GITHUB_TOKEN")
        auth = {"auth": ("Bearer", token)} if token is not None else {}
        resp = requests.get(
            f"https://api.github.com/repos/{org}/{repo}",
            headers={"Accept": "application/vnd.github.v3+json"},
            timeout=30,
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
            return f"{self._url.scheme}://{self._url.netloc}"
        else:
            return super().name
