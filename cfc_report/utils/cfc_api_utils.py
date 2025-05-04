""" utilities for talking with CFC API"""
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
import requests

from . import logger

URL_STUB = "https://server.chess.ca"


def get_player_info(cfc_id: str):
    """Retrieve player information from CFC API.

    Gets player details including name, rating and membership status
    from the Chess Federation of Canada API.

    Parameters
    ----------
    cfc_id : str
        The CFC ID number of the player to look up.

    Returns
    -------
    dict - JSON response from the API.
        example:
        {'updated': '2025-04-24',
        'player': {
            'cfc_id': 123123,
            'cfc_expiry': '2020-01-02',
            'fide_id': 0,
            'name_first': 'Michael',
            'name_last': 'Williams',
            'addr_city': "St.John's",
            'addr_province': 'NL',
            'regular_rating': 200,
            'regular_indicator': 11,
            'quick_rating': 200,
            'quick_indicator': 11,
            'events': [{'id': 199806005,
                'name': 'MacDonald Dr RR',
                'date_end': '1998-05-14',
                'rating_type': 'R',
                'games_played': 11,
                'score': 0.0,
                'rating_pre': 0,
                'rating_perf': 0,
                'rating_post': 200,
                'rating_indicator': 11}],
            'orgarb': [],
            'is_organizer': False,
            'is_arbiter': False
        },
        'apicode': 0,
        'error': ''}

        Player information from the API response.
        Contains fields like name, rating, expiry date, etc.

    Raises
    ------
    requests.exceptions.RequestException
        If the API request fails for any reason
    ValueError
        If the response is not valid JSON
    """
    api_path = f"/api/player/v1/{cfc_id}"

    try:
        r = requests.get(URL_STUB + api_path)
        r.raise_for_status()

        api_info = r.json()
        logger.debug("CFC API response: %s", api_info)

        if "name_first" not in api_info["player"]:
            raise ValueError(f"cfc id: {cfc_id} did not return a player")

        return api_info["player"]

    except requests.exceptions.RequestException as e:
        raise requests.exceptions.RequestException(
            f"Failed to make request: {e}")
