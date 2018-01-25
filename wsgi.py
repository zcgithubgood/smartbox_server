import os
import sys
from django.core.handlers.wsgi import WSGIHandler

homedir = os.getcwd()
sys.path.append(homedir)
os.environ["DJANGO_SETTINGS_MODULE"] = "smartbox.settings"
application = WSGIHandler()
