from dataclasses import dataclass, field, asdict


@dataclass
class MediaEntry:
    file_name: str
    description: str = None

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)

    def to_dict(self):
        return asdict(self)


@dataclass
class Entry:
    title: str = None
    tags: list[str] = field(default_factory=list)
    media: list[MediaEntry] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict):
        media = data.pop('media', [])
        media_entries = [MediaEntry.from_dict(m) for m in media]
        data['media'] = media_entries
        return cls(**data)

    def to_dict(self):
        return asdict(self)
