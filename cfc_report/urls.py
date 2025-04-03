""" urls for cfc_report """
# Copyright (C) 2024  Nicolas Vaagen
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
import os

from django.urls import path

from .views import create, home, player

# Define reusable prefix constants
CFC_REPORT_PATH_PREFIX = "create/"
CREATE_REPORT_PATH_PREFIX = "create/report/"
CREATE_ROUND_PATH_PREFIX = os.path.join(CREATE_REPORT_PATH_PREFIX, "round/")

# Organized urlpatterns
urlpatterns = [
    # Home index
    path('', home.index, name='index'),

    # CFC report URLs
    *[
        path(CFC_REPORT_PATH_PREFIX + "create/", create.report.initial_form, name="create-report-info"),
        path(CFC_REPORT_PATH_PREFIX + "report-players", create.player.set_in_report, name="create-report-players"),
        path(CREATE_REPORT_PATH_PREFIX, create.report.cfc_report, name="create-tournament-report"),
        path(CREATE_REPORT_PATH_PREFIX + "match", create.match.chess_match, name="create-report-match"),
        path(CREATE_ROUND_PATH_PREFIX, create.round.build, name="create-report-round"),
        path(CREATE_ROUND_PATH_PREFIX + "confirm", create.round.build, name="create-round-build"),
    ],

    # Player-related URLs
    path(CFC_REPORT_PATH_PREFIX + "new-player", player.add_player, name="add-new-player"),
]

# htmx url patterns, cleaner this way?
htmx_urlpatterns = [
    path("create/select-player/<str:cfc_id>",
         create.player.toggle_player_session, name="create-toggle-player"),
    path("create/select-match/<int:pk>",
         create.match.remove_match_session, name="select-match-round"),
    path("create/select-round/<int:pk>",
         create.round.select_round, name="create-select-round"),
]

urlpatterns = urlpatterns + htmx_urlpatterns
