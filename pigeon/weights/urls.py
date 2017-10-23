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
from django.conf.urls import include, url
import weights.views, weights.views.users, weights.views.measures, \
       weights.views.products

urlpatterns = [
    # Static pages
    url(r'^$', weights.views.home, name='home'),
    url(r'^about$', weights.views.about, name='about'),
    url(r'^privacy$', weights.views.privacy, name='privacy'),
    url(r'^contact$', weights.views.contact, name='contact'),
    url(r'^contribute$', weights.views.contribute, name='contribute'),
    # Users
    url(r'^account$', weights.views.users.user_account, name='user_account'),
    url(r'^delete_account$', weights.views.users.delete_account, name='delete_account'),
    url(r'^register/$', weights.views.users.register, name='register'),
    url(r'^profile/(?P<user>[0-9]+)/(?P<user_slug>[a-z0-9_-]+)$', weights.views.users.user_page,
        name='user_page'),
    # Measures
    url(r'^overview$', weights.views.measures.overview, name='overview'),
    url(r'^my_measures$', weights.views.measures.my_measures, name='my_measures'),
    url(r'^add_measure$', weights.views.measures.add_measure, name='add_measure'),
    url(r'^edit_measure/(?P<measure_id>[0-9]+)$', weights.views.measures.edit_measure,
        name='edit_measure'),
    url(r'^delete_measure/(?P<measure_id>[0-9]+)$', weights.views.measures.delete_measure,
        name='delete_measure'),
    url(r'^list_measures$', weights.views.measures.list_measures, name='list_measures'),
    url(r'^measure/(?P<measure_id>[0-9]+)$', weights.views.measures.measure_page,
        name='measure_page'),
    # Products
    url(r'^product/(?P<code>[0-9]+)$', weights.views.products.product_page,
        name='product_page'),
    url(r'^product/select-json$', weights.views.products.select_list,
        name='django_select2-json'),
    # Django stuff and 3rd party
    url('^', include('django.contrib.auth.urls')),
    url(r'^social/', include('social_django.urls', namespace='social')),
]
