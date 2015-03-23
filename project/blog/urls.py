from django.conf.urls import patterns, url
from blog import views, feed

urlpatterns = patterns(
	'',
	# Feed
	url(r'^feed/$', feed.BlogFeed(), name="feed"),

	# Archivo
	url(r'^all/$', views.ArchiveView.as_view(), name="all"),
	url(r'^author/(?P<author>\S+)/$', views.PostAuthorView.as_view(), name="author_view"),
	url(r'^tag/(?P<tag>\S+)/$', views.PostTagView.as_view(), name="tag_view"),
	url(r'^(?P<year>\d{4})/(?P<month>\d{2})/$',  views.PostDateView.as_view(), name="date_view"),
	
	# Blog
	url(r'^$', views.FrontView.as_view(), name="front"),
	url(r'^(?P<pk>[-\w]+)/(?P<slug>.*)/$',  views.PostView.as_view(), name="post_view"),
)