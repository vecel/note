from app.core import storage

def create_repository():
    return storage.create_repository()

def add_note(content: str): # TODO change to Note object
    repository = storage.load_repository()
    # TODO update repository dict
    storage.save_repository({"note1": content})

