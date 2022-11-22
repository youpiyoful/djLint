"""Test html pre tag.

pytest tests/test_html/test_tag_pre.py
"""
import pytest

from src.djlint.formatter.indent import indent_html
from tests.conftest import printer

# added for https://github.com/Riverside-Healthcare/djLint/issues/187
test_data = [
    pytest.param(
        (
            "{% if a %}\n"
            "    <div>\n"
            "        <pre><code>asdf</code></pre>\n"
            "        <pre><code>asdf\n"
            "            </code></pre>\n"
            "        <!-- other html -->\n"
            "        <h2>title</h2>\n"
            "    </div>\n"
            "{% endif %}\n"
        ),
        (
            "{% if a %}\n"
            "    <div>\n"
            "        <pre><code>asdf</code></pre>\n"
            "        <pre><code>asdf\n"
            "            </code></pre>\n"
            "        <!-- other html -->\n"
            "        <h2>title</h2>\n"
            "    </div>\n"
            "{% endif %}\n"
        ),
        id="pre_tag",
    ),
]


@pytest.mark.parametrize("source,expected", test_data)
def test_base(source, expected, basic_config):
    output = indent_html(source, basic_config)

    printer(expected, output)
    assert expected == output
