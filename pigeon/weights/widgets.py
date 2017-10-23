# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from functools import reduce
from itertools import chain
from pickle import PicklingError

from django import forms
from django.conf import settings
from django.core import signing
from django.core.cache import caches
from django.db.models import Q
from django.forms.models import ModelChoiceIterator
from django.utils.encoding import force_text
from django.utils.six.moves.cPickle import PicklingError as cPicklingError
from django.utils.translation import get_language

try:
    from django.urls import reverse
except ImportError:
    from django.core.urlresolvers import reverse


class HeavySelect2Mixin:

    def __init__(self, attrs=None, choices=(), **kwargs):
        self.choices = choices
        if attrs is not None:
            self.attrs = attrs.copy()
        else:
            self.attrs = {}
        self.userGetValTextFuncName = kwargs.pop('userGetValTextFuncName', 'null')


class ModelSelect2Widget(HeavySelect2Mixin, forms.Select):
    model = None
    queryset = None
    search_fields = []
    max_results = 25

    def __init__(self, *args, **kwargs):
        """
        Overwrite class parameters if passed as keyword arguments.
        Args:
            model (django.db.models.Model): Model to select choices from.
            queryset (django.db.models.query.QuerySet): QuerySet to select choices from.
            search_fields (list): List of model lookup strings.
            max_results (int): Max. JsonResponse view page size.
        """
        self.model = kwargs.pop('model', self.model)
        self.queryset = kwargs.pop('queryset', self.queryset)
        self.search_fields = kwargs.pop('search_fields', self.search_fields)
        self.max_results = kwargs.pop('max_results', self.max_results)
        defaults = {'data_view': 'django_select2-json'}
        defaults.update(kwargs)
        super(ModelSelect2Widget, self).__init__(*args, **defaults)

    def build_attrs(self, *args, **kwargs):
        """Set select2's AJAX attributes."""
        attrs = super().build_attrs(*args, **kwargs)

        # encrypt instance Id
        self.widget_id = signing.dumps(id(self))

        attrs['data-field_id'] = self.widget_id
        attrs.setdefault('data-ajax--cache', "true")
        attrs.setdefault('data-ajax--type', "GET")
        attrs.setdefault('data-minimum-input-length', 2)
        attrs['class'] += ' django-select2-heavy'
        return attrs

    def filter_queryset(self, term, queryset=None):
        """
        Return QuerySet filtered by search_fields matching the passed term.
        Args:
            term (str): Search term
            queryset (django.db.models.query.QuerySet): QuerySet to select choices from.
        Returns:
            QuerySet: Filtered QuerySet
        """
        if queryset is None:
            queryset = self.get_queryset()
        search_fields = self.get_search_fields()
        select = Q()
        term = term.replace('\t', ' ')
        term = term.replace('\n', ' ')
        for t in [t for t in term.split(' ') if not t == '']:
            select &= reduce(lambda x, y: x | Q(**{y: t}), search_fields,
                             Q(**{search_fields[0]: t}))
        return queryset.filter(select)

    def get_queryset(self):
        """
        Return QuerySet based on :attr:`.queryset` or :attr:`.model`.
        Returns:
            QuerySet: QuerySet of available choices.
        """
        if self.queryset is not None:
            queryset = self.queryset
        elif self.model is not None:
            queryset = self.model._default_manager.all()
        else:
            raise NotImplementedError(
                "%(cls)s is missing a QuerySet. Define "
                "%(cls)s.model, %(cls)s.queryset, or override "
                "%(cls)s.get_queryset()." % {
                    'cls': self.__class__.__name__
                }
            )
        return queryset

    def get_search_fields(self):
        """Return list of lookup names."""
        if self.search_fields:
            return self.search_fields
        raise NotImplementedError('%s, must implement "search_fields".' % self.__class__.__name__)

    def optgroups(self, name, value, attrs=None):
        """Return only selected options and set QuerySet from `ModelChoicesIterator`."""
        default = (None, [], 0)
        groups = [default]
        has_selected = False
        selected_choices = {force_text(v) for v in value}
        if not self.is_required and not self.allow_multiple_selected:
            default[1].append(self.create_option(name, '', '', False, 0))
        if not isinstance(self.choices, ModelChoiceIterator):
            return super(ModelSelect2Widget, self).optgroups(name, value, attrs=attrs)
        selected_choices = {
            c for c in selected_choices
            if c not in self.choices.field.empty_values
        }
        choices = (
            (obj.pk, force_text(obj))
            for obj in self.choices.queryset.filter(pk__in=selected_choices)
        )
        for option_value, option_label in choices:
            selected = (
                force_text(option_value) in value and
                (has_selected is False or self.allow_multiple_selected)
            )
            if selected is True and has_selected is False:
                has_selected = True
            index = len(default[1])
            subgroup = default[1]
            subgroup.append(self.create_option(name, option_value, option_label, selected_choices, index))
        return groups

    def render_options(self, *args):
        """Render only selected options and set QuerySet from :class:`ModelChoiceIterator`."""
        try:
            selected_choices, = args
        except ValueError:
            choices, selected_choices = args
            choices = chain(self.choices, choices)
        else:
            choices = self.choices
        selected_choices = {force_text(v) for v in selected_choices}
        output = ['<option value=""></option>' if not self.is_required and not self.allow_multiple_selected else '']
        if isinstance(self.choices, ModelChoiceIterator):
            if self.queryset is None:
                self.queryset = self.choices.queryset
            selected_choices = {c for c in selected_choices
                                if c not in self.choices.field.empty_values}
            choices = [(obj.pk, force_text(obj))
                       for obj in self.choices.queryset.filter(pk__in=selected_choices)]
        else:
            choices = [(k, v) for k, v in choices if force_text(k) in selected_choices]
        for option_value, option_label in choices:
            output.append(self.render_option(selected_choices, option_value, option_label))
        return '\n'.join(output)
