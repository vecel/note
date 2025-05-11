"""
Initialization command for the note application.

This module defines the `init` command which prepares the environment
for storing notes. It typically creates a `.notes` file in the current 
directory.
"""

import typer

app = typer.Typer()

@app.command()
def init():
    print("Initializing .notes file.")