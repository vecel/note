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
    result = runner.invoke(app, ["add", "New note."])
    with open(initialized_repo, "r") as file:
        repository = json.load(file)

    assert result.exit_code == 0
    assert "notes" in repository.keys()
    
    note = repository["notes"][0]

    assert all(key in note.keys() for key in ("id", "content", "tags"))
    assert "New note." == note["content"]

def test_add_with_tags(initialized_repo):
    result = runner.invoke(app, ["add", "New note.", "-t", "awesome,cool"])
    with open(initialized_repo, "r") as file:
        repository = json.load(file)

    assert result.exit_code == 0
    
    note = repository["notes"][0]

    assert all(key in note.keys() for key in ("id", "content", "tags"))
    assert ["awesome", "cool"] == note["tags"] 

def test_add_repository_not_initialized(tmp_path):
    os.chdir(tmp_path)
    result = runner.invoke(app, ["add", "New note."])

    assert result.exit_code == 0
    assert f"Notes repository does not exist. Run `note init` to initialize repository." in result.stdout
    