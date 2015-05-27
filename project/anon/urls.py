from django.conf.urls import patterns, url

from anon import views


urlpatterns = patterns(
	'',
	url(r'^anon/$', views.AnonFrontView.as_view(), name='anon_front', kwargs={'tab':'top'}),
	url(r'^anon/new$', views.AnonFrontView.as_view(), name='anon_new_front', kwargs={'tab':'new'}),
	url(r'^anon/create/$', views.AnonCreatePostView.as_view(), name='create'),
	url(r'^anon/(?P<pk>[-\w]+)/(?P<slug>.*)/$', views.AnonPostCommitView.as_view(), name='anon_post_view'),
)