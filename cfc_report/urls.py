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

from django.urls import path

from .views import create, add_player_view
from .views.index import IndexView

# Define reusable prefix constants
CFC_REPORT_PATH_PREFIX = ""

# Organized urlpatterns
urlpatterns = [
    # cfc index
    path(CFC_REPORT_PATH_PREFIX, IndexView.as_view(), name='index'),

    # CFC report URLs
    *[
        path(CFC_REPORT_PATH_PREFIX + "create/", create.report.initial_form, name="create-report-info"),
        path(CFC_REPORT_PATH_PREFIX + "report-players", create.player.set_in_report, name="create-report-players"),
    ],

    # Player-related URLs
    path(CFC_REPORT_PATH_PREFIX + "new-player", add_player_view, name="add-new-player"),
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
