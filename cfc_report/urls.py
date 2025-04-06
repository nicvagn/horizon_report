"""
urls for cfc_report
"""
from django.urls import path

from .constants import BASE_URL_PREFIX, PLAYER_URL_PREFIX, REPORT_URL_PREFIX
from .views.create import ReportFormView
from .views.index import IndexView
from .views.player_views import (toggle_player_session_view,
                                 set_tournament_players, add_player_database)

# URL prefix constants for better readability and reusability
TOURNAMENT_PLAYERS_PATH = "tournament-players"
ADD_PLAYER_PATH = "add-player/"

urlpatterns = [
    # Index page
    path(BASE_URL_PREFIX, IndexView.as_view(), name="index"),

    # Player-related operations
    path(f"{PLAYER_URL_PREFIX}{ADD_PLAYER_PATH}",
         add_player_database, name="add-new-player"),

    # Report-related operations
    path(f"{REPORT_URL_PREFIX}", ReportFormView.as_view(), name="report-info"),
    path(f"{REPORT_URL_PREFIX}{TOURNAMENT_PLAYERS_PATH}",
         set_tournament_players, name="report-tournament-players"),

    # HTMX-related URLs
    path(f"{PLAYER_URL_PREFIX}select/<str:cfc_id>",
         toggle_player_session_view, name="report-toggle-player"),
]
