import re

from app.core.errors import NoteAppError

def parse_tags(tags: str):
    result = re.match("^[a-zA-Z0-9]+(,[a-zA-Z0-9]+)*$", tags)
    if result is None:
        raise NoteAppError("Note was not added because of an error. Tags " \
        "should be comma separated list of strings containing only " \
        "letters and numbers.") # TODO change to custom exception
    return tags.split(",")