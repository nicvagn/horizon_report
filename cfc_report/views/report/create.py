"""view for creating a cfc report"""
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
from cfc_report import logger, models
from cfc_report.forms import MatchForm, RoundForm, TournamentInfoForm
from cfc_report.models import Match, Player
from cfc_report.services import database as db
from cfc_report.services import session
from cfc_report.services.ctr import CTR
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.vary import vary_on_headers


def initial(request):
    """Get initial tournament info
    Arguments
    ---------
    request : HttpRequest from the view
    """
    logger.debug("Report.initial entered with request: %s", request)
    # if is the form being submitted
    if request.method == "POST":
        tournament_info = request.POST
        logger.debug("POST request with value: %s", tournament_info)
        # save tournament info to session
        session.set_tournament_info(tournament_info)
        logger.debug("TournamentInfoForm made from POST: %s", tournament_info)

        # redirect to view to choose players
        return redirect("create-report-players")

    form = TournamentInfoForm()

    context = {
        "title": "Enter tournament information",
        "action_url": reverse("create-report-info"),
        "submit_btn_txt": "Pick Players",
        "form": form,
    }
    return render(request, "cfc_report/base/base-form.html", context)


def players(request):
    """set information about what players in a tournament"""

    db_players = db.get_players()
    tournament_players = session.get_players()
    context = {
        "title": "choose tournament players",
        "action_url": reverse("create-report-players"),
        "players": db_players,
        "tournament_players": tournament_players,
        "include_nav_bar": False,
    }

    # if the request is a POST it is the form submission not initial get
    # needed if no new players are choosen and you want to confirm players
    if request.method == "POST":
        player_info = request.POST
        logger.debug("POST request with value: %s", player_info)
        logger.debug("TournamentInfoForm made from POST: %s", player_info)
        return render(request, "cfc_report/create/round.html", player_info)

    logger.debug(
        "db_players: %s \n tournament_players: %s \n context: %s",
        db_players,
        tournament_players,
        context,
    )
    return render(request, "cfc_report/create/toggle-players.html", context)


def chess_match(request):
    """Enter information about a chess match
    Arguments
    ---------
    request : HttpRequest
        if POST a request containing a chess match
    """

    # The form for creating matches is in match.html
    logger.debug("Create.match entered with request: %s", request)
    # if is the form being submitted
    if request.method == "POST":
        match_info = request.POST
        logger.debug("POST request with value: %s", match_info)

        black_id = match_info["black"]
        white_id = match_info["white"]
        result = match_info["result"]

        # RESULT_CHOICES = [("b", "0 - 1"), ("w", "1 - 0"), ("d", "0.5 - 0.5"), ("_", "_")]
        # set the winning player_id from the result
        if result == Match.RESULT_CHOICES[0][1]:
           winner = white_id
        elif result == Match.RESULT_CHOICES[1][1]:
            winner = black_id
        # we are assuming match is done, :. draw
        else:
            winner = Match.RESULT_CHOICES[2][1]
        # create the chess match model, and save it to the db
        chess_match = session.create_match(white_id, black_id, winner)
        logger.debug(
            "chess_match entered: black_id %s, white_id: %s, result: %s, winner: %s",
            black_id,
            white_id,
            result,
            winner,
        )
        chess_match.save()

    # Continue letting user add more games
    context = {
        "tournament_players": session.get_players(),
        "round_number": session.get_tournament_round_number(),
        "entered_matches": session.get_matches(),
    }

    return render(request, "cfc_report/create/match.html", context)


def round(request) -> HttpResponse:
    """Enter info for a round in a chess tournament

    Arguments
    ---------
    request : HttpRequest
    """
    logger.debug("Create.round entered with request: %s", request)
    # if is the form being submitted
    if request.method == "POST":
        round_info = request.POST
        logger.debug("POST request with value: %s", round_info)
        # TODO
        # Continue letting user add more games
        return render(request, "cfc_report/create/round.html", {})

    context = {"entered_matches": session.get_matches(),
               "round_number": session.get_tournament_round_number(),
               "rounds": session.get_rounds()}
    return render(request, "cfc_report/create/round.html", context)


def confirm_round(request) -> HttpResponse:
    """Confirm a round for submission. If confirmed, finalize the round,
    else return to edditing it

    Arguments
    ---------
    request : HttpRequest
    """

    tournament_info = session.get_tournament_info()
    context = {
        "tournament_name": tournament_info["name"],
        "round_number": session.get_tournament_round_number(),
        "matches": session.get_matches(),
        "players": session.get_players(),
    }
    logger.debug("Create.confirm_round entered, confirming round completion. TournamentInfo: %s", tournament_info)

    return render(request, "cfc_report/create/confirm-round.html", context)


def report(request) -> HttpResponse:
    """Create report"""

    tournament_info = session.get_tournament_info()
    context = {
        "tournament_name": tournament_info["name"],
        "round_number": session.get_tournament_round_number(),
        "matches": session.get_matches(),
        "players": session.get_players(),
    }
    return render(request, "cfc_report/create/report.html", context)


def finalize_round(request) -> HttpResponse:
    """finalize a round in a chess tournament

    Arguments
    ---------
    request : HttpRequest
    """
    logger.debug("Create.finalize_round entered with request: %s", request)
    # finalize the round, and prep for new one
    session.finalize_round()

    # start creation of next round
    return redirect("create-report-round")

def finalize_report(request) -> HttpResponse:
    """finalize a chess tournament report

    Arguments
    ---------
    request : HttpRequest
    """
    logger.debug("Create.finalize_report entered with request: %s", request)
    # get tournament information
    t_info = session.get_tournament_info()

    logger.debug("Tournament Info got: %s", t_info)
    ctr = CTR(t_info, session)
    logger.debug("|CTR| created: %s", ctr)
    context = {
        "ctr": str(ctr)
    }

    return render(request, "cfc_report/show/ctr.html", context)


def preview(request):
    """Preview the tournament report"""
    # get the tournament info set in Create.initial()
    tournament_info = session.get_tournament_info()

    # get information on tournament players from the session
    players: list[Player] = session.get_players()

    context = {
        "name": tournament_info["name"],
        "province": tournament_info["province"],
        "time_format": "blitz",
        "num_players": len(players),
        "players": players,
        "td_cfc": tournament_info["td_cfc"],
        "to_cfc": tournament_info["to_cfc"],
    }
    logger.debug("context: %s", context)
    return render(request, "cfc_report/show/index.html", context)


def toggle_player_session(request, cfc_id=None):
    """Pick a player if it is not in the session, add it.
    If it is in the session, remove it. This uses htmx under the hood
    to replace on the DOM

    Side-effects
    ------------
    changes the CfcId's in session.

    Parameters
    ----------
    request : django request
        Django request
    cfc_id : "CfcId"
        The Player to add/removed to the session
    """

    logger.debug(
        "toggle_player_session entered with request: \
        %s and  player CfcId: %s",
        request,
        cfc_id,
    )
    assert cfc_id

    # if cfc id in session, remove it
    if cfc_id in session.get_player_ids():
        session.remove_player_by_id(cfc_id)
    else:
        # if not in session add to it
        session.add_player_by_id(cfc_id)

    db_players = db.get_players()
    tournament_players = session.get_players()

    context = {
        "players": db_players,
        "tournament_players": tournament_players,
        "include_nav_bar": False,
    }

    return render(request, "cfc_report/create/player-form.html", context)


def remove_match_session(request, pk=None) -> HttpResponse:
    """toggle a match from the db into the session and visa versa

    Side-effects
    ------------
    changes match pk's in session.

    Parameters
    ----------
    request : HttpRequest
        request sent to tell us to del match
    pk=None
        The primary key of the match to delete
    """
    assert pk
    logger.debug(
        "toggle_match_session entered with request: \
        %s and  match pk: %s",
        request,
        pk,
    )
    # remove the match from the session by primary key
    session.remove_match_by_pk(pk)

    # return an empty http response, because why not
    return HttpResponse("")
