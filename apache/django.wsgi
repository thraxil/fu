import os, sys

sys.path.append('/var/www/fu/prod/')
sys.path.append('/var/www/fu/prod/fusite/')

os.environ['DJANGO_SETTINGS_MODULE'] = 'fusite.settings_production'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()
