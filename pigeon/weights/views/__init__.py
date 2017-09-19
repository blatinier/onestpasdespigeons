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
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.utils.translation import ugettext as _
from weights.models import Measure
from django import forms


def home(request):
    """
    Pretty home page.
    """
    last_measures = Measure.objects.all().order_by('-created_at')[:6]
    return render(request, 'weights/home.html',
                  {'last_measures': last_measures})


def privacy(request):
    """
    User privacy
    """
    return render(request, 'weights/privacy.html', {})


def about(request):
    """
    Everything about licensing/opensource/OpenFoodFacts...
    """
    return render(request, 'weights/about.html', {})



def contribute(request):
    """
    Page to explain how to crontibute.
    (e.g issu github, add measures, add products, ideas, ...)
    """
    return render(request, 'weights/contribute.html', {})


class ContactForm(forms.Form):
    name = forms.CharField(required=True)
    email = forms.CharField(required=True)
    subject = forms.CharField(required=True)
    content = forms.CharField(required=True, widget=forms.Textarea)


def contact(request):
    """
    Contact form
    """
    success = False
    if request.method == 'POST':
        contact_form = ContactForm(request.POST)
        if contact_form.is_valid():
            send_mail(
                "[pigeon] %s" % contact_form.cleaned_data['subject'],
                """From: %s %s

%s""" % (contact_form.cleaned_data['name'],
         contact_form.cleaned_data['email'],
         contact_form.cleaned_data['content']),
                contact_form.cleaned_data['email'],
                settings.ADMINS,
            )
            success = True
            messages.success(request, _("Email sent!"))
        else:
            messages.error(request, _("All fields are required!"))
    else:
        contact_form = ContactForm()
    return render(request, 'weights/contact.html',
                  {'form': contact_form,
                   'success': success})

