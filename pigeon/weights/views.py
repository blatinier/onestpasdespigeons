from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from weights.forms import UserForm, ProfileForm


def home(request):
    """
    Pretty home page.
    """
    return render(request, 'weights/home.html', {})


def about(request):
    """
    Everything about licensing/opensource/OpenFoodFacts...
    """
    # TODO #20
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
            return redirect('home')
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
    Page to add your own measurements.
    """
    # TODO
    return render(request, 'weights/my_measures.html', {})
