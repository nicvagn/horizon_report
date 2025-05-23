"""
urls for cfc_report
"""
from django.urls import path

from .views.create.match import chess_match
from .views.create.round import create_round_view
from .views.database.add_player_database import add_player_database
from .views.index import IndexView
from .views.report.create_view import CreateReportView
from .views.report.info_form_view import (ReportInfoFormView,
                                          valid_form_create_tournament)
from .views.report.players_view import TournamentPlayersView, add_player_tournament
from .views.see.details import tournament_detail

# URL prefix constants for better readability and reusability
TOURNAMENT_PLAYERS_PATH = "tournament-players"
ADD_PLAYER_PATH = "add-player/"

# URL constants to aid in portability
# Base URL prefix for this app (defined for clarity and reuse)
BASE_URL_PREFIX = ""
# Path prefixes for specific subsections
PLAYER_URL_PREFIX = f"{BASE_URL_PREFIX}player/"
# Report URL prefix
REPORT_URL_PREFIX = f"{BASE_URL_PREFIX}report/"
# ROUND_URL_PREFIX
ROUND_URL_PREFIX = f"{REPORT_URL_PREFIX}round/"

urlpatterns = [
    # Index page
    path(BASE_URL_PREFIX, IndexView.as_view(), name="index"),

    # Player-related operations
    path(f"{PLAYER_URL_PREFIX}{ADD_PLAYER_PATH}",
         add_player_database, name="add-new-player"),

    # Report-related operations
    # # initial and players
    path(f"{REPORT_URL_PREFIX}", ReportInfoFormView.as_view(),
         name="create-report-initial"),

    # # initial - creates the tournament model and sets session vars
    path(f"{REPORT_URL_PREFIX}", valid_form_create_tournament,
         name="report-tournament-initial"),

    # # in progress
    path(f"{REPORT_URL_PREFIX}in-progress", CreateReportView.as_view(),
         name="create-report-overview"),
    # # tournament players
    path(f"{REPORT_URL_PREFIX}players/", TournamentPlayersView.as_view(),
         name='report-tournament-players'),

    path(f"{REPORT_URL_PREFIX}players/add", add_player_tournament,
         name='report-tournament-add-player'),

    # # Round
    path(f"{ROUND_URL_PREFIX}", create_round_view, name="report-create-round"),
    # # # Match creation
    path(f"{ROUND_URL_PREFIX}match", chess_match, name="report-create-match"),

    # Details
    path(f"{BASE_URL_PREFIX}details/tournament/<int:pk>/", tournament_detail,
         name="tournament-detail"),

]
