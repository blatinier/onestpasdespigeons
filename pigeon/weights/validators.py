# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#  Copyright (c) 2017 Benoit Latinier, Fabien Bourrel
#  This file is part of project: RendezMoiMesPlumes
#

from django.core.exceptions import ValidationError

def file_size(value):
    """ Validator for exceding file size """

    limit_mib = 5
    limit = limit_mib * 1024 * 1024
    if value.size > limit:
        raise ValidationError(_('File too large. Size should not exceed %d MiB.') % limit_mib)
