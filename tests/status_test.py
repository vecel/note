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

def test_status_edit(repo_with_notes, runner, test_app):
    result = runner.invoke(test_app, ["status", "-e", "COMPLETED", "-s", "yellow", "-p", "-1"])

    with open(repo_with_notes, "r") as file:
        repository = json.load(file)

    statuses = repository["config"]["statuses"]

    assert result.exit_code == 0
    assert "COMPLETED" in statuses.keys()
    assert all(key in statuses["COMPLETED"].keys() for key in ("style", "priority"))
    assert statuses["COMPLETED"]["style"] == "yellow"
    assert statuses["COMPLETED"]["priority"] == -1

def test_status_notes_sorted_after_edit(repo_with_notes, runner, test_app):
    result = runner.invoke(test_app, ["status", "-e", "COMPLETED", "-s", "yellow", "-p", "1"])

    with open(repo_with_notes, "r") as file:
        repository = json.load(file)

    notes = repository["notes"]

    assert result.exit_code == 0
    assert notes[0]["content"] == "Another note."
    assert notes[1]["content"] == "New note."

def test_status_previous_properties_kept_if_not_edited(repo_with_notes, runner, test_app):
    result = runner.invoke(test_app, ["status", "-e", "COMPLETED", "-s", "yellow"])

    with open(repo_with_notes, "r") as file:
        repository = json.load(file)

    completed_status = repository["config"]["statuses"]["COMPLETED"]

    assert result.exit_code == 0
    assert completed_status["style"] == "yellow"
    assert completed_status["priority"] == -2

def test_status_edit_non_existing_status(repo_with_notes, runner, test_app):
    result = runner.invoke(test_app, ["status", "-e", "NON_EXISTING", "-s", "yellow"])

    assert result.exit_code == 0
    assert "There is no status NON_EXISTING in the repository configuration. Run `note list -S` to see all statuses or `note status --add STATUS` to add a new one." in result.stdout

def test_status_repository_not_initialized(tmp_path, runner, test_app):
    os.chdir(tmp_path)
    result = runner.invoke(test_app, ["status", "-a", "NEW_STATUS"])

    assert result.exit_code == 0
    assert "Notes repository does not exist. Run `note init` to initialize repository." in result.stdout

def test_status_exactly_one_option_valid(repo_initialized, runner, test_app):
    result = runner.invoke(test_app, ["status", "-a", "NEW_STATUS", "-d", "OLD_STATUS"])

    assert result.exit_code == 0
    assert "You must use exactly one of --add, --edit or --delete." in result.stdout