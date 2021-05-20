"""
gallerize.logging
~~~~~~~~~~~~~~~~~

:Copyright: 2007-2021 Jochen Kupperschmidt
:License: MIT, see LICENSE for details.
"""


from typing import Any


def debug(message: str, *args: Any) -> None:
    print(message.format(*args))
