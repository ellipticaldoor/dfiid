from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from user_profile import views


urlpatterns = patterns(
	'',
	url(r'^user/(?P<pk>[-\w]+)/$', views.ProfileView.as_view(), name='profile'),
	url(r'^users/$', views.UsersView.as_view(), name='users'),
)