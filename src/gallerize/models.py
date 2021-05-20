"""
gallerize.models
~~~~~~~~~~~~~~~~

:Copyright: 2007-2021 Jochen Kupperschmidt
:License: MIT, see LICENSE for details.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Dimension:
    width: int
    height: int


@dataclass(frozen=True)
class Image:
    full_filename: str
    path: str
    filename: str
    thumbnail_filename: str
    page_name: str
    caption: Optional[str] = None
    previous_image: Optional[Image] = None
    next_image: Optional[Image] = None


@dataclass(frozen=True)
class Gallery:
    title: str
    destination_path: str
    resize: bool
    max_image_size: Dimension
    max_thumbnail_size: Dimension
    images: list[Image]
