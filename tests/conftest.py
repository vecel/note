import os
import json
import copy

import pytest
from typer.testing import CliRunner

from app.cli import app
from app.core import REPOSITORY_FILENAME, REPOSITORY_TEMPLATE
from app.core.models import Note

@pytest.fixture
def runner() -> CliRunner:
    """Provides a Typer CliRunner."""
    return CliRunner()

@pytest.fixture
def test_app():
    """Provides the Typer app instance."""
    return app

@pytest.fixture
def repo_path(tmp_path):
    os.chdir(tmp_path)
    return tmp_path / REPOSITORY_FILENAME

@pytest.fixture
def repo_initialized(repo_path):
    """
    Initializes empty repository in temporary file.
    
    Returns:
        Path: A path to repository.
    """
    with open(repo_path, "w") as file:
        json.dump(REPOSITORY_TEMPLATE, file)

    return repo_path

@pytest.fixture
def repo_with_notes(repo_path):
    """
    Initializes repository with sample notes in temporary file.
    
    Returns:
        Path: A path to repository.
    """
    notes = [
        Note.create("New note.", ["mytag"]),
        Note.create("Another note.", ["mytag", "awesome"], "COMPLETED")
    ]

    repo = copy.deepcopy(REPOSITORY_TEMPLATE)
    repo["notes"] = [note.to_dict() for note in notes]
    repo["config"]["statuses"]["COMPLETED"] = {
        "style": "green bold",
        "priority": -2
    }
    repo["config"]["statuses"]["PRIORITY"] = {
        "style": "red",
        "priority": 10
    }

    with open(repo_path, "w") as file:
        json.dump(repo, file)

    return repo_path

@pytest.fixture
def repo_with_untagged_notes(repo_path):
    """
    Initializes repository with sample, untagged notes in temporary file.
    
    Returns:
        Path: A path to repository.
    """
    notes = [
        Note.create("New note.", []),
        Note.create("Another note.", [])
    ]

    repo = copy.deepcopy(REPOSITORY_TEMPLATE)
    repo["notes"] = [note.to_dict() for note in notes]

    with open(repo_path, "w") as file:
        json.dump(repo, file)

    return repo_path
