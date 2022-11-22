"""Test yaml front matter.

pytest tests/test_html/test_yaml.py
"""
import pytest

from src.djlint.formatter.indent import indent_html
from tests.conftest import printer

test_data = [
    pytest.param(
        (
            "---\n"
            "    invalid:\n"
            "invalid:\n"
            "---\n"
            "\n"
            "\n"
            "\n"
            "<html><head></head><body></body></html>\n"
        ),
        (
            "---\n"
            "    invalid:\n"
            "invalid:\n"
            "---\n"
            "<html>\n"
            "    <head></head>\n"
            "    <body></body>\n"
            "</html>\n"
        ),
        id="invalid",
    ),
    pytest.param(
        (
            "---\n"
            "hello:     world\n"
            "---\n"
            "<html><head></head><body></body></html>\n"
        ),
        (
            "---\n"
            "hello:     world\n"
            "---\n"
            "<html>\n"
            "    <head></head>\n"
            "    <body></body>\n"
            "</html>\n"
        ),
        id="valid",
    ),
    pytest.param(
        ("---\n" "layout: <div><div></div></div>\n" "---\n" "<div></div>\n"),
        ("---\n" "layout: <div><div></div></div>\n" "---\n" "<div></div>\n"),
        id="more",
    ),
    pytest.param(
        (
            "---mycustomparser\n"
            "title: Hello\n"
            "slug: home\n"
            "---\n"
            "<h1>\n"
            "  Hello world!</h1>\n"
        ),
        (
            "---mycustomparser\n"
            "title: Hello\n"
            "slug: home\n"
            "---\n"
            "<h1>Hello world!</h1>\n"
        ),
        id="custom_parser",
    ),
    pytest.param(
        ("---\n" "---\n" "<h1>\n" "  Hello world!</h1>\n"),
        ("---\n" "---\n" "<h1>Hello world!</h1>\n"),
        id="empty",
    ),
    pytest.param(
        ("---\n" "---\n" "<div>\n" "---\n" "</div>\n"),
        ("---\n" "---\n" "<div>---</div>\n"),
        id="empty_2",
    ),
    pytest.param(
        (
            "---\n"
            "layout: foo\n"
            "---\n"
            "Test <a\n"
            'href="https://djlint.com">abc</a>.\n'
        ),
        (
            "---\n"
            "layout: foo\n"
            "---\n"
            'Test <a href="https://djlint.com">abc</a>.\n'
        ),
        id="issue_9042_no_empty_line",
    ),
    pytest.param(
        (
            "---\n"
            "layout: foo\n"
            "---\n"
            "Test <a\n"
            'href="https://djlint.com">abc</a>.\n'
        ),
        (
            "---\n"
            "layout: foo\n"
            "---\n"
            'Test <a href="https://djlint.com">abc</a>.\n'
        ),
        id="issue_9042",
    ),
]


@pytest.mark.parametrize("source,expected", test_data)
def test_base(source, expected, basic_config):
    output = indent_html(source, basic_config)

    printer(expected, output)
    assert expected == output
