import os, sys

sys.path.append('/var/www/fu/stage/')
sys.path.append('/var/www/fu/stage/fusite/')

os.environ['DJANGO_SETTINGS_MODULE'] = 'fusite.settings'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()
