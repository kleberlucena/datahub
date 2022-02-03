import os

from django.core.wsgi import get_wsgi_application
from dj_static import MediaCling, Cling

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

application = Cling(MediaCling(get_wsgi_application()))
