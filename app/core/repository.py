"""
Provides high-level operations on the note repository, such as creating the repository
and adding notes. This module separates core logic from low-level file storage operations.
"""
from app.core import storage
from app.core.models import Note
from app.core.errors import RepositoryCorruptedError

def create_repository():
    """
    Initializes a new note repository by delegating to the storage layer.

    Returns:
        Path: The absolute path to the newly created repository file.
    """
    return storage.create_repository()

def add_note(note: Note):
    repository = storage.load_repository()
    
    if "notes" not in repository.keys():
        raise RepositoryCorruptedError("Notes repository does not contain field 'notes'.")

    repository["notes"].append(note.to_dict())
    storage.save_repository(repository)

