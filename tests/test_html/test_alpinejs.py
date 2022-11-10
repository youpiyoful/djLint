"""DjLint tests for alpine.js.

run:

   pytest tests/test_html/test_alpinejs.py --cov=src/djlint --cov-branch \
          --cov-report xml:coverage.xml --cov-report term-missing

   pytest tests/test_html/test_alpinejs.py::test_alpine_js

"""
# pylint: disable=C0116

from src.djlint.formatter.indent import indent_html
from tests.conftest import printer

def test_alpine_js(basic_config) -> None:
    source = (
        '<div id="collapse"\n'
        '     x-data="{ show: true }"\n'
        '     x-show="show"\n'
        '     x-transition.duration.500ms\n'
        '     :disabled="!$store.userPreferences.deleteConfirm"\n'
        '     @click="clicked=true">'
        '</div>\n'
    )
    output =indent_html(source, basic_config)
    printer(source,output)

    assert source == output


def test_alpine_nested_html(basic_config) -> None:
    source = (
        '<html lang="en">\n'
        '    <body>\n'
        '        <!-- x-data , x-text , x-html -->\n'
        '        <div x-data="{key:\'value\',message:\'hello <b>world</b> \'}">\n'
        '            <p x-text="key"></p>\n'
        '            <p x-html="message"></p>\n'
        '        </div>\n'
        '    </body>\n'
        '</html>\n'
    )

    output =indent_html(source, basic_config)
    printer(source,output)

    assert source == output

