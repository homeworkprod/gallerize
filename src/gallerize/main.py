"""
gallerize.main
~~~~~~~~~~~~~~

:Copyright: 2007-2021 Jochen Kupperschmidt
:License: MIT, see LICENSE for details.
"""

from __future__ import annotations
import dataclasses
from itertools import islice
from pathlib import Path
import shutil
import subprocess
import sys
from typing import Iterable, Iterator, Optional

from .files import find_duplicate_filenames, read_first_line, write_file
from .html import render_html_pages
from .logging import debug
from .models import Dimension, Gallery, Image


IMAGE_CAPTION_EXTENSION: str = '.txt'

PATH_STATIC: Path = Path(__file__).parent / 'static'


def resize_image(
    src_filename: Path, dst_filename: Path, max_dimension: Dimension
) -> None:
    """Create a resized (and antialiased) version of an image."""
    dimension_str = f'{max_dimension.width:d}x{max_dimension.height:d}'
    cmd = [
        'convert',
        '-resize',
        dimension_str,
        str(src_filename),
        str(dst_filename),
    ]
    subprocess.check_call(cmd)


def create_gallery(
    title: str,
    destination_path: Path,
    resize: bool,
    max_image_size: Dimension,
    max_thumbnail_size: Dimension,
    full_image_filenames: list[Path],
) -> Gallery:
    images = [create_image(image) for image in sorted(full_image_filenames)]
    images = list(link_images(images))

    return Gallery(
        title=title,
        destination_path=destination_path,
        resize=resize,
        max_image_size=max_image_size,
        max_thumbnail_size=max_thumbnail_size,
        images=images,
    )


def link_images(images: list[Image]) -> Iterator[Image]:
    """Assign the predecessor and successor for every image."""
    for previous_image, image, next_image in window(images):
        yield dataclasses.replace(
            image,
            previous_image=previous_image,
            next_image=next_image,
        )


def generate_gallery(gallery: Gallery) -> None:
    # Create destination path if it doesn't exist.
    if not gallery.destination_path.exists():
        debug(
            'Destination path "{}" does not exist, creating it.',
            gallery.destination_path,
        )
        gallery.destination_path.mkdir()

    gallery = add_image_captions(gallery)
    generate_images(gallery)
    render_html_pages(gallery)
    copy_additional_static_files(gallery.destination_path)
    debug('Done.')


def add_image_captions(gallery: Gallery) -> Gallery:
    captioned_images = [
        dataclasses.replace(image, caption=load_caption(image))
        for image in gallery.images
    ]

    return dataclasses.replace(gallery, images=captioned_images)


def generate_images(gallery: Gallery) -> None:
    for image in gallery.images:
        generate_image(image, gallery)
        generate_thumbnail(image, gallery)


def copy_additional_static_files(destination_path: Path) -> None:
    if not PATH_STATIC.exists():
        debug(
            'Path "{}", does not exist; not copying any static files.',
            PATH_STATIC,
        )
        return

    filenames = list(sorted(PATH_STATIC.iterdir()))
    if not filenames:
        debug('No static files to copy.')
        return

    for filename in filenames:
        debug('Copying static file "{}" ...', filename)
        source = PATH_STATIC / filename
        destination = destination_path / filename
        shutil.copy(source, destination_path)


def window(
    images: Iterable[Image],
) -> Iterator[tuple[Optional[Image], Image, Optional[Image]]]:
    """Return a sliding window over the images.

    Returns a triple. Its first and third element can be `None`, but the
    second element never is.
    """
    n = 3
    padded_list: list[Optional[Image]] = list(images)
    padded_list.insert(0, None)
    padded_list.append(None)

    it = iter(padded_list)
    result = tuple(islice(it, n))

    if len(result) == n:
        yield result  # type: ignore

    for elem in it:
        result = result[1:] + (elem,)
        yield result  # type: ignore


def create_image(full_filename: Path) -> Image:
    basename = full_filename.stem
    extension = full_filename.suffix

    thumbnail_filename = f'{basename}_t{extension}'

    return Image(
        full_filename=full_filename,
        path=full_filename.parent,
        filename=full_filename.name,
        thumbnail_filename=thumbnail_filename,
        page_name=basename,
    )


def generate_image(image: Image, gallery: Gallery) -> None:
    """Create a (optionally resized) copy of an image."""
    destination_filename = gallery.destination_path / image.filename
    if gallery.resize:
        # Resize image.
        debug('Resizing image "{}" ...', image.full_filename)
        resize_image(
            image.full_filename,
            destination_filename,
            gallery.max_image_size,
        )
    else:
        # Copy image.
        debug('Copying image "{}" ...', image.full_filename)
        shutil.copy(image.full_filename, destination_filename)


def generate_thumbnail(image: Image, gallery: Gallery) -> None:
    """Create a preview of an image."""
    debug('Creating thumbnail "{}" ...', image.thumbnail_filename)
    destination_filename = gallery.destination_path / image.thumbnail_filename
    resize_image(
        image.full_filename,
        destination_filename,
        gallery.max_thumbnail_size,
    )


def load_caption(image: Image) -> Optional[str]:
    """Load image caption from file."""
    filename = image.path / (image.filename + IMAGE_CAPTION_EXTENSION)
    return read_first_line(filename)


# -------------------------------------------------------------------- #


def handle_duplicate_filenames(paths: Iterable[Path]) -> None:
    duplicates = find_duplicate_filenames(paths)
    if not duplicates:
        return

    print('Found duplicate filenames:')
    for filename, paths in duplicates:
        print(f'  + "{filename}" appears in the following paths:')
        for path in paths:
            print(f'    - {path}')

    sys.exit('Clashing target filenames, aborting.')
