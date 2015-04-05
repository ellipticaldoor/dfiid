from django.conf.urls import patterns, url
from content import views, feed

urlpatterns = patterns(
	'',
	# Feed
	url(r'^feed/$', feed.ContentFeed(), name='feed'),

	# Archivo
	url(r'^search/$', views.ArchiveView.as_view(), name='search'),
	url(r'^user/(?P<pk>\S+)/$', views.UserView.as_view(), name='user_view'),
	url(r'^tag/(?P<tag>\S+)/$', views.PostTagView.as_view(), name='tag_view'),
	url(r'^(?P<year>\d{4})/(?P<month>\d{2})/$',  views.PostDateView.as_view(), name='date_view'),
	
	# Content
	url(r'^$', views.FrontView.as_view(), name='front'),
	url(r'^(?P<pk>[-\w]+)/(?P<slug>.*)/$',  views.PostView.as_view(), name='post_view'),
)