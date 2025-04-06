"""Create a Report for a CFC Rated tournament."""
# Copyright (C) 2024 Nicolas Vaagen
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

from django.urls import reverse_lazy
from django.views.generic.edit import FormView

from cfc_report.forms.tournament_info_form import TournamentInfoForm


class ReportFormView(FormView):
    """A form view for generating reports for the cfc models."""
    template_name = "cfc_report/base/base-form.html"
    form_class = TournamentInfoForm
    # reverse_lazy is needed, or produces a circular input
    success_url = reverse_lazy("report-tournament-players")
    extra_context = {
        "title": "Enter tournament information",
        "submit_btn_txt": "Pick Players",
    }
