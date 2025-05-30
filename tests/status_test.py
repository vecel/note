import os
import json

def test_status_add(repo_initialized, runner, test_app):
    result = runner.invoke(test_app, ["status", "-a", "NEW_STATUS", "-s", "yellow", "-p", "3"])

    with open(repo_initialized, "r") as file:
        repository = json.load(file)

    statuses = repository["config"]["statuses"]

    assert result.exit_code == 0
    assert "NEW_STATUS" in statuses.keys()
    assert all(key in statuses["NEW_STATUS"].keys() for key in ("style", "priority"))
    assert statuses["NEW_STATUS"]["style"] == "yellow"
    assert statuses["NEW_STATUS"]["priority"] == 3

def test_status_repository_not_initialized(tmp_path, runner, test_app):
    os.chdir(tmp_path)
    result = runner.invoke(test_app, ["status", "-a", "NEW_STATUS"])

    assert result.exit_code == 0
    assert "Notes repository does not exist. Run `note init` to initialize repository." in result.stdout

def test_status_exactly_one_option_valid(repo_initialized, runner, test_app):
    result = runner.invoke(test_app, ["status", "-a", "NEW_STATUS", "-d", "OLD_STATUS"])

    assert result.exit_code == 0
    assert "You must use exactly one of --add, --edit or --delete." in result.stdout