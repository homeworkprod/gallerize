"""
gallerize.files
~~~~~~~~~~~~~~~

Generic file utilities

:Copyright: 2007-2021 Jochen Kupperschmidt
:License: MIT, see LICENSE for details.
"""

from __future__ import annotations
from collections import defaultdict
from pathlib import Path
from typing import Iterable, Optional

from .logging import debug


def find_duplicate_filenames(
    paths: Iterable[Path],
) -> list[tuple[str, list[Path]]]:
    d = defaultdict(list)
    for path in paths:
        key = path.name.lower()
        d[key].append(path)

    return [item for item in d.items() if len(item[1]) > 1]


def read_first_line(filename: Path) -> Optional[str]:
    """Read the first line from the specified file."""
    try:
        text = filename.read_text(encoding='utf-8')
        first_line = text.splitlines()[0]
        return first_line.strip()
    except IOError:
        # File does not exist (OK) or cannot be read (not really OK).
        return None


def write_file(filename: Path, content: str) -> None:
    debug('Writing "{}" ...', filename)
    filename.write_text(content, encoding='utf-8')
