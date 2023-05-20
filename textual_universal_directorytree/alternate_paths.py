"""
Textual's Implementation of Pathlib, Powered by fsspec
"""

from os import getenv

from upath import UPath
from upath.implementations.cloud import S3Path


class GitHubPath(UPath):
    """
    GitHubPath

    UPath implementation for GitHub to be compatible with
    the Directory Tree
    """

    def __new__(cls, *args, **kwargs) -> "GitHubPath":  # type: ignore[no-untyped-def]
        """
        Attempt to set the username and token from the environment
        """
        token = getenv("GITHUB_TOKEN")
        if token is not None:
            kwargs.update({"username": "Bearer", "token": token})
        github_path = super().__new__(cls, *args, **kwargs)
        return github_path

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


class S3TextualPath(S3Path):
    """
    S3BrowsrPath
    """

    @property
    def name(self) -> str:
        """
        Override the name for top level repo
        """
        if len(self.parts) == 1 and self.parts[0] == "/":
            return f"{self._url.scheme}://{self._url.netloc}"  # type: ignore[union-attr]
        else:
            return super().name
