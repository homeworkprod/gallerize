# -*- coding: utf-8 -*-

"""
gallerize tests
~~~~~~~~~~~~~~~

See README for details.

:Copyright: 2007-2015 Jochen Kupperschmidt
:License: MIT, see LICENSE for details.
"""

import pytest

from gallerize import find_duplicate_filenames, parse_dimension_arg, window


parametrize = pytest.mark.parametrize


@parametrize(('iterable', 'n', 'expected'), [
    (
        [1, 2, 3, 4, 5, 6, 7],
        3,
        [(1, 2, 3), (2, 3, 4), (3, 4, 5), (4, 5, 6), (5, 6, 7)]
    ),
    (
        [1, 2, 3, 4, 5, 6],
        4,
        [(1, 2, 3, 4), (2, 3, 4, 5), (3, 4, 5, 6)]
    ),
])
def test_window(iterable, n, expected):
    actual = list(window(iterable, n))
    assert actual == expected


@parametrize(('paths', 'expected'), [
    (
        ['dir1/foo.txt', 'dir1/bar.txt', 'foo.txt', 'dir2/Foo.tXt'],
        {
            'foo.txt': ['dir1/foo.txt', 'foo.txt', 'dir2/Foo.tXt'],
        }
    ),
    (
        ['xy/one.jpg', 'xy/two.jpg', 'xy/three.jpg', 'one.jpg', 'three.jpg'],
        {
            'one.jpg': ['xy/one.jpg', 'one.jpg'],
            'three.jpg': ['xy/three.jpg', 'three.jpg'],
        }
    ),
])
def test_find_duplicate_filenames(paths, expected):
    actual = dict(find_duplicate_filenames(paths))
    assert actual == expected


@parametrize(('arg_value', 'expected_width', 'expected_height'), [
    ('480x640',   480, 640),
    ('1280x960', 1280, 960),
])
def test_parse_dimension_arg(arg_value, expected_width, expected_height):
    actual = parse_dimension_arg(arg_value)

    assert actual.width == expected_width
    assert actual.height == expected_height
