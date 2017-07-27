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
#  Copyright © 2017 Benoît Latinier, Fabien Bourrel
#  This file is part of project: OnEstPasDesPigeons
#
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django_select2.forms import ModelSelect2Widget
from weights.models import PigeonUser, Product, Measure


LANGUAGE_CHOICES = (('en', 'en'), ('fr', 'fr'))
COUNTRY_CHOICES = (('us', 'us'), ('fr', 'fr'))


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1',
                  'password2')


class ProfileForm(forms.ModelForm):
    language = forms.ChoiceField(choices=LANGUAGE_CHOICES)
    country = forms.ChoiceField(choices=COUNTRY_CHOICES)

    class Meta:
        model = PigeonUser
        fields = ('language', 'country')



class ProductSelect2Widget(ModelSelect2Widget):
    search_fields = [
            'product_name__icontains',
            'generic_name__icontains',
        ]


class AddMeasureForm(forms.ModelForm):
    product = forms.ChoiceField(widget=ModelSelect2Widget(
            model=Product,
            search_fields=['product_name__icontains',
                           'generic_name__icontains'],
            queryset=Product.objects.all(),
        ))
    package_weight = forms.DecimalField(min_value=0, decimal_places=3)
    measured_weight = forms.DecimalField(min_value=0, decimal_places=3)
    measure_image = forms.ImageField()
    class Meta:
        model = Measure
        fields = ('product', 'package_weight', 'measured_weight',
                  'measure_image')
