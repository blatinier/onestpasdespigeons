from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect


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
    # TODO #1
    return render(request, 'registration/register.html', {})


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
    # TODO #48
    return render(request, 'weights/contribute.html', {})


@login_required
def my_measures(request):
    """
    Page to add your own measurements.
    """
    # TODO
    return render(request, 'weights/my_measures.html', {})
