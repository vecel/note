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
    assert "Notes repository does not exist. Run `note init` to initialize repository." in result.stdout

def test_list_tags(repo_with_notes, runner, test_app):
    result = runner.invoke(test_app, ["list", "-T"])

    assert result.exit_code == 0
    assert "#mytag" in result.stdout
    assert "#awesome" in result.stdout

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
    assert "There are no notes matching filter: 'nonexisting' in repository." in result.stdout

def test_list_note_id_with_tag_filter(repo_with_notes, runner, test_app):
    result = runner.invoke(test_app, ["list", "-t", "awesome"], env={"COLUMN": "80"})

    assert result.exit_code == 0
    assert "1" not in result.stdout
    assert "2" in result.stdout

def test_list_tags_displayed_only_once_with_tags_only(repo_with_notes, runner, test_app):
    result = runner.invoke(test_app, ["list", "-T"])

    assert result.exit_code == 0
    assert result.stdout.count("#mytag") == 1

def test_list_statuses_only(repo_with_notes, runner, test_app):
    result = runner.invoke(test_app, ["list", "-S"])

    assert result.exit_code == 0
    assert "COMPLETED  priority:  -2" in result.stdout
    assert "PRIORITY  priority:  10" in result.stdout