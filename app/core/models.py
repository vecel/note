from dataclasses import dataclass, asdict

@dataclass
class Note:
    content: str
    tags: list[str] | None
    status: str | None

    @staticmethod
    def create(content: str, tags: list[str] | None = None, status: str | None = None):
        return Note(content, tags, status)

    def to_dict(self):
        return asdict(self)