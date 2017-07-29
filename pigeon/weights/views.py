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
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404, reverse
from weights.forms import UserForm, ProfileForm, AddMeasureForm
from weights.models import Measure


def home(request):
    """
    Pretty home page.
    """
    return render(request, 'weights/home.html', {})


def about(request):
    """
    Everything about licensing/opensource/OpenFoodFacts...
    """
    return render(request, 'weights/about.html', {})


def register(request):
    """
    Register page.
    """
    if request.method == 'POST':
        user_form = UserForm(request.POST, prefix='user')
        profile_form = ProfileForm(request.POST, prefix='profile')
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.refresh_from_db()  # load the profile
            user.pigeonuser.language = profile_form.cleaned_data.get('language')
            user.pigeonuser.country = profile_form.cleaned_data.get('country')
            user.save()
            raw_password = user_form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect(reverse(my_measures))
    else:
        user_form = UserForm(prefix='user')
        profile_form = ProfileForm(prefix='profile')
    context = {'user_form': user_form, 'profile_form': profile_form}
    return render(request, 'registration/register.html', context)


@login_required
def list_measures(request):
    """
    List of all measures with all possible manipulation
    we can imagine.
    """
    # TODO #49
    return render(request, 'weights/list_measures.html', {})


def overview(request):
    """
    Some global statistics with nice graphs.
    """
    # TODO #19
    return render(request, 'weights/overview.html', {})


@login_required
def user_account(request):
    """
    Everything about user managing his account.
    """
    # TODO #1
    return render(request, 'weights/user_account.html', {})


def contribute(request):
    """
    Page to explain how to crontibute.
    (e.g issu github, add measures, add products, ideas, ...)
    """
    return render(request, 'weights/contribute.html', {})


@login_required
def my_measures(request):
    """
    Page to list your own measurements.
    """
    measures = Measure.objects.filter(user=request.user.pigeonuser)
    return render(request, 'weights/my_measures.html',
                  {'measures': measures})


@login_required
def add_measure(request):
    """
    Page to add your own measurements.
    """
    if request.method == 'POST':
        measure_inst = Measure(user=request.user.pigeonuser)
        add_measure_form = AddMeasureForm(request.POST, request.FILES,
                                          instance=measure_inst)
        if add_measure_form.is_valid():
            add_measure_form.save()
            # TODO flash message OK
            # https://docs.djangoproject.com/en/1.11/ref/contrib/messages/
            return redirect(reverse(my_measures))
            # TODO ticket add a btn to not redir, flash msg + add new measure
    add_measure_form = AddMeasureForm()
    return render(request, 'weights/add_measure.html',
                  {'add_measure_form': add_measure_form,
                   'btn_text': 'Add!'})


@login_required
def edit_measure(request, measure_id):
    """
    Page to edit your own measurements.
    """
    measure = get_object_or_404(Measure, pk=measure_id)
    if request.method == 'POST':
        if measure.user == request.user.pigeonuser:
            add_measure_form = AddMeasureForm(request.POST, request.FILES,
                                              instance=measure)
            if add_measure_form.is_valid():
                add_measure_form.save()
                # TODO flash message OK
                return redirect(reverse(my_measures))
        else:
            return HttpResponseForbidden()
    add_measure_form = AddMeasureForm(instance=measure)
    return render(request, 'weights/add_measure.html',
                  {'add_measure_form': add_measure_form,
                   'btn_text': 'Edit'})


@login_required
def delete_measure(request, measure_id):
    """
    Page to delete your own measurements.
    """
    # TODO #9, redirect doesn't take the deletion in account, refresh needed... concurrency problem?
    measure = get_object_or_404(Measure, pk=measure_id)
    if measure.user == request.user.pigeonuser:
        measure.delete()
    else:
        return HttpResponseForbidden()
    return redirect(reverse(my_measures))
