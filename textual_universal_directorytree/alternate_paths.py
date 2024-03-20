"""
Textual's Implementation of Pathlib, Powered by fsspec
"""

from __future__ import annotations

import os
import re
from typing import Any

from upath import UPath
from upath.implementations.cloud import S3Path
from upath.implementations.github import GitHubPath


class GitHubTextualPath(GitHubPath):
    """
    GitHubPath

    UPath implementation for GitHub to be compatible with the Directory Tree
    """

    @classmethod
    def _transform_init_args(
        cls,
        args: tuple[str | os.PathLike[Any], ...],
        protocol: str,
        storage_options: dict[str, Any],
    ) -> tuple[tuple[str | os.PathLike[Any], ...], str, dict[str, Any]]:
        """
        Initialize the GitHubPath with GitHub Token Authentication
        """
        if "token" not in storage_options:
            token = os.getenv("GITHUB_TOKEN")
            if token is not None:
                storage_options.update({"username": "Bearer", "token": token})
        handled_args = args
        if "sha" not in storage_options:
            handled_url = cls.handle_github_url(args[0])
            handled_args = (handled_url, *args[1:])
        return handled_args, protocol, storage_options

    def __str__(self) -> str:
        """
        String representation of the GitHubPath
        """
        return (
            f"{self.protocol}://{self.storage_options['org']}:"
            f"{self.storage_options['repo']}@{self.storage_options['sha']}/"
            f"{self.path}"
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
        token = os.getenv("GITHUB_TOKEN")
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
        github_uri = f"{gitub_prefix}{org}:{repo}@{default_branch}/{arg_str}"
        return github_uri

    @property
    def name(self) -> str:
        """
        Override the name for top level repo
        """
        original_name = super().name
        if original_name == "":
            return self.__str__()
        else:
            return original_name


class S3TextualPath(S3Path):
    """
    S3TextualPath
    """

    def _is_top_level_bucket(self) -> bool:
        """
        Check if the path is a top level bucket
        """
        return len(self.parts) == 1 and self.parts[0] == "/"

    def __str__(self) -> str:
        """
        String representation of the S3Path
        """
        return re.sub(r"s3:/*", "s3://", super().__str__())

    @property
    def name(self) -> str:
        """
        Override the name for top level repo
        """
        original_name = super().name
        if self._is_top_level_bucket():
            return f"{self._url.scheme}://{self._url.netloc}"
        elif original_name == "":
            return self.__str__()
        else:
            return original_name


class SFTPTextualPath(UPath):
    """
    SFTPTextualPath
    """

    @property
    def path(self) -> str:
        """
        Always return the path relative to the root
        """
        pth = super().path
        if pth.startswith("."):
            return f"/{pth[1:]}"
        elif pth.startswith("/"):
            return pth
        else:
            return "/" + pth

    def __str__(self) -> str:
        """
        Add the protocol prefix + extras to the string representation
        """
        string_representation = f"{self.protocol}://"
        if "username" in self.storage_options:
            string_representation += f"{self.storage_options['username']}@"
        string_representation += f"{self.storage_options['host']}"
        if "port" in self.storage_options:
            string_representation += f":{self.storage_options['port']}"
        string_representation += self.path
        return string_representation

    @property
    def name(self) -> str:
        """
        Override the name for top level repo
        """
        original_name = super().name
        if original_name == "":
            return self.__str__()
        else:
            return original_name
