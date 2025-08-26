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

DATE_ENV_VAR = 'DIARY_TODAY'

META_EDIT_TEXT = '''# Edit metadata values below.
# All edited values must follow the format `key: [value[,value,...]]`.
# Only uncommented lines following the format will be updated.
# If a key is removed or left with no value, it will be erased in metadata.
'''

MEDIA_META_EDIT_TEXT = '''# Note: changing the file name is not supported.
# The command will error out.
'''

ROOT_HELP = f"""
A CLI tool for documenting your life.

Most commands take a DATE (Y-M-D) parameter that determines which day's entry to manage.
If the parameter is not provided, today's entry is chosen by default.
It is also possible to set the {DATE_ENV_VAR} variable to change the default date.
"""

MEDIA_HELP = """
Manage entry media.

All commands in this group take a required argument FILE which determines the managed file.
It is either a local file path to add to an entry, or a name of a file that belongs to an entry.
"""
