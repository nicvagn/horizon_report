""" set up logger for package """
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
import logging
from .constants import DEBUG, FILE_HANDLER, LOGGER_NAME
from .services.log import set_up_logger
# settings
DEBUG = True
FILE_HANDLER = True
LOGGER_NAME = "CFC_REPORT"

set_up_logger(logger_name=LOGGER_NAME,
              debug=DEBUG, file_handler=FILE_HANDLER)
