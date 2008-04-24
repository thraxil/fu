# Django settings for fusite project.

from settings_shared import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG
DATABASE_NAME = 'fu'             # Or path to database file if using sqlite3.

TEMPLATE_DIRS = (
    "/var/www/fu/stage/fusite/fu/templates"
)

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = '/tmp/fusite/data/'







