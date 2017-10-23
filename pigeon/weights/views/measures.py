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

import urllib.parse
from django import forms
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Max, Min, Avg, F
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.utils.translation import ugettext as _
from utils.images import set_measure_thumbnail
from weights.charts import ContribBarChart
from weights.models import Measure, MeasureFilter, Product
from weights.validators import file_size
from weights.widgets import ModelSelect2Widget

# TODO https://github.com/applegrew/django-select2/blob/master/django_select2/forms.py
class AddMeasureForm(forms.ModelForm):
    product = forms.ModelChoiceField(
            widget=ModelSelect2Widget(
                       model=Product,
                       search_fields=['product_name__icontains',
                                      'brands__icontains']
                   ),
            required=False,
            queryset=Product.objects.all(),
        )
    unit = forms.ChoiceField(choices=Measure.UNIT_CHOICES, initial='g')
    package_weight = forms.DecimalField(min_value=0, decimal_places=3)
    measured_weight = forms.DecimalField(min_value=0, decimal_places=3)
    measure_image = forms.ImageField(required=False, validators=[file_size])

    class Meta:
        model = Measure
        fields = ('product', 'package_weight', 'measured_weight',
                  'measure_image', 'unit')


class AddProductForm(forms.ModelForm):
    code = forms.CharField(required=False)
    product_name = forms.CharField(required=False)
    brands = forms.CharField(required=False)
    class Meta:
        model = Product
        fields = ('code', 'product_name', 'brands')

    def clean(self):
        cleaned_data = super().clean()
        code = cleaned_data.get("code")
        product_name = cleaned_data.get("product_name")
        brands = cleaned_data.get("brands")

        if not (code and product_name and brands):
            raise forms.ValidationError(_("All product fields must be set"),
                                        code='invalid')

#
# Views
#

@login_required
def list_measures(request):
    """
    List of all measures with all possible manipulation
    we can imagine.
    """
    valid_sorts = {'created_at': 'created_at',
                   'user': 'user__user__username',
                   'product': 'product__product_name',
                   'pweight': 'package_weight',
                   'mweight': 'measured_weight'}
    default_sort_key = 'created_at'
    default_sort = valid_sorts[default_sort_key]
    sort_q = request.GET.get('order_by', default_sort_key)
    sort = valid_sorts.get(sort_q, default_sort)
    if request.GET.get('sort_order') == 'desc':
        sort = '-{}'.format(sort)

    page = request.GET.get('page', 1)
    items_per_page = request.GET.get('items_per_page', 25)
    measures_list = MeasureFilter(request.GET, queryset=Measure.objects.all())
    paginator = Paginator(measures_list.qs.order_by(sort), items_per_page)
    try:
        measures = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        measures = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        measures = paginator.page(paginator.num_pages)
    get_args = request.GET.dict()
    if 'order_by' in get_args:
        del get_args['order_by']
    if 'sort_order' in get_args:
        del get_args['sort_order']
    get_args = urllib.parse.urlencode(get_args)
    return render(request, 'weights/all_measures.html',
                  {'measures': measures,
                   'filter': measures_list,
                   'order_by': sort_q,
                   'sort_order': request.GET.get('sort_order'),
                   'get_args': get_args})


def overview(request):
    """
    Some global statistics with nice graphs.
    """
    measure_count = Measure.objects.count()
    if not measure_count:
        stats = {'nb_products': Product.objects.count(),
                 'nb_measures': measure_count,
                 'abs_min_diff': "N/A",
                 'abs_max_diff': "N/A",
                 'abs_median_diff': "N/A",
                 'abs_mean_diff': "N/A",
                 'rel_min_diff': "N/A",
                 'rel_max_diff': "N/A",
                 'rel_median_diff': "N/A",
                 'rel_mean_diff': "N/A",
                 'top_products': [],
                 'flop_products': [],
                 'top_brands': [],
                 'flop_brands': [],
                 }
        return render(request, 'weights/overview.html', stats)
    abs_diff_measures = Measure.objects.annotate(
            mdiff=F('measured_weight') - F('package_weight'))
    abs_diff = abs_diff_measures.aggregate(min_diff=Min('mdiff'),
                                           max_diff=Max('mdiff'),
                                           avg_diff=Avg('mdiff'))
    abs_median_diff = abs_diff_measures.order_by('mdiff')\
            [int(measure_count / 2)]
    rel_diff_measures = Measure.objects.annotate(
            mdiff=(100 * (F('measured_weight') - F('package_weight')) /
                   F('package_weight')))
    rel_diff = rel_diff_measures.aggregate(min_diff=Min('mdiff'),
                                           max_diff=Max('mdiff'),
                                           avg_diff=Avg('mdiff'))
    rel_median_diff = rel_diff_measures.order_by('mdiff')\
            [int(measure_count / 2)]

    product_measures = Measure.objects.values('product').annotate(
            mdiff=(Avg(100 * (F('measured_weight') - F('package_weight')) /
                   F('package_weight'))))
    top_products = [{'product': Product.objects.get(code=d['product']),
                     'mdiff': d['mdiff']}
                    for d in product_measures.order_by('-mdiff')[:5]]

    flop_products = [{'product': Product.objects.get(code=d['product']),
                      'mdiff': d['mdiff']}
                     for d in product_measures.order_by('mdiff')[:5]]

    brands_measures = Measure.objects.values('product__brands').annotate(
            mdiff=(Avg(100 * (F('measured_weight') - F('package_weight')) /
                   F('package_weight'))))
    top_brands = [{'brand': d['product__brands'],
                   'mdiff': d['mdiff']}
                  for d in brands_measures.order_by('-mdiff')[:5]
                  if d['product__brands']]

    flop_brands = [{'brand': d['product__brands'],
                    'mdiff': d['mdiff']}
                   for d in brands_measures.order_by('mdiff')[:5]
                   if d['product__brands']]
    stats = {'nb_products': Product.objects.count(),
             'nb_measures': measure_count,
             'abs_min_diff': abs_diff['min_diff'],
             'abs_max_diff': abs_diff['max_diff'],
             'abs_median_diff': abs_median_diff.mdiff,
             'abs_mean_diff': abs_diff['avg_diff'],
             'rel_min_diff': round(float(rel_diff['min_diff']), 2),
             'rel_max_diff': round(float(rel_diff['max_diff']), 2),
             'rel_median_diff': round(float(rel_median_diff.mdiff), 2),
             'rel_mean_diff': round(float(rel_diff['avg_diff']), 2),
             'top_products': top_products,
             'flop_products': flop_products,
             'top_brands': top_brands,
             'flop_brands': flop_brands,
             }
    return render(request, 'weights/overview.html', stats)


@login_required
def my_measures(request):
    """
    Page to list your own measurements.
    """
    measures = Measure.objects.filter(user=request.user)
    return render(request, 'weights/my_measures.html',
                  {'measures': measures,
                   'measures_by_week': ContribBarChart()})


@login_required
def add_measure(request):
    """
    Page to add your own measurements.
    """
    page_mode_create = False
    redirect_page = reverse('my_measures')
    if request.method == 'POST':
        measure_inst = Measure(user=request.user)
        add_measure_form = AddMeasureForm(request.POST, request.FILES,
                                          instance=measure_inst)
        if "add_and_continue" in add_measure_form.data:
            redirect_page = reverse('add_measure')
        if add_measure_form.is_valid():
            add_product_form = AddProductForm(request.POST)
            if add_measure_form.cleaned_data['product']:
                measure = add_measure_form.save()
                set_measure_thumbnail(measure)
                messages.success(request, _("Measure added!"))
                return redirect(redirect_page)
            if add_product_form.is_valid():
                prod = add_product_form.save(commit=False)
                prod.source = 'Internal'
                prod.save()
                measure = add_measure_form.save(commit=False)
                measure.product = prod
                measure.save()
                set_measure_thumbnail(measure)
                prod.quantity = "%d g" % measure.weight('g', 'package')
                prod.save()
                messages.success(request, _("Measure added!"))
                return redirect(redirect_page)
            page_mode_create = (add_product_form.data.get('code') or
                                add_product_form.data.get('product_name') or
                                add_product_form.data.get('brands'))
            messages.error(request, _("Please select or create a product"
                                      "(all fields in create are required)."))
        else:
            messages.error(request, _("Error in the form."))
    else:
        add_measure_form = AddMeasureForm()
        add_product_form = AddProductForm()
    title = _('Add a measure')
    return render(request, 'weights/add_measure.html',
                  {'add_measure_form': add_measure_form,
                   'add_product_form': add_product_form,
                   'btn_text': _('Add!'),
                   'btn_continue_text': _('Add and keep adding!'),
                   'title': title,
                   'page_mode_create': page_mode_create})


@login_required
def edit_measure(request, measure_id):
    """
    Page to edit your own measurements.
    """
    measure = get_object_or_404(Measure, pk=measure_id)
    if measure.user != request.user:
        return HttpResponseForbidden()
    if request.method == 'POST':
        add_measure_form = AddMeasureForm(request.POST, request.FILES,
                                          instance=measure)
        if add_measure_form.is_valid():
            add_measure_form.save()
            messages.success(request, _("Measure edited!"))
            return redirect(reverse('my_measures'))
    add_measure_form = AddMeasureForm(instance=measure)
    title = _('Edit measure {measure_id}').format(measure_id=measure.id)
    return render(request, 'weights/add_measure.html',
                  {'add_measure_form': add_measure_form,
                   'btn_text': _('Edit'),
                   'title': title,
                   'edit_mode': True})


@login_required
def delete_measure(request, measure_id):
    """
    Page to delete your own measurements.
    """
    measure = get_object_or_404(Measure, pk=measure_id)
    if measure.user == request.user:
        measure.delete()
        messages.success(request, _("Measure deleted!"))
    else:
        return HttpResponseForbidden()
    return redirect(reverse('my_measures'))


@login_required
def measure_page(request, measure_id):
    """
    Measure page with all details
    """
    measure = get_object_or_404(Measure, pk=measure_id)
    return render(request, 'weights/measure.html',
                  {'measure': measure})
