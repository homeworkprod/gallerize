"""
:Copyright: 2007-2021 Jochen Kupperschmidt
:License: MIT, see LICENSE for details.
"""

import pytest

from gallerize.cli import parse_dimension_arg


@pytest.mark.parametrize(
    ('arg_value', 'expected_width', 'expected_height'),
    [
        ('480x640', 480, 640),
        ('1280x960', 1280, 960),
    ],
)
def test_parse_dimension_arg(arg_value, expected_width, expected_height):
    actual = parse_dimension_arg(arg_value)

    assert actual.width == expected_width
    assert actual.height == expected_height
