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

NON_PAGED_ENTRY_COUNT = 100
SHORT_TEXT_SYMBOL_LIMIT = 30
META_ATTR_WIDTH = 34

DATE_ENV_VAR = 'DIARY_TODAY'

META_EDIT_TEXT = '''# Edit metadata values below.
# All edited values must follow the format `key: [value[,value,...]]`.
# Only uncommented lines following the format will be updated.
# If a key is removed or left with no value, it will be erased in metadata.
'''

MEDIA_META_EDIT_TEXT = '''# Note: changing the file name is not supported.
# The command will error out.
'''
