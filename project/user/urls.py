from django.conf.urls import patterns, url

from user import views


urlpatterns = patterns(
	'',
	url(r'^register/$', views.RegistrationView.as_view(), name='register'),
	url(r'^login/$', 'django.contrib.auth.views.login', name = "login"),
	url(r'^logout/$', 'django.contrib.auth.views.logout_then_login', name = "logout"),
)