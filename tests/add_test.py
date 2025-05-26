import os
import json

def test_add(repo_initialized, runner, test_app):
    result = runner.invoke(test_app, ["add", "New note."])
    with open(repo_initialized, "r") as file:
        repository = json.load(file)

    assert result.exit_code == 0
    assert "notes" in repository.keys()
    
    note = repository["notes"][0]

    assert all(key in note.keys() for key in ("content", "tags", "status"))
    assert "New note." == note["content"]

def test_add_with_tags(repo_initialized, runner, test_app):
    result = runner.invoke(test_app, ["add", "New note.", "-t", "awesome,cool"])
    with open(repo_initialized, "r") as file:
        repository = json.load(file)

    assert result.exit_code == 0
    
    note = repository["notes"][0]

    assert all(key in note.keys() for key in ("content", "tags", "status"))
    assert ["awesome", "cool"] == note["tags"] 

def test_add_repository_not_initialized(tmp_path, runner, test_app):
    os.chdir(tmp_path)
    result = runner.invoke(test_app, ["add", "New note."])

    assert result.exit_code == 0
    assert f"Notes repository does not exist. Run `note init` to initialize repository." in result.stdout
    
def test_add_with_status(repo_with_notes, runner, test_app):
    result = runner.invoke(test_app, ["add", "Note content", "-s", "COMPLETED"])

    assert result.exit_code == 0

def test_add_with_non_existing_status(repo_with_notes, runner, test_app):
    result = runner.invoke(test_app, ["add", "Note content", "-s", "NONEXISTING"])

    assert result.exit_code == 0
    assert "There is no status NONEXISTING in the repository configuration. Run `note list -S` to see all statuses or `note status --add STATUS` to add a new one."