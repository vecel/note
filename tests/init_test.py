import os
import json

from app.core import REPOSITORY_FILENAME

def test_init(tmp_path, runner, test_app):
    os.chdir(tmp_path)
    notes_file = tmp_path / REPOSITORY_FILENAME
    result = runner.invoke(test_app, ["init"])

    assert result.exit_code == 0
    assert notes_file.exists()
    assert f"Initialized empty notes repository in {notes_file}" in result.stdout

def test_init_already_exists(repo_initialized, runner, test_app):
    result = runner.invoke(test_app, ["init"])

    assert result.exit_code == 0
    assert repo_initialized.exists()
    assert f"Notes repository already initialized in {repo_initialized}" in result.stdout


def test_init_repository_structure(tmp_path, runner, test_app):
    os.chdir(tmp_path)
    notes_file = tmp_path / REPOSITORY_FILENAME
    result = runner.invoke(test_app, ["init"])

    with open(notes_file, "r") as file:
        repository = json.load(file)

    assert result.exit_code == 0
    assert isinstance(repository, dict)
    assert "notes" in repository.keys()
    assert "config" in repository.keys()
    assert "statuses" in repository["config"].keys()