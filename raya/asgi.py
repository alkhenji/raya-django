"""
ASGI config for raya project.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'raya.settings')

application = get_asgi_application() 