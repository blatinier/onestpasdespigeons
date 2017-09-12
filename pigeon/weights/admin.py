# -*- coding: utf-8 -*-
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
from django.contrib import admin
from .models import Product, Measure

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from weights.models import PigeonUser


class PigeonUserInline(admin.StackedInline):
    model = PigeonUser
    can_delete = False
    verbose_name_plural = 'pigeonuser'


class UserAdmin(BaseUserAdmin):
    inlines = (PigeonUserInline, )

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# Register your models here.
admin.site.register(Product)
admin.site.register(Measure)
