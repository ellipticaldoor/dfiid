from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from content import views


urlpatterns = patterns(
	'',
	url(r'^$', views.FrontView.as_view(), name='front'),
	url(r'^create/$', login_required(views.CreatePostView.as_view()), name="create"),
	url(r'^created/$', login_required(views.ListPostView.as_view()), name="created"),
	url(r'^(?P<pk>[-\w]+)/(?P<slug>\S+)/edit/$', login_required(views.EditPostView.as_view()), name="edit"),
	url(r'^(?P<pk>[-\w]+)/(?P<slug>.*)/$', views.PostView.as_view(), name='post_view'),
)