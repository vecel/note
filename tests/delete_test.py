import json

def test_delete(repo_with_notes, runner, test_app):
    result = runner.invoke(test_app, ["delete", "1"])

    with open(repo_with_notes, "r") as file:
        repository = json.load(file)

    assert result.exit_code == 0
    assert len(repository["notes"]) == 1
    assert repository["notes"][0]["content"] == "Another note."

def test_delete_non_existing_note(repo_with_notes, runner, test_app):
    result = runner.invoke(test_app, ["delete", "4"])

    assert result.exit_code == 0
    assert "There is no note with id 4 in the repository. Run `note list` to see all notes." in result.stdout