"""
WSGI config for horizon_report project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "horizon_report.settings")

from configurations.wsgi import get_wsgi_application
application = get_wsgi_application()
