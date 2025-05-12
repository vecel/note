"""
Initialization command for the note application.

This module defines the `init` command which prepares the environment
for storing notes. It typically creates a `.notes` file in the current 
directory.
"""
import os
import typer

from app import NOTES_FILENAME

app = typer.Typer()

@app.command()
def init():
    """
    Initializes empty notes repository in working directory.
    """
    try:
        with open(NOTES_FILENAME, "x") as _:
            print("Initialized empty notes repository.")
    except FileExistsError:
        path = os.path.join(os.getcwd(), NOTES_FILENAME)
        print(f"Notes repository already initialized in {path}")