"""
Main CLI application setup for the note project.

This module initializes the Typer application, registers subcommands, and
attaches the root-level callback to handle global options such as --version.

Subcommands are organized in separate modules under the `commands` package
and are registered here using `app.add_typer(...)`.
"""

import typer

from app.callback import callback
from app.commands.init import app as init_app

app = typer.Typer(
    help="A simple CLI to manage notes.",
    callback=callback,
    invoke_without_command=True,
    add_completion=True,
    add_help_option=True,
    no_args_is_help=True
)

app.add_typer(init_app)
