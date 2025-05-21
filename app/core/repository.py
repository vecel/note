"""
Provides high-level operations on the note repository, such as creating the repository
and adding notes. This module separates core logic from low-level file storage operations.
"""
from app.core import storage
from app.core.models import Note
from app.core.errors import RepositoryCorruptedError, NotesNotFoundError
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
    """
    repository = storage.load_repository()
    
    if "notes" not in repository.keys():
        raise RepositoryCorruptedError("Notes repository does not contain field 'notes'.")

    repository["notes"].append(note.to_dict())
    storage.save_repository(repository)

def list_notes(tag_filter: list[str] | None = None):
    repository = storage.load_repository()
    notes_list = repository["notes"]

    if not notes_list:
        raise NotesNotFoundError("Repository is empty. Run `note add` to add a note.")
    
    notes = [Note(**note) for note in notes_list]
    if tag_filter is not None:
        notes = [note for note in notes if note.tags and set(note.tags) & set(tag_filter)]
    if not notes:
        # TODO add filter to print statement
        raise NotesNotFoundError("There are no notes matching given tag filter in repository.")
    print_notes(notes)

def list_tags():
    repository = storage.load_repository()
    notes_list = repository["notes"]
    tags = [note["tags"] for note in notes_list if note["tags"]]
    tags = [tag for group in tags for tag in group]
    if not tags:
        raise NotesNotFoundError("There are no tagged notes in the repository.")
    print_tags(tags)
