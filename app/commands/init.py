"""
Initialization command for the note application.

This module defines the `init` command which prepares the environment
for storing notes. It typically creates a `.notes` file in the current 
directory.
"""
import os

import typer
from typing_extensions import Annotated

from app import NOTES_FILENAME

app = typer.Typer()

@app.command()
def init():
    """
    Initializes empty notes repository in working directory.
    """
    try:
        with open(".notes", "x") as _:
            print("Initialized empty notes repository.")
    except FileExistsError:
        print(f"Notes repository already initialized in {os.getcwd()}/{NOTES_FILENAME}")