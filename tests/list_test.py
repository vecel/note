import os

def test_list(repo_with_notes, runner, test_app):
    result = runner.invoke(test_app, ["list"])

    assert result.exit_code == 0
    assert "New note." in result.stdout
    assert "Another note." in result.stdout
    assert "#mytag" in result.stdout
    assert "#awesome" in result.stdout

def test_list_empty_repository(repo_initialized, runner, test_app):
    result = runner.invoke(test_app, ["list"])

    assert result.exit_code == 0
    assert "Repository is empty. Run `note add` to add a note." in result.stdout

def test_list_repository_not_initialized(tmp_path, runner, test_app):
    os.chdir(tmp_path)
    result = runner.invoke(test_app, ["list"])

    assert result.exit_code == 0
    assert f"Notes repository does not exist. Run `note init` to initialize repository." in result.stdout

def test_list_tags(repo_with_notes, runner, test_app):
    result = runner.invoke(test_app, ["list", "-T"])

    assert result.exit_code == 0
    assert "#mytag #awesome" in result.stdout

def test_list_no_tags(repo_with_untagged_notes, runner, test_app):
    result = runner.invoke(test_app, ["list", "-T"])

    assert result.exit_code == 0
    assert "There are no tagged notes in the repository." in result.stdout

def test_list_tag_filter(repo_with_notes, runner, test_app):
    result = runner.invoke(test_app, ["list", "-t", "awesome"])

    assert result.exit_code == 0
    assert "Another note." in result.stdout
    assert "New note." not in result.stdout

def test_list_tag_filter_no_matching_tag(repo_with_notes, runner, test_app):
    result = runner.invoke(test_app, ["list", "-t", "nonexisting"])

    assert result.exit_code == 0
    assert "There are no notes matching given tag filter in repository." in result.stdout

def test_list_note_id_with_tag_filter(repo_with_notes, runner, test_app):
    result = runner.invoke(test_app, ["list", "-t", "awesome"])

    assert result.exit_code == 0
    assert "1" not in result.stdout
    assert "2" in result.stdout