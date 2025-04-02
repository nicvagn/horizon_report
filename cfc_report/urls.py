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

from .views import create, home, player, view

urlpatterns = [
    path('', home.index, name='index'),

    # # CFC report # #
    # create a new report interactively
    path("create/", create.report.initial_form, name="create-report-info"),
    # add what players are in the report
    path("create/report-players", create.player.set_in_report,
         name="create-report-players"),
    # create a report skeleton from user info and ask for more
    path("create/report",
         create.report.cfc_report, name="create-report"),
    # add a match to the report
    path("create/report/match",
         create.match.chess_match, name="create-report-match"),
    # create round
    path("create/report/round",
         create.round.build, name="create-report-round"),
    path("create/report/round/confirm",
         create.round.build, name="create-round-build"),
    # # Player urls # #
    # add player to horizon report database
    path("create/new-player", player.add_player, name="add-new-player"),

]


# htmx url patterns, cleaner this way?
htmx_urlpatterns = [
    path("create/select-player/<str:cfc_id>",
         create.player.toggle_player_session, name="create-toggle-player"),
    path("create/select-match/<int:pk>",
         create.match.remove_match_session, name="select-match-round"),
    #path("create/select-round/<int:pk>", TODO
]

urlpatterns = urlpatterns + htmx_urlpatterns
