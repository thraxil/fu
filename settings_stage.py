# Django settings for fusite project.
from settings_shared import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASE_NAME = 'fu_stage'             # Or path to database file if using sqlite3.

TEMPLATE_DIRS = (
    "/var/www/fu/stage/fusite/fu/templates"
)

MEDIA_ROOT = '/var/www/fu/stage/data/'



