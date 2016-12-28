# +++++++++++ DJANGO +++++++++++
# To use your own django app use code like this:
import os
import sys

# assuming your django settings file is at '/home/myusername/mysite/mysite/settings.py'
path = '/home/mrsaltz/thepub'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'

# serve django via WSGI
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()