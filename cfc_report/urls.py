"""
urls for cfc_report
"""
from django.urls import path

from .views import player_views, create
from .views.index import IndexView

# Base URL prefix for this app (defined for clarity and reuse)
BASE_URL_PREFIX = ""

# Path prefixes for specific subsections
PLAYER_URL_PREFIX = f"{BASE_URL_PREFIX}/player/"

# URL patterns for the cfc_report app
urlpatterns = [
    # Index page
    path(BASE_URL_PREFIX, IndexView.as_view(), name="index"),

    # Report creation
    path(f"{BASE_URL_PREFIX}report/", create.report.ReportFormView.as_view(), name="create-report-info"),

    # Player creation
    path(f"{PLAYER_URL_PREFIX}add-player", player_views.add_player_database, name="add-new-player"),
    # Player selection (htmx related URL)
    path(
        PLAYER_URL_PREFIX + "<str:cfc_id>",
        player_views.toggle_player_session,
        name="create-toggle-player",
    ),
]
