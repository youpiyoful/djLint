"""Test ignored content.

poetry run pytest tests/test_html/test_ignored.py
"""
import pytest

from src.djlint.formatter.indent import indent_html
from tests.conftest import printer

test_data = [
    pytest.param(
        ("<!-- <span> -->\n" "<div><p><span></span></p></div>\n" "<!-- <div> -->\n"),
        (
            "<!-- <span> -->\n"
            "<div>\n"
            "    <p>\n"
            "        <span></span>\n"
            "    </p>\n"
            "</div>\n"
            "<!-- <div> -->\n"
        ),
        id="ignored_1",
    ),
    # check custom ignore tag {# djlint:off #} {# djlint:on #}
    pytest.param(
        (
            "<!-- djlint:off -->\n"
            "<div><p><span></span></p></div>\n"
            "<!-- djlint:on -->\n"
            "{# djlint:off #}\n"
            "<div><p><span></span></p></div>\n"
            "{# djlint:on #}\n"
            "{% comment %} djlint:off {% endcomment %}\n"
            "<div><p><span></span></p></div>\n"
            "{% comment %} djlint:on {% endcomment %}\n"
            "{{ /* djlint:off */ }}\n"
            "<div><p><span></span></p></div>\n"
            "{{ /* djlint:on */ }}\n"
            "{{!-- djlint:off --}}\n"
            "<div><p><span></span></p></div>\n"
            "{{!-- djlint:on --}}\n"
        ),
        (
            "<!-- djlint:off -->\n"
            "<div><p><span></span></p></div>\n"
            "<!-- djlint:on -->\n"
            "{# djlint:off #}\n"
            "<div><p><span></span></p></div>\n"
            "{# djlint:on #}\n"
            "{% comment %} djlint:off {% endcomment %}\n"
            "<div><p><span></span></p></div>\n"
            "{% comment %} djlint:on {% endcomment %}\n"
            "{{ /* djlint:off */ }}\n"
            "<div><p><span></span></p></div>\n"
            "{{ /* djlint:on */ }}\n"
            "{{!-- djlint:off --}}\n"
            "<div><p><span></span></p></div>\n"
            "{{!-- djlint:on --}}\n"
        ),
        id="ignored_2",
    ),
    pytest.param(
        (
            '{# djlint: off #}<meta name="description" content="{% block meta_content %}Alle vogelkijkhutten van Nederland{% endblock %}">{# djlint:on #}'
        ),
        (
            '{# djlint: off #}<meta name="description" content="{% block meta_content %}Alle vogelkijkhutten van Nederland{% endblock %}">{# djlint:on #}'
        ),
        id="ignored_3",
    ),
    pytest.param(
        ("<script>\n" "    <div><p><span></span></p></div>\n" "</script>\n"),
        ("<script>\n" "    <div><p><span></span></p></div>\n" "</script>\n"),
        id="script",
    ),
    pytest.param(
        (
            "<html>\n"
            "    <head>\n"
            '        <link href="{% static  \'foo/bar.css\' %}" rel="stylesheet"/>\n'
            "        <!--JS-->\n"
            "        <script src=\"{% static  'foo/bar.js' %}\"></script>\n"
            "    </head>\n"
            "</html>\n"
        ),
        (
            "<html>\n"
            "    <head>\n"
            '        <link href="{% static  \'foo/bar.css\' %}" rel="stylesheet"/>\n'
            "        <!--JS-->\n"
            "        <script src=\"{% static  'foo/bar.js' %}\"></script>\n"
            "    </head>\n"
            "</html>\n"
        ),
        id="inline_scripts_links",
    ),
    pytest.param(
        (
            "<style>\n"
            "    {# override to fix text all over the place in media upload box #}\n"
            "    .k-dropzone .k-upload-status {\n"
            "        color: #a1a1a1;\n"
            "    }\n"
            "</style>\n"
        ),
        (
            "<style>\n"
            "    {# override to fix text all over the place in media upload box #}\n"
            "    .k-dropzone .k-upload-status {\n"
            "        color: #a1a1a1;\n"
            "    }\n"
            "</style>\n"
        ),
        id="style_tag_1",
    ),
    pytest.param(
        (
            "<style>\n"
            " .k-dropzone .k-upload-status {\n"
            "       color: #a1a1a1;\n"
            "           }\n"
            "</style>\n"
        ),
        (
            "<style>\n"
            " .k-dropzone .k-upload-status {\n"
            "       color: #a1a1a1;\n"
            "           }\n"
            "</style>\n"
        ),
        id="style_tag_2",
    ),
]


@pytest.mark.parametrize("source,expected", test_data)
def test_base(source, expected, basic_config):
    output = indent_html(source, basic_config)

    printer(expected, output)
    assert expected == output
