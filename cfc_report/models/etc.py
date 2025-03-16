"""Data models related to ..."""

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

class Province(models.TextChoices):
    """A Canadian province

    Attributes
    ----------
    ON : "Ontario"
        The province of onterio
    ... : ...
        One for every province
    """

    ON = "Ontario"
    QC = "Quebec"
    NS = "Nova Scotia"
    NB = "New Brunswick"
    MB = "Manitoba"
    BC = "British Columbia"
    PE = "Prince Edward Island"
    SK = "Saskachewan"
    AB = "Alberta"
    NL = "Newfoundland and Labrador"
