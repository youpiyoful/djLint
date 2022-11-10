"""Djlint test config."""
# pylint: disable=W0621,C0116
import os
import tempfile
from pathlib import Path
from types import SimpleNamespace
from typing import Generator, TextIO

import pytest
from click.testing import CliRunner

from src.djlint import main as djlint

from src.djlint.settings import Config
@pytest.fixture()
def runner() -> CliRunner:
    """Click runner for djlint tests."""
    return CliRunner()


@pytest.fixture()
def tmp_file() -> Generator:
    """Create a temp file for formatting."""
    # pylint: disable=R1732
    tmp = tempfile.NamedTemporaryFile(delete=False)
    yield tmp
    tmp.close()
    os.unlink(tmp.name)

def printer(expected,actual):
    print()
    print("Expected", ("."*10))
    print(expected)
    print()
    print("Result", ("."*10))
    print(actual)
    print()

def write_to_file(the_file: str, the_text: bytes) -> None:
    """Shortcode for write some bytes to a file."""
    with open(the_file, mode="w+b") as open_file:
        open_file.write(the_text)


def reformat(the_file: TextIO, runner: CliRunner, the_text: bytes) -> SimpleNamespace:
    write_to_file(the_file.name, the_text)
    result = runner.invoke(djlint, [the_file.name, "--reformat"])
    return SimpleNamespace(
        **{
            "text": Path(the_file.name).read_text(encoding="utf8"),
            "exit_code": result.exit_code,
        }
    )

@pytest.fixture(scope="function")
def basic_config() -> Config:
    """
    Return a config object with default basic options.
    """
    return Config("dummy/source.html")
