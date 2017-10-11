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

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import (login, logout,
                                 update_session_auth_hash)
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.utils.translation import ugettext as _
from weights.models import PigeonUser, Measure
from django import forms
from django.contrib.auth.forms import UserCreationForm
from weights.validators import file_size
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from weights.charts import ContribBarChart


#
# Forms
#

class ProfileForm(forms.ModelForm):
    COUNTRY_CHOICES = (('us', 'us'), ('fr', 'fr'))

    nickname = forms.CharField(required=False)
    avatar = forms.ImageField(required=False, validators=[file_size])
    language = forms.ChoiceField(choices=settings.LANGUAGES)
    country = forms.ChoiceField(choices=COUNTRY_CHOICES)

    class Meta:
        model = PigeonUser
        fields = ('nickname', 'language', 'country', 'avatar')


class RegisterForm(UserCreationForm):
    class Meta:
        model = PigeonUser
        fields = ('username', 'first_name', 'last_name', 'email', 'password1',
                  'password2') + ProfileForm.Meta.fields

class UpdateUserForm(forms.ModelForm):

    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
    }
    password1 = forms.CharField(label=_("Password"), required=False,
        widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Password confirmation"),
        required=False,
        widget=forms.PasswordInput,
        help_text=_("Enter the same password as above, for verification."))

    class Meta:
        model = PigeonUser
        fields = ('username', 'first_name', 'last_name', 'email', 'password1',
                  'password2')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if (password1 or password2) and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def save(self, commit=True):
        user = super(UpdateUserForm, self).save(commit=False)
        raw_password = self.cleaned_data['password1']
        if raw_password:
            user.set_password(raw_password)
        if commit:
            user.save()
        return user

#
# Views
#

def register(request):
    """
    Register page.
    """
    if request.user.is_authenticated:
        messages.error(request, _("You already have an account."))
        return redirect(reverse('my_measures'))
    if request.method == 'POST':
        register_form = RegisterForm(request.POST, prefix='user')
        if register_form.is_valid():
            user = register_form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect(reverse('my_measures'))
    else:
        register_form = RegisterForm(prefix='user')
    context = {'register_form': register_form}
    return render(request, 'registration/register.html', context)

@login_required
def user_account(request):
    """
    Everything about user managing his account.
    """
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, prefix='user',
                                   instance=request.user)
        profile_form = ProfileForm(request.POST,
                                   request.FILES,
                                   prefix='profile',
                                   instance=request.user)
        context = {'user_form': user_form,
                   'profile_form': profile_form,
                   'update_text': _('Update'),
                   'user': request.user}
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.language = \
                    profile_form.cleaned_data.get('language')
            user.country = profile_form.cleaned_data.get('country')
            user.save()
            # Update password
            if user_form.cleaned_data.get('password1'):
                update_session_auth_hash(request, user)
            context['message'] = {'status': 'success',
                                  'text': _("Update successful!")}
        return render(request, 'weights/user_account.html', context)
    else:
        user_form = UpdateUserForm(prefix='user', instance=request.user)
        profile_form = ProfileForm(prefix='profile',
                                   instance=request.user)
    context = {'user_form': user_form,
               'profile_form': profile_form,
               'update_text': _('Update'),
               'user': request.user}
    return render(request, 'weights/user_account.html', context)


@login_required
def delete_account(request):
    """
    Delete user account.
    In fact just inactivate it.
    """
    user = request.user
    user.is_active = False
    user.save()
    logout(request)
    messages.info(request, _("Account deactivated."))
    return redirect(reverse('home'))

@login_required
def user_page(request, user, user_slug):
    """
    Public profile page of users
    """
    items_per_page = request.GET.get('items_per_page', 25)
    page = request.GET.get('page', 1)
    user = get_object_or_404(PigeonUser, pk=user)
    measures = Measure.objects.filter(user=user).order_by("-created_at")
    paginator = Paginator(measures, items_per_page)
    try:
        measures = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        measures = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        measures = paginator.page(paginator.num_pages)
    return render(request, 'weights/profile.html',
                  {'viewed_user': user,
                   'measures': measures,
                   'nb_measures': measures.count('user'),
                   'measures_by_week': ContribBarChart()})


