# Django settings for fusite project.
from settings_shared import *

DEBUG = False
TEMPLATE_DEBUG = DEBUG

DATABASE_NAME = 'fu' 

TEMPLATE_DIRS = (
    "/var/www/fu/prod/fusite/fu/templates"
)

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = '/var/www/fu/prod/data/'

SERVER_EMAIL = 'anders@columbia.edu'
