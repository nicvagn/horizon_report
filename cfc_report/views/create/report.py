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
from cfc_report.types import TournamentInfo


class ReportFormView(FormView):
    """A form view for generating reports for the CFC models."""
    template_name = "cfc_report/base/base-form.html"
    form_class = TournamentInfoForm
    success_url = reverse_lazy("report-tournament-players")
    extra_context = {
        "title": "Enter tournament information",
        "submit_btn_txt": "Pick Players",
    }

    def form_valid(self, form: TournamentInfoForm):
        """Called when the Tournament Info Form is valid.

        This method sets the session tournament details and completes the form processing.
        """
        self.set_session_tournament_info(form)
        return super().form_valid(form)

    def set_session_tournament_info(self, form: TournamentInfoForm):
        """Sets tournament information in the user's session for later use.

        Args:
            form (TournamentInfoForm): The form containing valid tournament data.
        """
        session_data: TournamentInfo = {
            "name": form.cleaned_data.get("name"),
            "num_rounds": form.cleaned_data.get("num_rounds"),
            "start_date": form.cleaned_data.get("start_date"),
            "end_date": form.cleaned_data.get("end_date"),
            "pairing_system": form.cleaned_data.get("pairing_system"),
            "province": form.cleaned_data.get("province"),
            "to_cfc": form.cleaned_data.get("to_cfc"),
            "td_cfc": form.cleaned_data.get("td_cfc"),
        }
        self.request.session["tournament_info"] = session_data
