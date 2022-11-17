"""DjLint tests for alpine.js.

run:

   pytest tests/test_html/test_alpinejs.py --cov=src/djlint --cov-branch \
          --cov-report xml:coverage.xml --cov-report term-missing

   pytest tests/test_html/test_alpinejs.py::test_alpine_js

"""
# pylint: disable=C0116

import pytest

from src.djlint.formatter.indent import indent_html
from tests.conftest import printer

alpine_js_source = (
    "<div\n"
    '    id="collapse"\n'
    '    x-data="{ show: true }"\n'
    '    x-show="show"\n'
    "    x-transition.duration.500ms\n"
    '    :disabled="!$store.userPreferences.deleteConfirm"\n'
    '    @click="clicked=true"\n'
    "></div>\n"
)

nested_html_source = (
    '<html lang="en">\n'
    "    <body>\n"
    "        <!-- x-data , x-text , x-html -->\n"
    "        <div x-data=\"{key:' value', message:'hello <b>world</b> '}\">\n"
    '            <p x-text="key"></p>\n'
    '            <p x-html="message"></p>\n'
    "        </div>\n"
    "    </body>\n"
    "</html>\n"
)

test_data = [
    pytest.param(alpine_js_source, alpine_js_source, id="alpine_js"),
    pytest.param(nested_html_source, nested_html_source, id="alpine_nested_html"),
]


@pytest.mark.parametrize("source,expected", test_data)
def test_base(source, expected, basic_config):
    output = indent_html(source, basic_config)

    printer(expected, output)
    assert expected == output
