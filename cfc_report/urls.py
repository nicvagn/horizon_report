"""
urls for cfc_report
"""
from django.urls import path

from .views import player_views, create
from .views.index import IndexView

from .constants import BASE_URL_PREFIX, PLAYER_URL_PREFIX, REPORT_URL_PREFIX

# URL patterns for the cfc_report app
urlpatterns = [
    # Index page
    path(BASE_URL_PREFIX, IndexView.as_view(), name="index"),

    # Player creation (for Player db)
    path(f"{PLAYER_URL_PREFIX}add-player", player_views.add_player_database,
         name="add-new-player"),

    # Report creation
    *[
        path(f"{REPORT_URL_PREFIX}", create.report.ReportFormView.as_view(),
             name="create-report-info"),
        # choose players in report
        path(f"{REPORT_URL_PREFIX}/players",
             player_views.set_tournament_players,
             name="create-tournament-players"),
    ],

    # selection (htmx related URL)
    *[
        # toggle player session
        path(
            PLAYER_URL_PREFIX + "select/<str:cfc_id>",
            player_views.toggle_player_session,
            name="create-toggle-player",
        ),
    ]
]
