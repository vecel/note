import os

from typer.testing import CliRunner

from app import __app_name__, __version__
from app.cli import app 
from app.core import REPOSITORY_FILENAME

runner = CliRunner()

def test_init(tmp_path):
    os.chdir(tmp_path)
    notes_file = tmp_path / REPOSITORY_FILENAME
    
    result = runner.invoke(app, ["init"])

    assert result.exit_code == 0
    assert notes_file.exists()
    assert f"Initialized empty notes repository in {notes_file}" in result.stdout

def test_init_already_exists(tmp_path):
    os.chdir(tmp_path)
    notes_file = tmp_path / REPOSITORY_FILENAME
    runner.invoke(app, ["init"])
    
    result = runner.invoke(app, ["init"])

    assert result.exit_code == 0
    assert notes_file.exists()
    assert f"Notes repository already initialized in {notes_file}" in result.stdout