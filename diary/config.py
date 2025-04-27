from pathlib import Path
from os import path

PROGNAME = 'diary'

ROOT_SUBDIR = '.diary'
DATA_SUBDIR = path.join(ROOT_SUBDIR, 'data')
ENTRY_FILE_NAME = 'entry.txt'
METADATA_FILE_NAME = 'meta.json'
MEDIA_SUBDIR_NAME = 'media'

USER_HOME = Path.home()
DATA_DIR = USER_HOME / Path(DATA_SUBDIR)

METADATA_TITLE_KEY = 'title'
METADATA_TAGS_KEY = 'tags'
METADATA_MEDIA_KEY = 'media'
MEDIA_META_NAME_KEY = 'file_name'
MEDIA_META_DESCRIPTION_KEY = 'description'

NON_PAGED_ENTRY_COUNT = 100
