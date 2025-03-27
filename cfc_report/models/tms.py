"""tms.py - models for CFC TMS Tournament report file."""
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
from django.db import models
from cfc_report.models.tournament import Tournament


class TMS(models.Model):
    """model wrapping CFC TMS (Tournament Report) File format
    Attrabutes
    ---------

    TBA
    """
    tms = models.TextField(null=True)

    def __str__(self):
        tms = ""
        for line in self.tms:
            tms = tms + line + "\n"
        return tms
