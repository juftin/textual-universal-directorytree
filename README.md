<h1 align="center">textual-universal-directorytree</h1>

<div align="center">
  <a href="https://github.com/juftin/textual-universal-directorytree">
    <img src="docs/screenshots/test_github_screenshot.svg" alt="textual-universal-directorytree" />
  </a>
</div>

<p align="center">
<a href="https://textual.textualize.io/widgets/directory_tree/">DirectoryTree</a> widget for <a href="https://textual.textualize.io/">textual</a>, compatible with all filesystems
</p>

<p align="center">
  <a href="https://github.com/juftin/textual-universal-directorytree"><img src="https://img.shields.io/pypi/v/textual-universal-directorytree?color=blue&label=%F0%9F%93%81%20textual-universal-directorytree" alt="PyPI"></a>
  <a href="https://pypi.python.org/pypi/textual-universal-directorytree/"><img src="https://img.shields.io/pypi/pyversions/textual-universal-directorytree" alt="PyPI - Python Version"></a>
  <a href="https://github.com/juftin/textual-universal-directorytree/blob/main/LICENSE"><img src="https://img.shields.io/github/license/juftin/textual-universal-directorytree?color=blue&label=License" alt="GitHub License"></a>
  <a href="https://juftin.github.io/textual-universal-directorytree/"><img src="https://img.shields.io/static/v1?message=docs&color=526CFE&logo=Material+for+MkDocs&logoColor=FFFFFF&label=" alt="docs"></a>
  <a href="https://github.com/juftin/textual-universal-directorytree/actions/workflows/tests.yaml?query=branch%3Amain"><img src="https://github.com/juftin/textual-universal-directorytree/actions/workflows/tests.yaml/badge.svg?branch=main" alt="Testing Status"></a>
  <a href="https://github.com/pypa/hatch"><img src="https://img.shields.io/badge/%F0%9F%A5%9A-Hatch-4051b5.svg" alt="Hatch project"></a>
  <a href="https://github.com/astral-sh/ruff"><img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json" alt="Ruff"></a>
  <a href="https://github.com/pre-commit/pre-commit"><img src="https://img.shields.io/badge/pre--commit-enabled-lightgreen?logo=pre-commit" alt="pre-commit"></a>
  <a href="https://github.com/semantic-release/semantic-release"><img src="https://img.shields.io/badge/%20%20%F0%9F%93%A6%F0%9F%9A%80-semantic--release-e10079.svg" alt="semantic-release"></a>
  <a href="https://gitmoji.dev"><img src="https://img.shields.io/badge/gitmoji-%20😜%20😍-FFDD67.svg" alt="Gitmoji"></a>
</p>

## Installation

```shell
pip install textual-universal-directorytree
```

### Extra Dependencies

Some filesystems require additional dependencies to be installed.
The `remote` extra includes all the known optional dependencies. See the
[Filesystems Supported](#filesystems-supported) section for more information.

```shell
pip install "textual-universal-directorytree[remote]"
```

## Usage

The below example shows how to use `textual-universal-directorytree` in a Textual app.
It uses the GitHub filesystem to display the contents of the textual GitHub repository.
It requires the `requests` library to be installed (or the `remote` extra).

```python
from __future__ import annotations

from typing import Any, ClassVar

from rich.syntax import Syntax
from textual import on
from textual.app import App, ComposeResult
from textual.binding import BindingType
from textual.containers import Horizontal, VerticalScroll
from textual.widgets import DirectoryTree, Footer, Header, Static

from textual_universal_directorytree import UniversalDirectoryTree, UPath


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
```

Run the above app in your terminal:

```python
python -m textual_universal_directorytree github://juftin:textual-universal-directorytree@main/
```

## Filesystems Supported

`textual-universal-directorytree` leverages [fsspec](https://github.com/fsspec/filesystem_spec) and
[universal_pathlib](https://github.com/fsspec/universal_pathlib) to enable compatibility with
local and remote filesystems.

In some cases you need to install a filesystem-specific library
to enable compatibility with that filesystem. For example, to enable compatibility with AWS S3 you must
install [s3fs](https://github.com/fsspec/s3fs) which is an `fsspec` implementation for S3.

The following filesystems are known to be supported by `textual-universal-directorytree`, but it's possible
that [others filesystems](https://filesystem-spec.readthedocs.io/en/latest/api.html#other-known-implementations)
are supported as well and just haven't been tested. If you find a filesystem that works, please open an issue.

| File System     | Format                            | Optional Dependencies                            |
| --------------- | --------------------------------- | ------------------------------------------------ |
| Local           | `path/to/file`                    | None                                             |
| Local           | `file://path/to/file`             | None                                             |
| AWS S3          | `s3://bucket/path`                | [s3fs](https://github.com/fsspec/s3fs)           |
| AWS S3          | `s3a://bucket/path`               | [s3fs](https://github.com/fsspec/s3fs)           |
| Google GCS      | `gs://bucket/path`                | [gcsfs](https://github.com/fsspec/gcsfs)         |
| Azure Data Lake | `adl://bucket/path`               | [adlfs](https://github.com/fsspec/adlfs)         |
| Azure Blob      | `abfs://bucket/path`              | [adlfs](https://github.com/fsspec/adlfs)         |
| Azure Blob      | `az://bucket/path`                | [adlfs](https://github.com/fsspec/adlfs)         |
| GitHub          | `github://owner:repo@branch`      | [requests](https://github.com/requests/requests) |
| GitHub          | `github://owner:repo@branch/path` | [requests](https://github.com/requests/requests) |
| SSH             | `ssh://user@host:port/path`       | [paramiko](https://github.com/paramiko/paramiko) |
| SFTP            | `sftp://user@host:port/path`      | [paramiko](https://github.com/paramiko/paramiko) |

## License

`textual-universal-directorytree` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html)
license.
