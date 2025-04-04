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

from .views import player_views, create
from .views.index import IndexView

# Define constants to avoid repetition
CFC_REPORT_BASE_PATH = ""  # Replace with the actual prefix value

# Define urlpatterns with better readability and structure
urlpatterns = [
    # Index page for cfc_report
    path(CFC_REPORT_BASE_PATH, IndexView.as_view(), name='index'),

    # Report creation URLs
    path(CFC_REPORT_BASE_PATH + "report/",
         create.report.ReportFormView.as_view(),
         name="create-report-info"
         )
]

# htmx url patterns, cleaner this way?
htmx_urlpatterns = [
    path("create/select-player/<str:cfc_id>",
         player_views.toggle_player_session, name="create-toggle-player"),
    # path("create/select-match/<int:pk>",
    # create.match.remove_match_session, name="select-match-round"),
    # path("create/select-round/<int:pk>",
    # create.round.select_round, name="create-select-round"),
]

urlpatterns = urlpatterns + htmx_urlpatterns
