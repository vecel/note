import re

from rich import print
from rich.table import Table
from rich.text import Text

from app.core.errors import NoteAppError
from app.core.models import Note

def parse_tags(tags: str):
    result = re.match("^[a-zA-Z0-9]+(,[a-zA-Z0-9]+)*$", tags)
    if result is None:
        raise NoteAppError("Note was not added because of an error. Tags " \
        "should be comma separated list of strings containing only " \
        "letters and numbers.") # TODO change to custom exception
    return tags.split(",")

def print_notes(notes: list[tuple[int, Note]]):
    table = Table(title="Your Notes")
    table.add_column("ID", width=6)
    table.add_column("Content", style="white", width=60)
    table.add_column("Tags", style="violet bold", width=16)

    for idx, note in notes:
        content, tags = note.content, note.tags
        tags = ' '.join(f"#{tag}" for tag in tags) if tags is not None else ''
        table.add_row(str(idx + 1), content, str(tags))
    
    print(table)

def print_tags(tags: list[str]):
    tags_list = ' '.join(f"#{tag}" for tag in tags)
    tags_list = Text(tags_list, style="violet bold")
    print(tags_list)
