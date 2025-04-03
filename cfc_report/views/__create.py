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
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from cfc_report import logger
from cfc_report.forms import TournamentInfoForm
from cfc_report.models import (Match, Player, Round, Tournament)
from cfc_report.services import database as db
from cfc_report.services import session_services
from cfc_report.services.ctr_builder import CTR_builder


def initial(request):
    """Get initial tournament info
    Arguments
    ---------
    request : HttpRequest from the view
    """
    logger.debug("Report.initial entered with request: %s", request)
    # if is the form being submitted
    if request.method == "POST":
        # get the tournament info from the form submit
        tournament_info = request.POST
        logger.debug("POST request with value: %s", tournament_info)
        # save tournament info to session_services
        session_services.tournament.set_tournament_info(tournament_info)
        logger.debug("TournamentInfoForm made from POST: %s", tournament_info)
        # create tournament using info from the POST
        T = tournament(tournament_info)
        logger.debug("Tournament object made: %s", T)
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
    tournament_players = session_services.player.get_players()
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
        result = match_info["result"]
        if result == Match.RESULT_CHOICES[Match.RESULT_BLACK]:
            result = Match.RESULT_BLACK
        elif result == Match.RESULT_CHOICES[Match.RESULT_WHITE]:
            result = Match.RESULT_WHITE
        elif result == Match.RESULT_CHOICES[Match.RESULT_DRAW]:
            result = Match.RESULT_DRAW
        else:
            logger.error("Unknown Match Result: %s", result)
            result = Match.RESULT_UNKNOWN

        # get the cfc ids
        black_id = match_info["black"]
        white_id = match_info["white"]
        # get the players
        black = get_object_or_404(Player, cfc_id=black_id)
        white = get_object_or_404(Player, cfc_id=white_id)
        rnd = get_object_or_404(
            Round, round_num=session_services.tournament.get_tournament_round_number())
        # create the chess match model, and save it to the db
        chess_match = Match(white=white, black=black, result=result,
                            round=rnd)
        logger.debug(
            "chess_match entered: black_id %s, white_id: %s, result: %s,  \
            winner: %s",
            black_id,
            white_id,
            result,
        )
        chess_match.save()

    # Continue letting user add more games
    context = {
        "tournament_players": session_services.player.get_players(),
        "round_number": session_services.tournament.building_round_number(),
        "entered_matches": session_services.tournament.get_matches(),
    }

    return render(request, "cfc_report/create/match.html", context)


def round(request) -> HttpResponse:
    """Enter info for a round in a chess tournament, create the round model

    Arguments
    ---------
    request : HttpRequest
    """

    logger.debug("Create.round entered with request: %s", request)
    # round we are building
    cur_round = session_services.toournament.get_tournament_round_number()
    # create Round model in dadabase
    new_round = Round(round_num=cur_round, tournament=session_services.get_tournament())
    new_round.save()
    logger.debug("new round created. Round: %s", new_round)

    context = {
        "entered_matches": session_services.get_matches(),
        "round_number": cur_round,
        "rounds": session_services.get_rounds(),
    }
    return render(request, "cfc_report/create/round.html", context)


def confirm_round(request) -> HttpResponse:
    """Confirm a round for submission. If confirmed, finalize the round,
    else return to edditing it

    Arguments
    ---------
    request : HttpRequest
    """

    tournament_info = session_services.get_tournament_info()
    context = {
        "tournament_name": tournament_info["name"],
        "round_number": session_services.get_tournament_round_number(),
        # HACK: FIXME figgure out db sessions
        "matches": db.get_matches(),
        "players": db.get_players(),
    }
    logger.debug(
        "Create.confirm_round entered, confirming round completion.\n \
         TournamentInfo: %s \n context: %s \n",
        tournament_info,
        context,
    )

    return render(request, "cfc_report/create/confirm-round.html", context)


def tournament(t_info) -> Tournament:
    """Create a models.Tournament from t_info.

    Parameters
    ----------
    t_info : a POST request

    Returns
    -------
    A tournament model
    """

    # Make the tournament model for this tournament
    T = Tournament.objects.create(name=t_info["name"],
                                  num_rounds=t_info["num_rounds"],
                                  date=t_info["date"],
                                  province=t_info["province"], )

    logger.info("Tournament created: %s", T)
    return T


def report(request) -> HttpResponse:
    """Create report"""

    tournament_info = session_services.get_tournament_info()
    context = {
        "tournament_name": tournament_info["name"],
        "round_number": session_services.get_tournament_round_number(),
        "matches": session_services.get_matches(),
        "players": session_services.get_players(),
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
    session_services.finalize_round()

    # check if rounds are over. IE this is the last round
    if session_services.is_last_round():
        return redirect("create-report-preview")

    # start creation of next round
    return redirect("create-report-round")


def preview_report(request) -> HttpResponse:
    """Preview chess report, see all the players, rounds and games that will be
    in the report

    Arguments
    ---------
    request : HttpRequest
    """

    logger.debug("create.preview_report entered with request: %s", request)
    # get tournament information
    t_info = session_services.get_tournament_info()

    logger.debug("Tournament Info got: %s", t_info)
    ctr = CTR_builder(t_info, session_services)
    logger.debug("|CTR| created: %s", ctr)

    context = {
        "tournament_name": session_services.get_tournament_name(),
        "ctr": str(ctr),
        "tms": "TMS NOT DONE",
    }

    return render(request, "cfc_report/show/preview-report.html", context)


def finalize_report(request) -> HttpResponse:
    """Finalize a chess tournament report

    Arguments
    ---------
    request : HttpRequest
    """
    logger.debug("Create.finalize_report entered with request: %s", request)
    # get tournament information
    t_info = session_services.get_tournament_info()

    logger.debug("Tournament Info got: %s", t_info)
    ctr = CTR_builder(t_info, session_services)
    ctr.save()
    logger.debug("|CTR| created and saved: %s", ctr)

    ctr.write_file(t_info)
    context = {"ctr": str(ctr)}

    return render(request, "cfc_report/show/ctr.html", context)


def preview(request):
    """Preview the tournament report"""
    # get the tournament info set in Create.initial()
    tournament_info = session_services.tournament.get_tournament_info()

    # get information on tournament players from the session_services
    players: list[Player] = session_services.player.get_players()

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
    """Pick a player if it is not in the session_services, add it.
    If it is in the session_services, remove it. This uses htmx under the hood
    to replace on the DOM

    Side-effects
    ------------
    changes the CfcId's in session_services.

    Parameters
    ----------
    request : django request
        Django request
    cfc_id : "CfcId"
        The Player to add/removed to the session_services
    """

    logger.debug(
        "toggle_player_session entered with request: \
        %s and  player CfcId: %s",
        request,
        cfc_id,
    )
    assert cfc_id

    # if cfc id in session_services, remove it
    if cfc_id in session_services.player.get_player_ids():
        session_services.remove_player_by_id(cfc_id)
    else:
        # if not in session_services add to it
        session_services.player.add_player_by_id(cfc_id)

    db_players = db.get_players()
    tournament_players = session_services.player.get_players()

    context = {
        "players": db_players,
        "tournament_players": tournament_players,
        "include_nav_bar": False,
    }

    return render(request, "cfc_report/create/player-form.html", context)


def remove_match_session(request, pk=None) -> HttpResponse:
    """toggle a match from the db into the session_services and visa versa

    Side-effects
    ------------
    changes match pk's in session_services.

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
    # remove the match from the session_services by primary key
    session_services.match.remove_match_by_pk(pk)

    # return an empty http response, because why not
    return HttpResponse("")
