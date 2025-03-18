"""a CFC models"""
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
from cfc_report import logger
from cfc_report.fields import CfcIdField
from django.db import models
from django.utils.text import slugify


class CfcId(models.Model):
    """A CFC ID number, a six char number

    Attributes
    ----------
    number : a cfc id number in range 100000 - 999999
    """

    number = CfcIdField()
    slug = models.SlugField(default="", unique=True, null=False)

    def save(self, *args, **kwargs):
        """create slug url before saving
        Override of save()

        Arguments
        ---------
        *args and **kwargs - passed on to super().save(...)

        Returns
        -------
        None
        """

        self.slug = slugify(self.number)
        logger.info(
            "PersonWithCfdId: (%s) saved and slug (%s) created for it",
            self,
            self.slug
        )
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.number)
