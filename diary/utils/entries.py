from pathlib import Path
import json

from diary import config
from diary.utils.models import Entry, MediaEntry


def check_file_ok(directory: Path, file: Path = None, create: bool = False) -> bool:

    if not create:
        return directory.exists() and (file is None or file.exists())

    try:
        directory.mkdir(parents=True, exist_ok=True)
        if file is not None:
            file.touch(exist_ok=True)
    except PermissionError:
        return False
    return True


def get_entry_path(entry_name: str, create: bool = False) -> Path | None:
    subdirectory = config.DATA_DIR / entry_name
    filename = subdirectory / config.ENTRY_FILE_NAME

    if not check_file_ok(directory=subdirectory, file=filename, create=create):
        return None
    return filename


def get_entry_media_path(entry_name: str, create: bool = False) -> Path | None:
    subdirectory = config.DATA_DIR / entry_name / config.MEDIA_SUBDIR_NAME

    if not check_file_ok(directory=subdirectory, create=create):
        return None
    return subdirectory


def get_metadata_path(entry_name: str, create: bool = False) -> Path | None:
    subdirectory = config.DATA_DIR / entry_name
    filename = subdirectory / config.METADATA_FILE_NAME

    if not check_file_ok(directory=subdirectory, file=filename, create=create):
        return None
    return filename


def get_metadata(entry_name: str, create: bool = False) -> Entry | None:
    metadata_path = get_metadata_path(entry_name, create=create)

    if metadata_path is None:
        return None

    with open(str(metadata_path), 'r') as f:
        content = f.read()

    return Entry.from_dict(json.loads(content) if content else {})


def update_media_metadata(
    current: list[MediaEntry],
    update: list[MediaEntry]
) -> list[MediaEntry]:
    existing_data_mapping = {i.file_name: i for i in current}
    update_data_mapping = {i.file_name: i for i in update}

    existing_data_mapping.update(update_data_mapping)
    return list(existing_data_mapping.values())


def upsert_metadata(
    metadata_path: str,
    entry_data: Entry
):
    with open(metadata_path, 'r') as f:
        content = f.read()

    metadata = Entry.from_dict(json.loads(content) if content else {})
    if entry_data.title:
        metadata.title = entry_data.title
    if entry_data.tags:
        existing_tags: list = metadata.tags
        existing_tags.extend(entry_data.tags)
        metadata.tags = list(set(existing_tags))
    if entry_data.media:
        existing_data = metadata.media
        metadata.media = update_media_metadata(
            current=existing_data, update=entry_data.media
        )

    with open(metadata_path, 'w') as f:
        f.write(json.dumps(metadata.to_dict()))
