import os
import json

import pytest
from typer.testing import CliRunner

from app import __app_name__, __version__
from app.cli import app 

runner = CliRunner()

@pytest.fixture
def repo_initialized(tmp_path):
    os.chdir(tmp_path)
    runner.invoke(app, ["init"])

@pytest.fixture
def repo_with_notes(repo_initialized):
    runner.invoke(app, ["add", "New note.", "-t", "mytag"])
    runner.invoke(app, ["add", "Another note.", "-t", "mytag,awesome"])

@pytest.fixture
def repo_with_untagged_notes(repo_initialized):
    runner.invoke(app, ["add", "New note."])
    runner.invoke(app, ["add", "Another one."])

def test_list(repo_with_notes):
    result = runner.invoke(app, ["list"])

    assert result.exit_code == 0
    assert "New note." in result.stdout
    assert "Another note." in result.stdout
    assert "#mytag #awesome" in result.stdout

def test_list_empty_repository(repo_initialized):
    result = runner.invoke(app, ["list"])

    assert result.exit_code == 0
    assert "Repository is empty. Run `note add` to add a note." in result.stdout

def test_list_repository_not_initialized(tmp_path):
    os.chdir(tmp_path)
    result = runner.invoke(app, ["list"])

    assert result.exit_code == 0
    assert f"Notes repository does not exist. Run `note init` to initialize repository." in result.stdout

def test_list_tags(repo_with_notes):
    result = runner.invoke(app, ["list", "-T"])

    assert result.exit_code == 0
    assert "#mytag #awesome" in result.stdout

def test_list_no_tags(repo_with_untagged_notes):
    result = runner.invoke(app, ["list", "-T"])

    assert result.exit_code == 0
    assert "There are no tagged notes in the repository." in result.stdout

def test_list_tag_filter(repo_with_notes):
    result = runner.invoke(app, ["list", "-t", "awesome"])

    assert result.exit_code == 0
    assert "Another note." in result.stdout
    assert "New note." not in result.stdout

def test_list_tag_filter_no_matching_tag(repo_with_notes):
    result = runner.invoke(app, ["list", "-t", "nonexisting"])

    assert result.exit_code == 0
    assert "There are no notes matching given tag filter in repository." in result.stdout