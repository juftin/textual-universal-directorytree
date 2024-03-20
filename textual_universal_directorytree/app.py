"""
Example Universal Directory Tree App
"""

from __future__ import annotations

import argparse
import os
from typing import Any, ClassVar

from rich.syntax import Syntax
from textual import on
from textual.app import App, ComposeResult
from textual.binding import BindingType
from textual.containers import Horizontal, VerticalScroll
from textual.widgets import DirectoryTree, Footer, Header, Static
from upath import UPath

from textual_universal_directorytree import UniversalDirectoryTree


class UniversalDirectoryTreeApp(App):
    """
    The power of upath and fsspec in a Textual app
    """

    TITLE = "UniversalDirectoryTree"

    CSS = """
    UniversalDirectoryTree {
        max-width: 50%;
        width: auto;
        height: 100%;
        dock: left;
    }
    """

    BINDINGS: ClassVar[list[BindingType]] = [
        ("q", "quit", "Quit"),
    ]

    def __init__(self, path: str | UPath, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self.universal_path = UPath(path).resolve()
        self.directory_tree = UniversalDirectoryTree(path=self.universal_path)
        self.file_content = Static(expand=True)

    def compose(self) -> ComposeResult:
        yield Header()
        yield Horizontal(self.directory_tree, VerticalScroll(self.file_content))
        yield Footer()

    @on(DirectoryTree.FileSelected)
    def handle_file_selected(self, message: DirectoryTree.FileSelected) -> None:
        """
        Do something with the selected file.

        Objects returned by the FileSelected event are upath.UPath objects and
        they are compatible with the familiar pathlib.Path API built into Python.
        """
        self.sub_title = str(message.path)
        try:
            file_content = message.path.read_text()
        except UnicodeDecodeError:
            self.file_content.update("")
            return None
        lexer = Syntax.guess_lexer(path=message.path.name, code=file_content)
        code = Syntax(code=file_content, lexer=lexer)
        self.file_content.update(code)


def cli() -> None:
    """
    Command Line Interface for the example App
    """
    parser = argparse.ArgumentParser(description="Universal Directory Tree")
    parser.add_argument("path", type=str, help="Path to open", default=".")
    args = parser.parse_args()
    cli_app = UniversalDirectoryTreeApp(path=args.path)
    cli_app.run()


app = UniversalDirectoryTreeApp(path=os.getenv("UDT_PATH", os.getcwd()))

if __name__ == "__main__":
    cli()
