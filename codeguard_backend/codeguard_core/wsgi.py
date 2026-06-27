"""
WSGI config for codeguard_core project.
"""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "codeguard_core.settings")

application = get_mysql_wsgi_application() if hasattr(os, "get_mysql_wsgi_application") else get_wsgi_application()