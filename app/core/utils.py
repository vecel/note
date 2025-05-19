import re

def parse_tags(tags: str):
    result = re.match("^[a-zA-Z0-9]+(,[a-zA-Z0-9]+)*$", tags)
    if result is None:
        raise Exception("Invalid tags format.") # TODO change to custom exception
    return tags.split(",")