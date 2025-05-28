"""
Provides high-level operations on the note repository, such as creating the repository
and adding notes. This module separates core logic from low-level file storage operations.
"""
from app.core import storage
from app.core.models import Note, Status, NoteWithStatus
from app.core.errors import RepositoryCorruptedError, NotesNotFoundError, NoteAppError, StatusDoesNotExistError
from app.core.utils import print_notes, print_tags

def create_repository():
    """
    Initializes a new note repository by delegating to the storage layer.

    Returns:
        Path: The absolute path to the newly created repository file.
    """
    return storage.create_repository()

def add_note(note: Note):
    """
    Adds a new note to the notes repository.

    This function loads the existing repository, verifies that it contains a
    'notes' field, appends the new note, and saves the updated repository 
    back to disk.

    Args:
        note (Note): The Note object to be added to the repository.

    Raises:
        RepositoryCorruptedError: If the loaded repository does not contain a 'notes' field,
                                  indicating it is improperly structured or corrupted.
        StatusDoesNotExistErrorl: If note is being created with non-existing status.
    """
    repository = storage.load_repository()
    notes = _get_notes(repository)
    statuses = _get_statuses(repository)
    
    if note.status and note.status not in statuses.keys():
        raise StatusDoesNotExistError(f"There is no status {note.status} in the repository configuration. Run `note list -S` to see all statuses or `note status --add STATUS` to add a new one.")

    notes.append(note.to_dict())

    _sort_notes(repository)

    storage.save_repository(repository)

def list_notes(tag_filter: list[str] | None = None):
    repository = storage.load_repository()
    notes = _get_notes_with_statuses(repository)

    if not notes:
        raise NotesNotFoundError("Repository is empty. Run `note add` to add a note.")
    
    if tag_filter is not None:
        notes = [note for note in notes if note.note.tags and set(note.note.tags) & set(tag_filter)]
        if not notes:
            filter_msg = ", ".join(tag_filter)
            raise NotesNotFoundError(f"There are no notes matching filter: '{filter_msg}' in repository.")
    
    print_notes(notes)

def list_tags():
    repository = storage.load_repository()
    notes = _get_notes(repository)
    tags = [note["tags"] for note in notes if note["tags"]]
    tags = [tag for group in tags for tag in group]
    if not tags:
        raise NotesNotFoundError("There are no tagged notes in the repository.")
    print_tags(tags)

def delete_note(id: int):
    repository = storage.load_repository()
    notes = _get_notes(repository)
    if not 1 <= id <= len(notes):
        raise NotesNotFoundError(f"There is no note with id {id} in the repository. Run `note list` to see all notes.")
    notes.pop(id - 1)
    storage.save_repository(repository)

def create_status(name: str, status: Status):
    repository = storage.load_repository()
    statuses = _get_statuses(repository)

    if name in statuses.keys():
        raise NoteAppError(f"Status {name} already exists. Use `note config status -e` to edit statuses.")
    
    statuses[name] = {
        "style": status.style,
        "priority": status.priority
    }
    storage.save_repository(repository)

def edit_status(name: str, status: Status):
    repository = storage.load_repository()
    statuses = _get_statuses(repository)

    if name not in statuses.keys():
        raise StatusDoesNotExistError(f"There is no status {name} in the repository configuration. Run `note list -S` to see all statuses or `note status --add STATUS` to add a new one.")
    
    statuses[name] = {
        "style": status.style,
        "priority": status.priority
    }

    _sort_notes(repository)

    storage.save_repository(repository)

def delete_status(name: str):
    repository = storage.load_repository()
    statuses = _get_statuses(repository)

    if name not in statuses.keys():
        raise StatusDoesNotExistError(f"There is no status {name} in the repository configuration. Run `note list -S` to see all statuses or `note status --add STATUS` to add a new one.")
    
    # TODO check whether there are notes with this status, if so ask user what to do or raise an exception

    statuses.pop(name)
    storage.save_repository(repository)

def _get_notes(repository: dict):
    if "notes" not in repository.keys():
        raise RepositoryCorruptedError("Notes repository does not contain field 'notes'.")
    return repository["notes"]

def _get_statuses(repository: dict):
    if "config" not in repository.keys():
        raise RepositoryCorruptedError("Notes repository does not contain field 'config'.")
    
    if "statuses" not in repository["config"].keys():
        raise RepositoryCorruptedError("Notes repository configuration does not contain field 'statuses'.")
    
    return repository["config"]["statuses"]

def _get_notes_with_statuses(repository: dict):
    notes = _get_notes(repository)
    statuses = _get_statuses(repository)

    return [NoteWithStatus(idx, Note(**note), Status(**statuses[note["status"]]) if note["status"] else Status.create()) for idx, note in enumerate(notes)]

def _sort_notes(repository: dict):
    notes = _get_notes(repository)
    statuses = _get_statuses(repository)

    notes.sort(key=lambda note_dict: 0 if note_dict["status"] is None else statuses[note_dict["status"]]["priority"], reverse=True)