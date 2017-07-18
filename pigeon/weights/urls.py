from django.conf.urls import include, url
from django.contrib.auth import views as auth_views
from . import views

# TODO auth views https://docs.djangoproject.com/en/1.11/topics/auth/default/#using-the-views
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
    #url(r'^password_change/$', auth_views.PasswordChangeView.as_view()),
    #url(r'^password_change/done/$', auth_views.PasswordChangeDoneView.as_view()),
    #url(r'^password_reset/$', auth_views.PasswordResetView.as_view()),
    #url(r'^password_reset/done/$', auth_views.PasswordResetDoneView.as_view()),
    #url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-),+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', auth_views.PasswordResetConfirmView.as_view()),
    #url(r'^reset/done/$', auth_views.PasswordResetCompleteView.as_view()),

    #url(r'^password_reset$', views.password_reset, name='password_reset'),
]
