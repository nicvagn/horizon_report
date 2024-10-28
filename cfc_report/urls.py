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

from .views import home, player, report

urlpatterns = [
    path('', home.index, name='index'),
    # path("player/<slug:slug>", views.view_player, name="view-player"),
    path("view/", report.view, name="view-report"),
    path("create/", report.Create.initial, name="create-report-info"),
    path("create/players", report.Create.players,
         name="create-report-players"),
    path("create/select/<int:cfc_id>/", player.pick_player, name="pick-player"),
    path("add-player", player.add_player, name="add-player"),
]
