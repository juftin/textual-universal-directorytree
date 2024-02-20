"""
Helpers for the tests
"""

from __future__ import annotations

import pathlib
from os import environ, getenv

from textual._doc import take_svg_screenshot

from textual_universal_directorytree.app import UniversalDirectoryTreeApp


class Screenshotter:
    """
    App Screenshotter
    """

    def __init__(self, file_path: str | pathlib.Path) -> None:
        """
        Initialize the Screenshotter
        """
        self.app = UniversalDirectoryTreeApp(path=str(file_path))

    def take_screenshot(
        self, press: list[str] | None = None
    ) -> tuple[str, pathlib.Path]:
        """
        Take a Screenshot
        """
        screenshot = take_svg_screenshot(
            app=self.app,
            terminal_size=(120, 35),
            press=press or [],
            title=None,
        )
        screenshot_path = self._get_screenshot_path()
        if getenv("REGENERATE_SCREENSHOTS", "0") != "0":
            screenshot_path.write_text(screenshot)
        return screenshot, screenshot_path

    @classmethod
    def _get_screenshot_path(cls) -> pathlib.Path:
        """
        Get the Screenshot Path

        Screenshots are stored in the docs/screenshots directory
        so they can be included in the documentation
        """
        test_dir = pathlib.Path(__file__).parent
        repo_dir = test_dir.parent
        docs_dir = repo_dir / "docs"
        screenshot_dir = docs_dir / "screenshots"
        current_test = environ["PYTEST_CURRENT_TEST"].split("::")[-1].split(" ")[0]
        screenshot_path = screenshot_dir / f"{current_test}.svg"
        return screenshot_path
