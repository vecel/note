from dataclasses import dataclass, asdict

@dataclass
class Note:
    content: str
    tags: list[str] | None

    # @staticmethod
    # def create(content: str, tags: list[str] | None = None):
    #     return Note(content, tags)

    def to_dict(self):
        return asdict(self)