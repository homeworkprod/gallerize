#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
gallerize
~~~~~~~~~

Create a static HTML/CSS image gallery from a bunch of images.

See README for details.

:Copyright: 2007-2015 Jochen Kupperschmidt
:License: MIT, see LICENSE for details.
"""

from __future__ import print_function
import argparse
import codecs
from collections import defaultdict, namedtuple
try:
    from future_builtins import filter, map  # Python 2.6+
except ImportError:
    pass  # Python 3+
from itertools import islice
import os
import shutil
import subprocess
import sys

from jinja2 import Environment, FileSystemLoader


ARGS_DEFAULT_MAX_IMAGE_SIZE = '1024x1024'
ARGS_DEFAULT_MAX_THUMBNAIL_SIZE = '120x120'

IMAGE_CAPTION_EXTENSION = '.txt'
TEMPLATE_EXTENSION = '.html'
OUTPUT_HTML_EXTENSION = '.html'

PATH = os.path.dirname(os.path.abspath(__file__))
PATH_STATIC = os.path.join(PATH, 'static')
TEMPLATE_ENVIRONMENT = Environment(
    autoescape=True,
    loader=FileSystemLoader(os.path.join(PATH, 'templates')),
    trim_blocks=False)


def debug(message, *args):
    print(message.format(*args))

def resize_image(src_filename, dst_filename, max_dimension):
    """Create a resized (and antialiased) version of an image."""
    dimension_str = '{0.width:d}x{0.height:d}'.format(max_dimension)
    cmd = ['convert', '-resize', dimension_str, src_filename, dst_filename]
    subprocess.check_call(cmd)

def render_html_to_file(template_name, context, path, page_name):
    """Render the template and write the result to the given file."""
    context['url_for_page'] = lambda page: page + OUTPUT_HTML_EXTENSION
    html = render_template(template_name + TEMPLATE_EXTENSION, **context)

    filename = os.path.join(path, page_name + OUTPUT_HTML_EXTENSION)
    write_file(filename, html)

def render_template(template_filename, **context):
    return TEMPLATE_ENVIRONMENT \
        .get_template(template_filename) \
        .render(context)

def write_file(filename, content):
    with codecs.open(filename, 'wb', 'utf-8') as f:
        debug('Writing "{}" ...', filename)
        f.write(content)


class Gallery(object):

    @classmethod
    def from_args(cls, args):
        gallery = Gallery()

        gallery.images = [Image(gallery, image)
                          for image in sorted(args.full_image_filenames)]
        gallery.link_images()
        gallery.title = args.title
        gallery.destination_path = args.destination_path
        gallery.resize = not args.no_resize
        gallery.max_image_size = args.max_image_size
        gallery.max_thumbnail_size = args.max_thumbnail_size

        return gallery

    def link_images(self):
        """Assign the predecessor and successor for every image."""
        for previous_image, image, next_image \
                in window([None] + self.images + [None], 3):
            image.previous_image = previous_image
            image.next_image = next_image

    def generate(self):
        # Create destination path if it doesn't exist.
        if not os.path.exists(self.destination_path):
            debug('Destination path "{}" does not exist, creating it.',
                  self.destination_path)
            os.mkdir(self.destination_path)

        self.generate_images()
        for image in self.images:
            image.load_caption()
        self.generate_stylesheet()
        self.render_html_pages()
        self.copy_additional_static_files()
        debug('Done.')

    def generate_images(self):
        for image in self.images:
            image.generate_image()
            image.generate_thumbnail()
            image.load_caption()

    def generate_stylesheet(self):
        filename = os.path.join(self.destination_path, 'style.css')
        css = render_template('style.css')
        write_file(filename, css)

    def render_html_pages(self):
        for image in self.images:
            image.render_html_page()
        self.render_html_index_page()

    def render_html_index_page(self):
        """Create an HTML document of thumbnails that link to single image
        documents.
        """
        context = {
            'gallery': self,
        }
        render_html_to_file('index', context, self.destination_path, 'index')

    def copy_additional_static_files(self):
        if not os.path.exists(PATH_STATIC):
            debug('Path "{}", does not exist; not copying any static files.',
                  PATH_STATIC)
            return

        filenames = list(sorted(os.listdir(PATH_STATIC)))
        if not filenames:
            debug('No static files to copy.')
        for filename in filenames:
            debug('Copying static file "{}" ...', filename)
            shutil.copy(
                os.path.join(PATH_STATIC, filename),
                os.path.join(self.destination_path, filename))


def window(iterable, n):
    """Return a sliding window of width ``n`` over the iterable."""
    it = iter(iterable)
    result = tuple(islice(it, n))
    if len(result) == n:
        yield result
    for elem in it:
        result = result[1:] + (elem,)
        yield result


class Image(object):

    previous_image = None
    next_image = None

    def __init__(self, gallery, full_filename):
        self.gallery = gallery
        self.full_filename = full_filename
        self.path, self.filename = os.path.split(full_filename)
        self.basename, self.extension = os.path.splitext(self.filename)
        self.thumbnail_filename = 'thumbnail_{}{}' \
            .format(self.basename, self.extension)
        self.page_name = self.basename

    def generate_image(self):
        """Create a (optionally resized) copy of an image."""
        destination_filename = os.path.join(self.gallery.destination_path,
                                            self.filename)
        if self.gallery.resize:
            # Resize image.
            debug('Resizing image "{}" ...', self.full_filename)
            resize_image(
                self.full_filename,
                destination_filename,
                self.gallery.max_image_size)
        else:
            # Copy image.
            debug('Copying image "{}" ...', self.full_filename)
            shutil.copy(self.full_filename, destination_filename)

    def generate_thumbnail(self):
        """Create a preview of an image."""
        debug('Creating thumbnail "{}" ...', self.thumbnail_filename)
        destination_filename = os.path.join(self.gallery.destination_path,
                                            self.thumbnail_filename)
        resize_image(
            self.full_filename,
            destination_filename,
            self.gallery.max_thumbnail_size)

    def load_caption(self):
        """Load image caption from file."""
        caption_filename = os.path.join(
            self.path,
            self.filename + IMAGE_CAPTION_EXTENSION)
        self.caption = self._read_first_line(caption_filename)

    def _read_first_line(self, filename):
        """Read the first line from the specified file."""
        try:
            with codecs.open(filename, 'rb', 'utf-8') as f:
                return f.next().strip()
        except IOError:
            # File does not exist (OK) or cannot be read (not really OK).
            pass

    def render_html_page(self):
        """Create an HTML document for a single image."""
        context = {
            'image': self,
        }
        render_html_to_file('view', context, self.gallery.destination_path,
                            self.page_name)


# -------------------------------------------------------------------- #
# command line argument parsing


Dimension = namedtuple('Dimension', ['width', 'height'])

def parse_dimension_arg(value):
    """Validate a dimension value."""
    try:
        return Dimension(*map(int, value.split('x', 1)))
    except ValueError:
        raise argparse.ArgumentTypeError(
            'invalid dimension value: {!r}'.format(value))

def parse_args():
    """Parse command-line arguments."""

    parser = argparse.ArgumentParser(
        usage='%(prog)s [options] <target path> <image> [image] ...')

    parser.add_argument(
        '-c', '--captions',
        dest='captions',
        action='store_true',
        default=False,
        help='read image captions from text files ("<IMAGE_NAME>.txt")')

    parser.add_argument(
        '--no-resize',
        dest='no_resize',
        action='store_true',
        default=False,
        help='do not resize images, just copy them')

    parser.add_argument(
        '-s', '--size',
        dest='max_image_size',
        type=parse_dimension_arg,
        default=ARGS_DEFAULT_MAX_IMAGE_SIZE,
        help='set maximum image size [default: {}]'
             .format(ARGS_DEFAULT_MAX_IMAGE_SIZE))

    parser.add_argument(
        '-t', '--thumbnail-size',
        dest='max_thumbnail_size',
        type=parse_dimension_arg,
        default=ARGS_DEFAULT_MAX_THUMBNAIL_SIZE,
        help='set maximum thumbnail size [default: {}]'
             .format(ARGS_DEFAULT_MAX_THUMBNAIL_SIZE))

    parser.add_argument(
        '--title',
        dest='title',
        help='set gallery title on the website')

    # First positional argument.
    parser.add_argument('destination_path')

    # Remaining positional arguments (at least one), as a list.
    parser.add_argument('full_image_filenames', nargs='+')

    return parser.parse_args()


# -------------------------------------------------------------------- #


def handle_duplicate_filenames(paths):
    duplicates = list(find_duplicate_filenames(paths))
    if duplicates:
        print('Found duplicate filenames:')
        for filename, paths in duplicates:
            print('  + "{}" appears in the following paths:'.format(filename))
            for path in paths:
                print('    - ' + path)
        sys.exit('Clashing target filenames, aborting.')

def find_duplicate_filenames(paths):
    d = defaultdict(list)
    for path in paths:
        key = os.path.basename(path).lower()
        d[key].append(path)

    return filter(lambda x: len(x[1]) > 1, d.items())


# -------------------------------------------------------------------- #


if __name__ == '__main__':
    try:
        args = parse_args()
        handle_duplicate_filenames(args.full_image_filenames)
        Gallery.from_args(args).generate()
    except KeyboardInterrupt:
        sys.exit('Ctrl-C pressed, aborting.')
