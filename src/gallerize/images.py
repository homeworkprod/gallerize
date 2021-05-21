"""
gallerize.images
~~~~~~~~~~~~~~~~

Image processing

:Copyright: 2007-2021 Jochen Kupperschmidt
:License: MIT, see LICENSE for details.
"""

from pathlib import Path
import shutil
import subprocess

from .logging import debug
from .models import Dimension, Gallery, Image


def generate_images(gallery: Gallery, resize: bool, optimize: bool) -> None:
    """Generate images for the gallery."""
    for image in gallery.images:
        _generate_image(
            image,
            gallery.destination_path,
            resize,
            gallery.max_image_size,
            optimize,
        )
        _generate_thumbnail(
            image,
            gallery.destination_path,
            gallery.max_thumbnail_size,
            optimize,
        )


def _generate_image(
    image: Image,
    destination_path: Path,
    resize: bool,
    max_size: Dimension,
    optimize: bool,
) -> None:
    """Create an (optionally resized) copy of an image."""
    destination_filename = destination_path / image.filename
    if resize:
        # Resize image.
        debug('Resizing image "{}" ...', image.full_filename)
        _resize_image(image.full_filename, destination_filename, max_size)
    else:
        # Copy image.
        debug('Copying image "{}" ...', image.full_filename)
        shutil.copy(image.full_filename, destination_filename)

    if optimize:
        _optimize_image(destination_filename)


def _generate_thumbnail(
    image: Image, destination_path: Path, max_size: Dimension, optimize: bool
) -> None:
    """Create a small preview image for an image."""
    debug('Creating thumbnail "{}" ...', image.thumbnail_filename)
    destination_filename = destination_path / image.thumbnail_filename
    _resize_image(image.full_filename, destination_filename, max_size)

    if optimize:
        _optimize_image(destination_filename)


def _resize_image(
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


def _optimize_image(filename: Path) -> None:
    """Optimize image and strip EXIF and other non-important metadata."""
    cmd = ['jpegoptim', '--strip-all', str(filename)]
    subprocess.check_call(cmd)
