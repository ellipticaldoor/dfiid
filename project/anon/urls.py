from django.conf.urls import patterns, url

from anon import views


urlpatterns = patterns(
	'',
	url(r'^anon/$', views.AnonFrontView.as_view(), name='anon_front'),
	url(r'^anon/create/$', views.AnonCreatePostView.as_view(), name='create'),
)