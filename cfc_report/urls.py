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

from django.contrib import admin
from django.urls import path

from .views import home, player
from .views.report import create, view
from .services import session


urlpatterns = [
    path('', home.index, name='index'),

    # create
    path("create/", create.initial, name="create-report-info"),
    path("create/players", create.players, name="create-report-players"),
    path("create/match", create.chess_match, name="create-report-match"),
    path("create/round", create.round, name="create-report-round"),
    path("create/finalize/round", create.finalize_round, name="create-round-finalize"),
    path("create/finalize/report", create.finalize_report, name="create-report-finalize"),
    path("add-player", player.add_player, name="add-player"),

    # view
    path("view/", view.report, name="view-report"),
]

# htmx url patterns, cleaner this way?
htmx_urlpatterns = [
    path("create/select/<str:cfc_id>", create.toggle_player_session, name="create-toggle-player"),
    path("create/select-match/<int:pk>", create.remove_match_session, name="select-match-round")
]

urlpatterns = urlpatterns + htmx_urlpatterns
