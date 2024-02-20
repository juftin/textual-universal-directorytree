import argparse
from typing import Any, ClassVar, List

import upath
from rich.syntax import Syntax
from textual import on
from textual.app import App, ComposeResult
from textual.binding import BindingType
from textual.containers import Horizontal, VerticalScroll
from textual.widgets import DirectoryTree, Footer, Header, Static

from textual_universal_directorytree import UniversalDirectoryTree


class UniversalDirectoryTreeApp(App):
    """
    The power of upath and fsspec in a Textual app
    """

    BINDINGS: ClassVar[List[BindingType]] = [
        ("q", "quit", "Quit"),
    ]

    def __init__(self, path: str, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self.universal_path = path
        self.file_content = Static()

    def compose(self) -> ComposeResult:
        yield Header()
        directory_tree = UniversalDirectoryTree(path=self.universal_path)
        yield Horizontal(directory_tree, VerticalScroll(self.file_content))
        yield Footer()

    @on(DirectoryTree.FileSelected)
    def handle_file_selected(self, message: DirectoryTree.FileSelected) -> None:
        """
        Do something with the selected file.

        Objects returned by the FileSelected event are upath.UPath objects and
        they are compatible with the familiar pathlib.Path API built into Python.
        """
        selected_file_path = message.path
        file_content = selected_file_path.read_text(errors="replace")
        lexer = Syntax.guess_lexer(path=str(selected_file_path))
        code = Syntax(code=file_content, lexer=lexer)
        self.file_content.update(code)


def cli() -> None:
    """
    Command Line Interface for the example App
    """
    parser = argparse.ArgumentParser(description="Universal Directory Tree")
    parser.add_argument("path", type=str, help="Path to open", default=".")
    args = parser.parse_args()
    file_path = str(upath.UPath(args.path).resolve()).rstrip("/")
    app = UniversalDirectoryTreeApp(path=file_path)
    app.run()


if __name__ == "__main__":
    cli()
