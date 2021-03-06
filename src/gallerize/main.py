"""
gallerize.main
~~~~~~~~~~~~~~

:Copyright: 2007-2021 Jochen Kupperschmidt
:License: MIT, see LICENSE for details.
"""

from __future__ import annotations
from collections import defaultdict
import dataclasses
from dataclasses import dataclass
from itertools import islice
import os
from pathlib import Path
import shutil
import subprocess
import sys
from typing import (
    Any,
    Dict,
    Iterable,
    Iterator,
    List,
    Optional,
    Sequence,
    Tuple,
)

from jinja2 import Environment, PackageLoader


IMAGE_CAPTION_EXTENSION: str = '.txt'
TEMPLATE_EXTENSION: str = '.html'
OUTPUT_HTML_EXTENSION: str = '.html'

PATH: str = os.path.dirname(os.path.abspath(__file__))
PATH_STATIC: str = os.path.join(PATH, 'static')
TEMPLATE_ENVIRONMENT: Environment = Environment(
    autoescape=True,
    loader=PackageLoader(__package__, 'templates'),
    trim_blocks=False,
)


@dataclass(frozen=True)
class Dimension:
    width: int
    height: int


def debug(message: str, *args: Any) -> None:
    print(message.format(*args))


def resize_image(
    src_filename: str, dst_filename: str, max_dimension: Dimension
) -> None:
    """Create a resized (and antialiased) version of an image."""
    dimension_str = f'{max_dimension.width:d}x{max_dimension.height:d}'
    cmd = ['convert', '-resize', dimension_str, src_filename, dst_filename]
    subprocess.check_call(cmd)


def render_html_to_file(
    template_name: str, context: Dict[str, Any], path: str, page_name: str
) -> None:
    """Render the template and write the result to the given file."""
    context['url_for_page'] = lambda page: page + OUTPUT_HTML_EXTENSION
    html = render_template(template_name + TEMPLATE_EXTENSION, **context)

    filename = os.path.join(path, page_name + OUTPUT_HTML_EXTENSION)
    write_file(filename, html)


def render_template(template_filename: str, **context: Dict[str, Any]) -> str:
    return TEMPLATE_ENVIRONMENT.get_template(template_filename).render(context)


def write_file(filename: str, content: str) -> None:
    debug('Writing "{}" ...', filename)
    Path(filename).write_text(content, encoding='utf-8')


def create_gallery(
    title: str,
    destination_path: str,
    resize: bool,
    max_image_size: Dimension,
    max_thumbnail_size: Dimension,
    full_image_filenames: List[str],
) -> Gallery:
    gallery = Gallery(
        title=title,
        destination_path=destination_path,
        resize=resize,
        max_image_size=max_image_size,
        max_thumbnail_size=max_thumbnail_size,
    )

    gallery.images = [
        create_image(gallery, image) for image in sorted(full_image_filenames)
    ]
    link_images(gallery.images)

    return gallery


@dataclass
class Gallery:
    title: str
    destination_path: str
    resize: bool
    max_image_size: Dimension
    max_thumbnail_size: Dimension
    images: List[Image] = dataclasses.field(default_factory=list)


def link_images(images: List[Image]) -> None:
    """Assign the predecessor and successor for every image."""
    for previous_image, image, next_image in window(images):
        image.previous_image = previous_image
        image.next_image = next_image


def generate_gallery(gallery: Gallery) -> None:
    # Create destination path if it doesn't exist.
    if not os.path.exists(gallery.destination_path):
        debug(
            'Destination path "{}" does not exist, creating it.',
            gallery.destination_path,
        )
        os.mkdir(gallery.destination_path)

    generate_images(gallery)
    render_html_pages(gallery)
    copy_additional_static_files(gallery.destination_path)
    debug('Done.')


def generate_images(gallery: Gallery) -> None:
    for image in gallery.images:
        generate_image(image, gallery)
        generate_thumbnail(image, gallery)
        image.caption = load_caption(image)


def render_html_pages(gallery: Gallery) -> None:
    for image in gallery.images:
        render_html_page(image, gallery.destination_path)
    render_html_index_page(gallery)


def render_html_index_page(gallery: Gallery) -> None:
    """Create an HTML document of thumbnails that link to single image
    documents.
    """
    context = {'gallery': gallery}
    render_html_to_file('index', context, gallery.destination_path, 'index')


def copy_additional_static_files(destination_path: str) -> None:
    if not os.path.exists(PATH_STATIC):
        debug(
            'Path "{}", does not exist; not copying any static files.',
            PATH_STATIC,
        )
        return

    filenames = list(sorted(os.listdir(PATH_STATIC)))
    if not filenames:
        debug('No static files to copy.')
    for filename in filenames:
        debug('Copying static file "{}" ...', filename)
        shutil.copy(
            os.path.join(PATH_STATIC, filename),
            os.path.join(destination_path, filename),
        )


def window(
    images: Iterable[Image],
) -> Iterator[Tuple[Optional[Image], Image, Optional[Image]]]:
    """Return a sliding window over the images.

    Returns a triple. Its first and third element can be `None`, but the
    second element never is.
    """
    n = 3
    padded_list: List[Optional[Image]] = list(images)
    padded_list.insert(0, None)
    padded_list.append(None)

    it = iter(padded_list)
    result = tuple(islice(it, n))

    if len(result) == n:
        yield result  # type: ignore

    for elem in it:
        result = result[1:] + (elem,)
        yield result  # type: ignore


@dataclass
class Image:
    gallery: Gallery
    full_filename: str
    path: str
    filename: str
    thumbnail_filename: str
    page_name: str
    previous_image: Optional[Image] = None
    next_image: Optional[Image] = None


def create_image(gallery: Gallery, full_filename: str) -> Image:
    path, filename = os.path.split(full_filename)
    basename, extension = os.path.splitext(filename)
    thumbnail_filename = f'{basename}_t{extension}'

    return Image(
        gallery=gallery,
        full_filename=full_filename,
        path=path,
        filename=filename,
        thumbnail_filename=thumbnail_filename,
        page_name=basename,
    )


def generate_image(image: Image, gallery: Gallery) -> None:
    """Create a (optionally resized) copy of an image."""
    destination_filename = os.path.join(
        gallery.destination_path, image.filename
    )
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
    destination_filename = os.path.join(
        gallery.destination_path, image.thumbnail_filename
    )
    resize_image(
        image.full_filename,
        destination_filename,
        gallery.max_thumbnail_size,
    )


def load_caption(image: Image) -> str:
    """Load image caption from file."""
    caption_filename = os.path.join(
        image.path, image.filename + IMAGE_CAPTION_EXTENSION
    )
    return _read_first_line(caption_filename)


def _read_first_line(filename: str) -> Optional[str]:
    """Read the first line from the specified file."""
    try:
        text = Path(filename).read_text(encoding='utf-8')
        first_line = text.splitlines()[0]
        return first_line.strip()
    except IOError:
        # File does not exist (OK) or cannot be read (not really OK).
        return None


def render_html_page(image: Image, destination_path: str) -> None:
    """Create an HTML document for a single image."""
    context = {'image': image}
    render_html_to_file('view', context, destination_path, image.page_name)


# -------------------------------------------------------------------- #


def handle_duplicate_filenames(paths) -> None:
    duplicates = find_duplicate_filenames(paths)
    if not duplicates:
        return

    print('Found duplicate filenames:')
    for filename, paths in duplicates:
        print(f'  + "{filename}" appears in the following paths:')
        for path in paths:
            print(f'    - {path}')

    sys.exit('Clashing target filenames, aborting.')


def find_duplicate_filenames(
    paths: Iterable[str],
) -> List[Tuple[str, List[str]]]:
    d = defaultdict(list)
    for path in paths:
        key = os.path.basename(path).lower()
        d[key].append(path)

    return [item for item in d.items() if len(item[1]) > 1]