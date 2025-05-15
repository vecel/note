class NoteAppError(Exception):
    """
    Base class for all custom exceptions in the note application.
    """
    pass

class RepositoryDoesNotExistError(NoteAppError):
    """
    Raised when a note repository is not found in the current directory.
    """
    pass

class RepositoryCorruptedError(NoteAppError):
    """
    Raised when a note repository cannot be loaded, likely due to invalid
    content (e.g. malformed JSON).
    """
    pass