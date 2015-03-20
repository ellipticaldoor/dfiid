from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from cms import views


urlpatterns = patterns(
	'',
	# CMS
	url(r'^cms/$', login_required(views.PostListView.as_view()), name="cms_post_list"),
	url(r'^cms/tags/$', login_required(views.TagListView.as_view()), name="cms_tag_list"),

	# Editor
	url(r'^new_post/$', login_required(views.PostCreateView.as_view()), name="new_post"),
	url(r'^(?P<pk>[-\w]+)/(?P<slug>\S+)/edit/$', login_required(views.PostEditView.as_view()), name="post_edit"),
	url(r'^new_tag/$', login_required(views.TagCreateView.as_view()), name="new_post"),
)
