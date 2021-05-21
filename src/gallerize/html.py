"""
gallerize.html
~~~~~~~~~~~~~~

HTML rendering

:Copyright: 2007-2021 Jochen Kupperschmidt
:License: MIT, see LICENSE for details.
"""

from __future__ import annotations
from pathlib import Path
from typing import Any

from jinja2 import Environment, PackageLoader

from .files import write_file
from .models import Gallery, Image


TEMPLATE_EXTENSION: str = '.html'
OUTPUT_HTML_EXTENSION: str = '.html'

TEMPLATE_ENVIRONMENT: Environment = Environment(
    autoescape=True,
    loader=PackageLoader(__package__, 'templates'),
    trim_blocks=False,
)


def render_html_pages(gallery: Gallery) -> None:
    for image in gallery.images:
        _render_html_page(gallery, image)
    _render_html_index_page(gallery)


def _render_html_page(gallery: Gallery, image: Image) -> None:
    """Create an HTML document for a single image."""
    context = {'gallery': gallery, 'image': image}
    _render_html_to_file(
        'view', context, gallery.destination_path, image.page_name
    )


def _render_html_index_page(gallery: Gallery) -> None:
    """Create an HTML document of thumbnails that link to single image
    documents.
    """
    context = {'gallery': gallery}
    _render_html_to_file('index', context, gallery.destination_path, 'index')


def _render_html_to_file(
    template_name: str, context: dict[str, Any], path: Path, page_name: str
) -> None:
    """Render the template and write the result to the given file."""
    context['url_for_page'] = lambda page: page + OUTPUT_HTML_EXTENSION
    html = _render_template(template_name + TEMPLATE_EXTENSION, **context)

    filename = path / (page_name + OUTPUT_HTML_EXTENSION)
    write_file(filename, html)


def _render_template(template_filename: str, **context: dict[str, Any]) -> str:
    return TEMPLATE_ENVIRONMENT.get_template(template_filename).render(context)
