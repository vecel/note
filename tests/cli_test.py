from app import __app_name__, __version__

def test_version(runner, test_app):
    result = runner.invoke(test_app, ["--version"])
    assert result.exit_code == 0
    assert f"{__app_name__} v{__version__}" in result.stdout