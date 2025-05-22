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
    