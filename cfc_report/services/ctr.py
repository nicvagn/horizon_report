""" work with, and produce ctr cfc file """
# horizon_pair
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
# Copyright (C) 2024  Nicolas Vaagen
from typing import List

# make a ctr tournament report file
from cfc_report import logger
from cfc_report.models import Match, Player, Tournament


class CtrCreationException(Exception):
    """Something went wrong with ctr creation"""
    pass

class CTR:
    """CTR is a wrapper class for CTR (Tournament Report) File format"""

    def __init__(self, tournament_info, session):
        logger.info("class CTR init w -- tournament_info: %s, session: %s", tournament_info, session)
        self.player_ids = session.get_player_ids()
        self.num_players = len(self.player_ids)

        name = tournament_info["name"]
        num_rounds = int(tournament_info["num_rounds"])
        pairing_system = tournament_info["pairing_system"]
        td_cfc_id = tournament_info["td_cfc"]
        to_cfc_id = tournament_info["to_cfc"]
        province =  tournament_info["province"]
        date = (tournament_info["date_year"] + "-" + tournament_info["date_month"]
                + "-" + tournament_info["date_day"])


        # make sure the tournament has requisite data
        try:
            assert name is not None
            assert pairing_system is not None
            assert td_cfc_id is not None
            assert province is not None
            assert date is not None
            assert self.num_players > 0
        except AssertionError:
            print(f"make_ctr_report: missing tournament data in {name}")
            raise CtrCreationException("missing tournament data.")

        # get the pairing abbreviation
        if pairing_system == "Swiss":
            pairing_abriviation = "S"
        else:
            # Round Robin is default,
            # I think this works ie: I think there are only 2 options
            pairing_abriviation = "R"

        """List with one index per CTR line"""
        self.ctr: List[str] = []

        # start by building the 1st line of the ctr
        self.ctr.append(
            f'"{name}","{province}","0","{pairing_abriviation}","{date}","{self.num_players}","{td_cfc_id}","{to_cfc_id}"'
        )

        logger.info("ctr init. ctr: %s", self.ctr)

        # add all matches to report
        for rnd in range(num_rounds):
            # get matches in round
            matches =  Match.objects.filter(round_number=rnd)

            logger.info("building round: %s \nw: Matches: %s", rnd, matches)
            for match in matches:
                match_report = self.make_match_report(
                    match, match.white
                )
                match_report += self.make_match_report(
                    match, match.black
                )
                # append both players match reports to main report
                for line in match_report:
                    self.ctr.append(line)

    def write_file(self) -> None:
        """write the ctr report to file.
        side effect: creates file 'ctr_report.crt' in current directory.
                     If file already exists, it will be overwritten.
        """

        # make sure ctr data has been created
        try:
            assert self.ctr

        except AssertionError:
            print("make_ctr_report: asked to write ctr file but no ctr data")
            raise CtrCreationException(
                "missing ctr data when asked to write file"
            )

        # write the ctr report to file
        ctr_report = open("ctr_report.crt", "w")
        for line in self.ctr:
            ctr_report.write(line)
        ctr_report.close()

    def make_match_report(self, m: Match, player: Player) -> List[str]:
        """make a match part of ctr report file for a given player
        returns: a list of strings to be written to ctr_report one per line"""

        logger.info("make_match_report entered with match: %s, and player: %s", m, player)
        match_result = m.result
        if match_result == player.cfc_id:
            res = "W"
            points = "1.0"
        elif match_result is None:
            res = "D"
            points = "0.5"
        else:
            res = "L"
            points = "0.0"

        # match report
        match_report: List[str] = []

        # line 1
        match_report.append(f'"{player.cfc_id}"')

        # line 2
        match_report.append(f'"{res}","0"')

        # line 3
        match_report.append(f'"{points}"')

        return match_report

    def __str__(self) -> str:
        ctr = ""
        for line in self.ctr:
            ctr += line + "\n"
        return ctr

if __name__ == "__main__":
    # test
    T = {"name": "my test tornament",
         "num_rounds": 4,
         "pairing_system": "Swiss",
         "td_cfc": "111111",
         "to_cfc": "222222",
         "date_year": "1",
         "date_month": "1",
         "date_day": "1",}
    ctr = CTR(T)
