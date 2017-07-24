from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^overview$', views.overview, name='overview'),
    url(r'^about$', views.about, name='about'),
    url(r'^account$', views.user_account, name='user_account'),
    url(r'^contribute$', views.contribute, name='contribute'),
    url(r'^my_measures$', views.my_measures, name='my_measures'),
    url(r'^list_measures$', views.list_measures, name='list_measures'),

    url(r'^register/$', views.register, name='register'),
    url('^', include('django.contrib.auth.urls')),
]
