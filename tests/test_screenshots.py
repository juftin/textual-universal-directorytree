"""
Screenshot Testing
"""

from tests.conftest import cassette
from tests.helpers import Screenshotter


@cassette
def test_github_screenshot(screenshotter: Screenshotter) -> None:
    """
    Snapshot a release of this repo
    """
    screenshot, screenshot_path = screenshotter.take_screenshot(
        press=[
            "wait:3000",
            "down",
            "down",
            "down",
            "down",
            "down",
            "down",
            "down",
            "space",
            "enter",
            "_",
        ]
    )
    assert screenshot_path.read_text() == screenshot
