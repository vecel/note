import json
from pathlib import Path

from app.core import REPOSITORY_FILENAME
from app.core.errors import RepositoryDoesNotExistError, RepositoryCorruptedError

repository = Path() / REPOSITORY_FILENAME

def create_repository():
    try:
        with repository.open("x") as _:
            return repository.absolute()
    except FileExistsError:
        raise FileExistsError(f"Notes repository already initialized in {repository.absolute()}")

def load_repository():
    if not repository.exists():
        raise RepositoryDoesNotExistError(f"Notes repository does not exist. Run `note init` to initialize repository.")
    
    if repository.stat().st_size == 0:
        return {}
    
    try:
        with open(REPOSITORY_FILENAME, "r") as file:
            return json.load(file)
    except json.JSONDecodeError as error:
        raise RepositoryCorruptedError(f"Cannot read repository. File is not valid JSON. {error}")

def save_repository(repo: dict):
    if not repository.exists():
        raise RepositoryDoesNotExistError(f"Notes repository does not exist. Run `note init` to initialize repository.")
    
    with repository.open("w") as file:
        json.dump(repo, file)