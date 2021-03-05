"""
:Copyright: 2007-2021 Jochen Kupperschmidt
:License: MIT, see LICENSE for details.
"""

import pytest

from gallerize.main import window


@pytest.mark.parametrize(
    ('iterable', 'expected'),
    [
        (
            [1, 2, 3, 4, 5, 6, 7],
            [
                (1, 2, 3),
                (2, 3, 4),
                (3, 4, 5),
                (4, 5, 6),
                (5, 6, 7),
            ],
        ),
        (
            [None, 1, 2, 3, None],
            [
                (None, 1, 2),
                (1, 2, 3),
                (2, 3, None),
            ],
        ),
    ],
)
def test_window(iterable, expected):
    assert list(window(iterable)) == expected
