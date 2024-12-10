"""Data services for modifying and creating data for a CFC rated tournament"""
# horizon_report
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

from cfc_report import logger
from cfc_report.models import (Match, Player, TournamentDirector,
                               TournamentOrganizer)
from django.db.models import QuerySet


def get_players() -> QuerySet:
    """Get players in database
    returns:
        QuerySet of players in db
    """
    all_players = Player.objects.all()
    logger.debug("get_players got these players from db: %s", all_players)
    return all_players


def get_player_by_cfc(cfc_id: "Cfc_id") -> Player:
    """Get a player by their cfc_id

    Returns
    -------
    Player
        The found player

    Raises
    ------
    DoesNotExist exception if player not found
    """
    p = Player.objects.get(cfc_id=cfc_id)
    logger.debug("Player %s got from cfc_id %s", p, cfc_id)
    return p


def add_player(p: Player) -> None:
    """Add a player to the database
    parameters:
        p: The models.Player object to add
    """
    logger.debug("player %s added to db", p)
    p.save()


def add_player_by_cfc(cfc_id: "CfcId", name: str) -> None:
    """Add a player to the database using name and cfcid
    parameters:
        cfc_id : "CfcId"
            the cfc id of the player
        name : str
            the players name.
    """

    p = Player(name, cfc_id)

    add_player(p)


def get_TDs() -> QuerySet:
    """Get TournamentDirector's in database
    returns:
        QuerySet of TD's
    """
    tds = TournamentDirector.objects.all()
    logger.debug("get_TDs got %s", tds)
    return tds


def get_TOs() -> QuerySet:
    """Get TournamentDirector's in database
    returns:
        QuerySet of TD's
    """
    tos = TournamentOrganizer.objects.all()
    logger.debug("get_TOs got: %s", tos)
    return tos


def get_matches() -> QuerySet:
    """Get the matches in the database

    Returns
    -------
    The matches in the Database
    """
    matches = Match.objects.all()
    logger.debug("get_matches got: %s", matches)

    return matches

def enter_round() -> None:
    """enter a round into database"""
    pass


def populate_database() -> None:
    """Populate the db with dumby data"""

    # players
    cfc_id = 111111
    players = []
    for n in ["charles Fool", "Jake Bell", "Albert Fish", "Jonny Boy",
              "Dad Dadderson", "11111111", "222222222", "33333333",
              "44444444444", "55555555555", "6666666"]:
        players.append(Player(name=n, cfc_id=str(cfc_id)))
        cfc_id += 1

    for p in players:
        p.save()

    # TournamentDirector
    td = []
    for n in ["Big Mommy", "Small Low"]:
        td.append(TournamentDirector(name=n, cfc_id=str(cfc_id)))
        cfc_id += 1

    for p in td:
        p.save()

    # TournamentOrganizer
    tos = []
    for n in ["Tonka Dump", "Great Leap"]:
        tos.append(TournamentOrganizer(name=n, cfc_id=str(cfc_id)))
        cfc_id += 1

    for p in tos:
        p.save()

    # Matches
    # create some filler data
    matches = []
    for n in range(int(len(players) / 2)):
        matches.append(
            Match(white=players[n], black=players[n+1], winner=players[n])
        )

    for m in matches:
        m.save()
