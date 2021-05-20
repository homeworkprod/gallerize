"""
:Copyright: 2007-2021 Jochen Kupperschmidt
:License: MIT, see LICENSE for details.
"""

from pathlib import Path

import pytest

from gallerize.main import find_duplicate_filenames


@pytest.mark.parametrize(
    ('paths', 'expected'),
    [
        (
            [
                Path('dir1/foo.txt'),
                Path('dir1/bar.txt'),
                Path('foo.txt'),
                Path('dir2/Foo.tXt'),
            ],
            {
                'foo.txt': [
                    Path('dir1/foo.txt'),
                    Path('foo.txt'),
                    Path('dir2/Foo.tXt'),
                ],
            },
        ),
        (
            [
                Path('xy/one.jpg'),
                Path('xy/two.jpg'),
                Path('xy/three.jpg'),
                Path('one.jpg'),
                Path('three.jpg'),
            ],
            {
                'one.jpg': [Path('xy/one.jpg'), Path('one.jpg')],
                'three.jpg': [Path('xy/three.jpg'), Path('three.jpg')],
            },
        ),
    ],
)
def test_find_duplicate_filenames(paths, expected):
    assert dict(find_duplicate_filenames(paths)) == expected
