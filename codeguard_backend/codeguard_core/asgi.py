"""
ASGI config for codeguard_core project.
Yields asynchronous capability for high-concurrency connections.
"""

import os
from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "codeguard_core.settings")

application = get_asgi_application()