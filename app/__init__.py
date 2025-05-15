import toml

config = toml.load("pyproject.toml")

__app_name__ = config.get("tool", {}).get("poetry", {}).get("name", None)
__version__ = config.get("tool", {}).get("poetry", {}).get("version", None)
