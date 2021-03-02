"""
:Copyright: 2007-2021 Jochen Kupperschmidt
:License: MIT, see LICENSE for details.
"""

import pytest

from gallerize import find_duplicate_filenames


@pytest.mark.parametrize(
    ('paths', 'expected'),
    [
        (
            ['dir1/foo.txt', 'dir1/bar.txt', 'foo.txt', 'dir2/Foo.tXt'],
            {
                'foo.txt': ['dir1/foo.txt', 'foo.txt', 'dir2/Foo.tXt'],
            },
        ),
        (
            [
                'xy/one.jpg',
                'xy/two.jpg',
                'xy/three.jpg',
                'one.jpg',
                'three.jpg',
            ],
            {
                'one.jpg': ['xy/one.jpg', 'one.jpg'],
                'three.jpg': ['xy/three.jpg', 'three.jpg'],
            },
        ),
    ],
)
def test_find_duplicate_filenames(paths, expected):
    assert dict(find_duplicate_filenames(paths)) == expected
