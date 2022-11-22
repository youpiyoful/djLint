"""Test html picture tag.

pytest tests/test_html/test_tag_picture.py
"""
import pytest

from src.djlint.formatter.indent import indent_html
from tests.conftest import printer

test_data = [
    pytest.param(
        (
            '<picture><source media="(max-width:640px)"\n'
            'srcset="image.jpg"><img src="image.jpg" alt="image"></picture>\n'
        ),
        (
            "<picture>\n"
            '    <source media="(max-width:640px)" srcset="image.jpg">\n'
            '    <img src="image.jpg" alt="image">\n'
            "</picture>\n"
        ),
        id="picture_source_img_tags",
    ),
]


@pytest.mark.parametrize("source,expected", test_data)
def test_base(source, expected, basic_config):
    output = indent_html(source, basic_config)

    printer(expected, output)
    assert expected == output
