import os
import sys

sys.path.append('/srv/www/vhosts')

os.environ['DJANGO_SETTINGS_MODULE'] = 'econf.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

