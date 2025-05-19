from dataclasses import dataclass, asdict

@dataclass
class Note:
    id: int
    content: str
    tags: list[str] | None

    @staticmethod
    def create(content: str, tags: list[str] | None = None):
        return Note(1, content, tags)

    def to_dict(self):
        return asdict(self)