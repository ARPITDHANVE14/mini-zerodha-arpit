"""
WSGI config for mini_zerodha project.
"""
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mini_zerodha.settings')
application = get_wsgi_application()
