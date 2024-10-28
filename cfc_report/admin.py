"""cfc_report admin.py"""
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
from django.contrib import admin
from .models import (Player, Roster, TournamentDirector, TournamentOrganizer,
                     Match, )
# Register your models here.

admin.site.register(Player)
admin.site.register(Roster)
admin.site.register(TournamentDirector)
admin.site.register(TournamentOrganizer)
admin.site.register(Match)
