from pathlib import Path
import json

from diary import config


def check_file_ok(directory: Path, file: Path = None) -> bool:
    try:
        directory.mkdir(parents=True, exist_ok=True)
        if file is not None:
            file.touch(exist_ok=True)
    except PermissionError:
        return False
    return True


def get_entry_path(entry_name: str) -> str | None:
    subdirectory = config.DATA_DIR / entry_name
    filename = subdirectory / config.ENTRY_FILE_NAME

    if not check_file_ok(directory=subdirectory, file=filename):
        return None
    return str(filename)


def get_entry_media_path(entry_name: str) -> str | None:
    subdirectory = config.DATA_DIR / entry_name / config.MEDIA_SUBDIR_NAME

    if not check_file_ok(directory=subdirectory):
        return None
    return str(subdirectory)


def get_metadata_path(entry_name: str) -> str | None:
    subdirectory = config.DATA_DIR / entry_name
    filename = subdirectory / config.METADATA_FILE_NAME

    if not check_file_ok(directory=subdirectory, file=filename):
        return None
    return str(filename)


def get_metadata(entry_name) -> dict:
    metadata_path = get_metadata_path(entry_name)

    if metadata_path is None:
        return {}

    with open(metadata_path, 'r') as f:
        content = f.read()
    return json.loads(content) if content else {}


def update_media_metadata(
    current: list[dict[str, str]],
    update: list[dict[str, str]]
) -> list[dict[str, str]]:
    existing_data_mapping = {i[config.MEDIA_META_NAME_KEY]: i for i in current}
    update_data_mapping = {i[config.MEDIA_META_NAME_KEY]: i for i in update}

    existing_data_mapping.update(update_data_mapping)
    return list(existing_data_mapping.values())


def upsert_metadata(
        metadata_path: str,
        title: str = None,
        tags: tuple[str] = None,
        media_entries: list[dict[str, str]] = None,
):
    with open(metadata_path, 'r') as f:
        content = f.read()

    metadata = json.loads(content) if content else {}
    if title:
        metadata[config.METADATA_TITLE_KEY] = title
    if tags:
        existing_tags: list = metadata.get(config.METADATA_TAGS_KEY, [])
        existing_tags.extend(tags)
        metadata[config.METADATA_TAGS_KEY] = list(set(existing_tags))
    if media_entries:
        existing_data = metadata.get(config.METADATA_MEDIA_KEY, [])
        metadata[config.METADATA_MEDIA_KEY] = update_media_metadata(
            current=existing_data, update=media_entries
        )

    with open(metadata_path, 'w') as f:
        f.write(json.dumps(metadata))
