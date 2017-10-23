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

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, F, Q
from django.shortcuts import render, get_object_or_404
from weights.models import Measure, Product


@login_required
def product_page(request, code):
    """
    Product page with measures
    """
    items_per_page = request.GET.get('items_per_page', 25)
    page = request.GET.get('page', 1)
    product = get_object_or_404(Product, pk=code)
    measures = Measure.objects.filter(product=product).order_by("-created_at")
    nb_measures = measures.count()
    paginator = Paginator(measures, items_per_page)
    rel_diff_measures = Measure.objects.filter(product=product).annotate(
            mdiff=((F('measured_weight') - F('package_weight')) /
                   F('package_weight') * 100))
    rel_diff = rel_diff_measures.aggregate(avg_diff=Avg('mdiff'))

    try:
        measures = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        measures = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        measures = paginator.page(paginator.num_pages)
    return render(request, 'weights/product.html',
                  {'product': product,
                   'measures': measures,
                   'nb_measures': nb_measures,
                   'rel_mean_diff': round(float(rel_diff['avg_diff']), 2)})


def select_list(request):
    term = request.GET.get('term', '')
    products = Product.objects.filter(Q(product_name__icontains=term) |
                                      Q(brands__icontains=term))[0:25]
    return render(request, 'weights/product_select.json',
                  {'products': products})
