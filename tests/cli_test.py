from typer.testing import CliRunner

from app import __app_name__, __version__
from app.cli import app

runner = CliRunner()

def test_version():
    result = runner.invoke(app, args="--version")
    assert result.exit_code == 0
    assert f"{__app_name__} v{__version__}" in result.stdout