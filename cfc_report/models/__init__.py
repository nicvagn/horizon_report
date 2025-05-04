from horizon_report import setup_logger
from .ctr import CTR
from .fields import CfcIdField, PairingSystemField, ProvinceField
from .match import Match
from .player import Player
from .roster import Roster
from .round import Round
from .tms import TMS
from .tournament import Tournament

# module level logger configuration
debug = True
file_handler = None
logger_name = __name__

# Initialize package logger
logger = setup_logger(debug, file_handler, logger_name)
