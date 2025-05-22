import os

import pytest
from typer.testing import CliRunner

from app.cli import app

@pytest.fixture
def runner() -> CliRunner:
    return CliRunner()

@pytest.fixture
def test_app():
    return app

@pytest.fixture
def repo_initialized(tmp_path, runner, test_app):
    os.chdir(tmp_path)
    runner.invoke(test_app, ["init"])

@pytest.fixture
def repo_with_notes(repo_initialized, runner, test_app):
    runner.invoke(test_app, ["add", "New note.", "-t", "mytag"])
    runner.invoke(test_app, ["add", "Another note.", "-t", "mytag,awesome"])

@pytest.fixture
def repo_with_untagged_notes(repo_initialized, runner, test_app):
    runner.invoke(test_app, ["add", "New note."])
    runner.invoke(test_app, ["add", "Another one."])
