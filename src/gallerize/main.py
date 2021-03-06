"""
gallerize.main
~~~~~~~~~~~~~~

:Copyright: 2007-2021 Jochen Kupperschmidt
:License: MIT, see LICENSE for details.
"""

from __future__ import annotations
import codecs
from collections import defaultdict
from dataclasses import dataclass
from itertools import islice
import os
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
    with codecs.open(filename, 'w', 'utf-8') as f:
        debug('Writing "{}" ...', filename)
        f.write(content)


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
        Image(gallery, image) for image in sorted(full_image_filenames)
    ]
    gallery.link_images()

    return gallery


class Gallery:
    def __init__(
        self,
        title: str,
        destination_path: str,
        resize: bool,
        max_image_size: Dimension,
        max_thumbnail_size: Dimension,
    ) -> None:
        self.images: List[Image] = []
        self.title = title
        self.destination_path = destination_path
        self.resize = resize
        self.max_image_size = max_image_size
        self.max_thumbnail_size = max_thumbnail_size

    def link_images(self) -> None:
        """Assign the predecessor and successor for every image."""
        for previous_image, image, next_image in window(self.images):
            image.previous_image = previous_image
            image.next_image = next_image

    def generate(self) -> None:
        # Create destination path if it doesn't exist.
        if not os.path.exists(self.destination_path):
            debug(
                'Destination path "{}" does not exist, creating it.',
                self.destination_path,
            )
            os.mkdir(self.destination_path)

        self.generate_images()
        for image in self.images:
            image.load_caption()
        self.render_html_pages()
        self.copy_additional_static_files()
        debug('Done.')

    def generate_images(self) -> None:
        for image in self.images:
            image.generate_image()
            image.generate_thumbnail()
            image.load_caption()

    def render_html_pages(self) -> None:
        for image in self.images:
            image.render_html_page()
        self.render_html_index_page()

    def render_html_index_page(self) -> None:
        """Create an HTML document of thumbnails that link to single image
        documents.
        """
        context = {
            'gallery': self,
        }
        render_html_to_file('index', context, self.destination_path, 'index')

    def copy_additional_static_files(self) -> None:
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
                os.path.join(self.destination_path, filename),
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


class Image:
    def __init__(self, gallery: Gallery, full_filename: str) -> None:
        self.gallery = gallery
        self.full_filename = full_filename
        self.path, self.filename = os.path.split(full_filename)
        self.basename, self.extension = os.path.splitext(self.filename)
        self.thumbnail_filename = f'{self.basename}_t{self.extension}'
        self.page_name = self.basename
        self.previous_image: Optional[Image] = None
        self.next_image: Optional[Image] = None

    def generate_image(self) -> None:
        """Create a (optionally resized) copy of an image."""
        destination_filename = os.path.join(
            self.gallery.destination_path, self.filename
        )
        if self.gallery.resize:
            # Resize image.
            debug('Resizing image "{}" ...', self.full_filename)
            resize_image(
                self.full_filename,
                destination_filename,
                self.gallery.max_image_size,
            )
        else:
            # Copy image.
            debug('Copying image "{}" ...', self.full_filename)
            shutil.copy(self.full_filename, destination_filename)

    def generate_thumbnail(self) -> None:
        """Create a preview of an image."""
        debug('Creating thumbnail "{}" ...', self.thumbnail_filename)
        destination_filename = os.path.join(
            self.gallery.destination_path, self.thumbnail_filename
        )
        resize_image(
            self.full_filename,
            destination_filename,
            self.gallery.max_thumbnail_size,
        )

    def load_caption(self) -> None:
        """Load image caption from file."""
        caption_filename = os.path.join(
            self.path, self.filename + IMAGE_CAPTION_EXTENSION
        )
        self.caption = self._read_first_line(caption_filename)

    def _read_first_line(self, filename: str) -> Optional[str]:
        """Read the first line from the specified file."""
        try:
            with codecs.open(filename, 'rb', 'utf-8') as f:
                return f.next().strip()
        except IOError:
            # File does not exist (OK) or cannot be read (not really OK).
            return None

    def render_html_page(self) -> None:
        """Create an HTML document for a single image."""
        context = {
            'image': self,
        }
        render_html_to_file(
            'view', context, self.gallery.destination_path, self.page_name
        )


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
