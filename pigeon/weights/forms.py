from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from weights.models import PigeonUser


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
