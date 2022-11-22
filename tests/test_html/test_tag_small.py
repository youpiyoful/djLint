"""Test html small tag.

pytest tests/test_html/test_tag_small.py
"""
import pytest

from src.djlint.formatter.indent import indent_html
from tests.conftest import printer

test_data = [
    pytest.param(
        "<small>text</small>",
        "<small>text</small>\n",
        id="small_tag",
    ),
]


@pytest.mark.parametrize("source,expected", test_data)
def test_base(source, expected, basic_config):
    output = indent_html(source, basic_config)

    printer(expected, output)
    assert expected == output
