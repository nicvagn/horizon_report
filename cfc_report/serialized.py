
"""Data classes for serialized objects for CFC rated tournament"""
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

class SerializedPlayer(TypedDict):
    """A serialized Player ready to be JSON
    Attributes
    ----------
    name : str
        Player's name
    cfc_id : str
        Player's cfc_id, CFC id's must be 6 numbers, ie: 222333
    """
    name: str
    cfc_id: str
