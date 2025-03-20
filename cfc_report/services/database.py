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
import datetime

from cfc_report import logger
from cfc_report.models.person import (Player, TournamentDirector,
                                      TournamentOrganizer)
from cfc_report.models.tournament import Match, Roster, Round, Tournament
from cfc_report.models.cfc import CfcId
from cfc_report.models.fields import PairingSystemField
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404


# GET
def get_players() -> QuerySet:
    """Get players in database
    returns:
        QuerySet of players in db
    """
    all_players = Player.objects.all()
    logger.debug("get_players got these players from db: %s", all_players)
    return all_players


def get_player_by_cfc(cfc_id: CfcId) -> Player:
    """Get a player by their cfc_id

    Returns
    -------
    Player
        The found player

    Raises
    ------
    DoesNotExist exception if player not found
    """

    p = get_object_or_404(Player, cfc_id=cfc_id)

    logger.debug("Player %s got from cfc_id %s", p, cfc_id)
    return p


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


# ADD
def add_player(p: Player) -> None:
    """Add a player to the database
    parameters:
        p: The models.Player object to add
    """
    logger.debug("player %s added to db", p)
    p.save()


def populate_database() -> None:
    """Populate the db with dumby data"""
    cfc_id = 111111
    tournament = Tournament(name="Test Closed", num_rounds=1, date=datetime.now(), pairing_system=PairingSystemField.PAIRING_SYSTEMS["SW"])

    # players
    players = []
    for n in [
        "charles Fool",
        "Jake Bell",
        "Albert Fish",
        "Jonny Boy",
        "Dad Dadderson",
        "Joan Boat",
        "Carl Marz",
        "Lover Bou",
        "Paul Lark",
        "Papa Vaagen",
        "Alex Charter"
    ]:
        players.append(Player(name=n, cfc_id=CfcId(number=cfc_id)))
        cfc_id += 1

    for p in players:
        p.save()

    # TournamentDirector
    td = []
    for n in ["Big Mommy", "Small Low"]:
        td.append(TournamentDirector(name=n, cfc_id=CfcId(number=cfc_id)))
        cfc_id += 1

    for p in td:
        p.save()

    # TournamentOrganizer
    tos = []
    for n in ["Tonka Dump", "Great Leap"]:
        tos.append(TournamentOrganizer(name=n, cfc_id=CfcId(number=cfc_id)))
        cfc_id += 1

    for p in tos:
        p.save()

    first_round = Round(round_num=1, tournament=tournament)
    # Matches
    # create some filler data
    r = Match.RESULT_WHITE
    matches = []
    for n in range(int(len(players) / 2)):

        matches.append(
            Match(white=players[n], black=players[n + 1],
                  result=r, round=first_round)
        )
        # convoluted
        if r == Match.RESULT_WHITE:
            r = Match.RESULT_BLACK
        elif r == Match.RESULT_BLACK:
            r = Match.RESULT_DRAW
        elif r == Match.RESULT_DRAW:
            r = Match.RESULT_WHITE

    for m in matches:
        m.save()
