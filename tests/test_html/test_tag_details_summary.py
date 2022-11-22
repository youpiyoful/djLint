"""Tests html details/summary tag.

pytest tests/test_html/test_tag_details_summary.py
"""
import pytest

from src.djlint.formatter.indent import indent_html
from tests.conftest import printer

test_data = [
    pytest.param(
        ("<details><summary>summary</summary>body</details>"),
        (
            "<details>\n"
            "    <summary>\n"
            "        summary\n"
            "    </summary>\n"
            "    body\n"
            "</details>\n"
        ),
        id="details_summary_tags",
    ),
]


@pytest.mark.parametrize("source,expected", test_data)
def test_base(source, expected, basic_config):
    output = indent_html(source, basic_config)

    printer(expected, output)
    assert expected == output
