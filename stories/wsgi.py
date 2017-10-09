"""
WSGI config for stories project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os
import sys

path = '/home/stainlesstalong/pythonanywhere_blog/stories'
if path not in sys.path:
	sys.path.append(path)

os.environ["DJANGO_SETTINGS_MODULE"] = "stories.settings"

from django.core.wsgi import get_wsgi_application
from django.contrib.staticfiles.handlers import StaticFilesHandler
application = StaticFilesHandler(get_wsgi_application())



# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "stories.settings")
#
# application = get_wsgi_application()
