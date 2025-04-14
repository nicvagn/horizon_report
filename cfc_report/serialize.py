"""views for cfc_report serializers"""
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
from django.core.serializers.json import DjangoJSONEncoder


class PlayerSerializer(DjangoJSONEncoder):
    """
    Custom JSON serializer for the Player model.
    """

    @staticmethod
    def serialize(player):
        """
        Serialize the Player instance as JSON.

        Parameters
        ----------
        player : Player
            An instance of the Player model.

        Returns
        -------
        dict
            A dictionary representation of the Player instance.
        """
        return {
            "id": player.id,
            "name": player.name,
            "cfc_id": player.cfc_id,
        }

    @staticmethod
    def serialize_list(players):
        """
        Serialize a list of Player instances as JSON.

        Parameters
        ----------
        players : list of Player
            A list of Player instances.

        Returns
        -------
        list of dict
            A list of dictionary representations of the Player instances.
        """
        return [PlayerSerializer.serialize(player) for player in players]

    @staticmethod
    def deserialize(data, player_model):
        """
        Deserialize a dictionary into a Player instance.

        Parameters
        ----------
        data : dict
            The dictionary containing player data.
        player_model : type
            The Player model class.

        Returns
        -------
        Player
            A Player instance constructed from the data.

        Raises
        ------
        ValueError
            If any required fields are missing or invalid.
        """
        try:
            # Validate required fields
            if not data.get("name") or not data.get("cfc_id"):
                raise ValueError("Missing required fields: 'name' and 'cfc_id'.")

            # Validate CFC ID
            if not str(data["cfc_id"]).isdigit() or len(str(data["cfc_id"])) != 6:
                raise ValueError("Invalid 'cfc_id'. It must be a 6-digit number.")

            return player_model(
                name=data["name"],
                cfc_id=int(data["cfc_id"]),
            )
        except (KeyError, TypeError) as e:
            raise ValueError(f"Invalid data format: {e}")

    @staticmethod
    def deserialize_list(data_list, player_model):
        """
        Deserialize a list of dictionaries into a list of Player instances.

        Parameters
        ----------
        data_list : list of dict
            A list of dictionaries containing player data.
        player_model : type
            The Player model class.

        Returns
        -------
        list of Player
            A list of Player instances constructed from the data.

        Raises
        ------
        ValueError
            If any required fields are missing or invalid in any of the dictionaries.
        """
        return [PlayerSerializer.deserialize(data, player_model) for data in data_list]
