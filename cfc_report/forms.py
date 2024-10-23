"""forms.py: Forms for CFC rated tournament"""
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
# set up logging
import logging
from django import forms
from .form_fields import CfcIdField, PairingSystemField, ProvinceField
from .constants import LOGGER_NAME
logger = logging.getLogger(LOGGER_NAME)


class TournamentForm(forms.Form):
    """for getting info on a CFC rated tournament

    Attributes
    ----------
    name : forms.CharField
        name of the tournament
    num_rounds : forms.IntegerField
        number of rounds
    date : forms.DateField
        The date of the tournament
    pairing_system : PairingSystem
        The pairing system used in this tournament.
    province : Province
        The canadian province this tournament was held
    to_cfc : CfcIdField
        The CFC ID of the TournamentOrganizer
    td_cfc : CfcIdField
        The CFC ID of the TournamentDirector
    """

    name = forms.CharField(max_length=60)
    num_rounds = forms.IntegerField()
    date = forms.DateField()
    pairing_system = PairingSystemField()
    province = ProvinceField()
    to_cfc = CfcIdField()  # TournamentOrganizer CFC id
    td_cfc = CfcIdField()  # TournamentDirector CFC id

    def add_player(self, player: "Player"):
        """Choose a player to be in created tournament

        Arguments
        ---------
        player : Player
            Chosen player

        Returns
        -------
            None
        """
        raise NotImplementedError

    def __str__(self):
        return f"""Tournament name: {self.name}
        Number of rounds: {self.num_rounds}
        date: {self.date}
        Pairing System: {self.pairing_system}
        province: {self.province}
        TournamentOrganizer CFC: {self.to_cfc}
        TournamentDirector CFC: {self.td_cfc}
        """