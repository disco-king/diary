import os
from pathlib import Path
import json

import click

from diary.config import DATA_SUBDIR, MEDIA_SUBDIR_NAME


USER_HOME = Path.home()
DATA_DIR = USER_HOME / Path(DATA_SUBDIR)