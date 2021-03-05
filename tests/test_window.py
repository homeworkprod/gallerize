"""
:Copyright: 2007-2021 Jochen Kupperschmidt
:License: MIT, see LICENSE for details.
"""

import pytest

from gallerize.main import window


@pytest.mark.parametrize(
    ('iterable', 'n', 'expected'),
    [
        (
            [1, 2, 3, 4, 5, 6, 7],
            3,
            [
                (1, 2, 3),
                (2, 3, 4),
                (3, 4, 5),
                (4, 5, 6),
                (5, 6, 7),
            ],
        ),
        (
            [1, 2, 3, 4, 5, 6],
            4,
            [
                (1, 2, 3, 4),
                (2, 3, 4, 5),
                (3, 4, 5, 6),
            ],
        ),
    ],
)
def test_window(iterable, n, expected):
    assert list(window(iterable, n)) == expected
