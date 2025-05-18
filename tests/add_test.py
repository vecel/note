import os
import json

import pytest
from typer.testing import CliRunner

from app import __app_name__, __version__
from app.cli import app
from app.core import REPOSITORY_FILENAME

runner = CliRunner()

@pytest.fixture
def initialized_repo(tmp_path):
    os.chdir(tmp_path)
    notes_file = tmp_path / REPOSITORY_FILENAME
    runner.invoke(app, ["init"])
    return notes_file

def test_add(initialized_repo):
    note = {
        "content": "New note",
        "tags": None
    }
    result = runner.invoke(app, ["add", note["content"]])
    with open(initialized_repo, "r") as file:
        repository = json.load(file)

    assert result.exit_code == 0
    assert "notes" in repository.keys()
    assert note in repository["notes"]

def test_add_with_tags(initialized_repo):
    note = {
        "content": "New note.",
        "tags": ["awesome", "cool"]
    }
    result = runner.invoke(app, ["add", "New note.", "-t", "awesome,cool"])
    with open(initialized_repo, "r") as file:
        repository = json.load(file)

    assert result.exit_code == 0
    assert note in repository["notes"]

def test_add_repository_not_initialized(tmp_path):
    os.chdir(tmp_path)
    result = runner.invoke(app, ["add", "New note."])

    assert result.exit_code == 0
    assert f"Notes repository does not exist. Run `note init` to initialize repository." in result.stdout
    