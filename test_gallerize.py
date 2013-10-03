# -*- coding: utf-8 -*-

"""
gallerize tests
~~~~~~~~~~~~~~~

See README for details.

:Copyright: 2007-2013 Jochen Kupperschmidt
:License: MIT, see LICENSE for details.
"""

import pytest

import gallerize


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
    actual = list(gallerize.window(iterable, n))
    assert actual == expected

@parametrize(('paths', 'expected'), [
    (
        ['dir1/foo.txt', 'dir1/bar.txt', 'foo.txt', 'dir2/Foo.tXt'],
        [
            ('foo.txt', ['dir1/foo.txt', 'foo.txt', 'dir2/Foo.tXt']),
        ]
    ),
    (
        ['xy/one.jpg', 'xy/two.jpg', 'xy/three.jpg', 'one.jpg', 'three.jpg'],
        [
            ('one.jpg', ['xy/one.jpg', 'one.jpg']),
            ('three.jpg', ['xy/three.jpg', 'three.jpg']),
        ]
    ),
])
def test_find_duplicate_filenames(paths, expected):
    actual = list(gallerize.find_duplicate_filenames(paths))
    assert actual == expected
