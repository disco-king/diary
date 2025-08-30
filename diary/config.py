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

ENTRY_REF_VARNAME = 'entry'
ENTRY_REF_METAVAR = 'ENTRY'
FILE_VARNAME = 'file'
FILE_METAVAR = 'FILE'

LIST_CMDNAME = 'list'

NAME_OPTION_METAVAR = 'NAME'
TAG_OPTION_METAVAR = 'TAG'

FILENAME_METAVAR = 'NAME'
COMMENT_METAVAR = 'COMMENT'

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

Most commands take a {ENTRY_REF_METAVAR} parameter that determines which day's entry to manage.
It can be either a date (Y-M-D) or the entry number in the main listing (`{PROGNAME} {LIST_CMDNAME}`).
If the parameter is not provided, today's entry is chosen by default.
It is also possible to set the {DATE_ENV_VAR} variable to change the default date.
"""

MEDIA_HELP = """
Manage entry media.

All commands in this group take a required argument FILE which determines the managed file.
It is either a local file path to add to an entry, or a name of a file that belongs to an entry.
"""

WRITE_HELP = f"""
Write an entry.

Write a new entry or edit an existing one.
The {ENTRY_REF_METAVAR} parameter determines which entry to write,
and additional metadata can be added via {NAME_OPTION_METAVAR} and {TAG_OPTION_METAVAR} options.
"""

ADD_MEDIA_HELP = f"""
Add media to an entry.

Provide a local file path in the {FILE_METAVAR} param.
The file will be added to the entry {ENTRY_REF_METAVAR} or today's entry by default.
The file can be named via {FILENAME_METAVAR}
and described via {COMMENT_METAVAR} options - useful for later management.
"""
