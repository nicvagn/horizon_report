"""Get info for Report for a CFC Rated tournament."""
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
from cfc_report.models.roster import Roster
from cfc_report.models.tournament import Tournament
from . import logger


def valid_form_create_tournament(form: TournamentInfoForm) -> Tournament:
    """Creates (involves save) Tournament instance from form data.

    Args:
        form (TournamentInfoForm): The validated form containing tournament data.

    Returns:
        Tournament: The created Tournament instance.
    """
    # create an empty roster for a tournament
    roster = Roster.objects.create()

    tournament = Tournament.objects.create(
        name=form.cleaned_data.get("name"),
        num_rounds=form.cleaned_data.get("num_rounds"),
        start_date=form.cleaned_data.get("start_date"),
        end_date=form.cleaned_data.get("end_date"),
        pairing_system=form.cleaned_data.get("pairing_system"),
        province=form.cleaned_data.get("province"),
        to_cfc=form.cleaned_data.get("to_cfc"),
        td_cfc=form.cleaned_data.get("td_cfc"),
        roster=roster,
    )
    return tournament


class ReportInfoFormView(FormView):
    """A form view for generating initial report info for CFC rated
    tournament."""
    template_name = "cfc_report/base/base-form.html"
    form_class = TournamentInfoForm
    success_url = reverse_lazy("report-players")
    extra_context = {
        "title": "Enter tournament information",
        "submit_btn_txt": "Pick Players",
    }

    def form_valid(self, form: TournamentInfoForm):
        """Called when the Tournament Info Form is valid.

        This method sets the session tournament details and completes the
        form processing.
        """

        t = valid_form_create_tournament(form)
        t.save()
        logger.debug(
            "ReportInfoFormView.form_valid - Created (and saved in db) Tournament model: %s" % t)
        self.set_session_tournament_info(t)

        return super().form_valid(form)

    def set_session_tournament_info(self, tournament: Tournament):
        """Sets tournament information in the user's session for later use.

        Args:
             (TournamentInfoForm): The form containing valid tournament data.
        """
        self.request.session["round_number"] = 1
        self.request.session["tournament_id"] = tournament.id
        logger.debug("set 'tournament_id' and 'round_number' in session")
