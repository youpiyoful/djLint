"""Djlint tests specific to aurelia.

Some tests may be from prettier.io's html test suite.

Where applicable this notice may be needed:

#### Prettier.io license ####
Copyright © James Long and contributors
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

run::

   poetry run pytest tests/test_html/test_aurelia.py --cov=src/djlint --cov-branch \
          --cov-report xml:coverage.xml --cov-report term-missing

   poetry run pytest tests/test_html/test_aurelia.py::test_aurelia

"""
# pylint: disable=C0116
import pytest

from src.djlint.formatter.indent import indent_html
from tests.conftest import printer

test_data = [
    pytest.param(
        ("<template>\n" '    <i class.bind="icon"></i>\n' "</template>\n"),
        ("<template>\n" '    <i class.bind="icon"></i>\n' "</template>\n"),
        id="aurelia",
    ),
]


@pytest.mark.parametrize("source,expected", test_data)
def test_base(source, expected, basic_config):
    output = indent_html(source, basic_config)

    printer(expected, output)
    assert expected == output
