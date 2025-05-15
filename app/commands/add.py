"""
Command for adding notes for the repository.

This module defines the `add` command which saves note to repository.
"""
import typer
from typing_extensions import Annotated

from app.core.repository import add_note
from app.core.errors import NoteAppError

app = typer.Typer()

@app.command()
def add(
    content: Annotated[
        str,
        typer.Argument(
            help="Content of the note."
        )
    ],
    tags: Annotated[
        str | None, 
        typer.Option(
            "--tags", 
            "-t", 
            help="Tags to be added to the note. Should be a string of comma" \
            " separated values with no white characters between."
        )
    ] = None
):
    """
    Adds a new note with specified CONTENT and optional TAGS.

    --tags should be a string of comma separated values associated to the
    note (e.g. "personal,todo"). 
    """
    # TODO check whether .notes exists (if not -> return code =/= 0 and print hint to use `note init`)
    # TODO create note object and save it to database

    try:
        add_note(content)
    except NoteAppError as error:
        print(error)