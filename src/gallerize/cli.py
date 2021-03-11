"""
gallerize.cli
~~~~~~~~~~~~~

:Copyright: 2007-2021 Jochen Kupperschmidt
:License: MIT, see LICENSE for details.
"""

import argparse
import sys

from . import VERSION
from .main import (
    create_gallery,
    Dimension,
    generate_gallery,
    handle_duplicate_filenames,
)


ARGS_DEFAULT_MAX_IMAGE_SIZE: str = '1024x1024'
ARGS_DEFAULT_MAX_THUMBNAIL_SIZE: str = '120x120'


def parse_dimension_arg(value: str) -> Dimension:
    """Validate a dimension value."""
    try:
        return Dimension(*map(int, value.split('x', 1)))
    except ValueError:
        raise argparse.ArgumentTypeError(f'invalid dimension value: {value!r}')


def parse_args():
    """Parse command-line arguments."""

    parser = argparse.ArgumentParser(
        usage='%(prog)s [options] <target path> <image> [image] ...'
    )

    parser.add_argument(
        '-c',
        '--captions',
        dest='captions',
        action='store_true',
        default=False,
        help='read image captions from text files ("<IMAGE_NAME>.txt")',
    )

    parser.add_argument(
        '--no-resize',
        dest='no_resize',
        action='store_true',
        default=False,
        help='do not resize images, just copy them',
    )

    parser.add_argument(
        '-s',
        '--size',
        dest='max_image_size',
        type=parse_dimension_arg,
        default=ARGS_DEFAULT_MAX_IMAGE_SIZE,
        help=f'set maximum image size [default: {ARGS_DEFAULT_MAX_IMAGE_SIZE}]',
    )

    parser.add_argument(
        '-t',
        '--thumbnail-size',
        dest='max_thumbnail_size',
        type=parse_dimension_arg,
        default=ARGS_DEFAULT_MAX_THUMBNAIL_SIZE,
        help=f'set maximum thumbnail size [default: {ARGS_DEFAULT_MAX_THUMBNAIL_SIZE}]',
    )

    parser.add_argument(
        '--title', dest='title', help='set gallery title on the website'
    )

    parser.add_argument(
        '--version', action='version', version=f'gallerize {VERSION}'
    )

    # First positional argument.
    parser.add_argument('destination_path')

    # Remaining positional arguments (at least one), as a list.
    parser.add_argument('full_image_filenames', nargs='+')

    return parser.parse_args()


def main():
    try:
        args = parse_args()
        handle_duplicate_filenames(args.full_image_filenames)
        gallery = create_gallery(
            title=args.title,
            destination_path=args.destination_path,
            resize=not args.no_resize,
            max_image_size=args.max_image_size,
            max_thumbnail_size=args.max_thumbnail_size,
            full_image_filenames=args.full_image_filenames,
        )
        generate_gallery(gallery)
    except KeyboardInterrupt:
        sys.exit('Ctrl-C pressed, aborting.')
