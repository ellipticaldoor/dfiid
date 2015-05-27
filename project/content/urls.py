from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from content import views


urlpatterns = patterns(
	'',
	url(r'^$', views.FrontView.as_view(), name='front', kwargs={'tab':'top'}),
	url(r'^new/$', views.FrontView.as_view(), name='new', kwargs={'tab':'new'}),

	url(r'^sub/$', views.SubView.as_view(), name='sub'),
	url(r'^sub/(?P<sub>\S+)/$', views.SubPostListView.as_view(), name='sub_view'),
	url(r'^sub/(?P<sub>\S+)/(?P<followers>\S+)$', views.SubPostListView.as_view(), name='sub_followers'),
	url(r'^create_sub/$', login_required(views.CreateSubView.as_view()), name='create_sub'),
	
	url(r'^create/$', login_required(views.CreatePostView.as_view()), name='create'),
	url(r'^created/$', login_required(views.PostUserCreatedView.as_view()), name='created'),
	
	url(r'^sub_follow/(?P<followed>[-\w]+)/$', login_required(views.SubFollowCreate.as_view()), name='sub_follow'),
	url(r'^sub_unfollow/(?P<unfollowed>[-\w]+)/$', login_required(views.SubFollowDelete.as_view()), name='sub_unfollow'),

	url(r'^post/(?P<pk>[-\w]+)/(?P<slug>\S+)/edit/$', login_required(views.UpdatePostView.as_view()), name='edit'),
	url(r'^post/(?P<pk>[-\w]+)/(?P<slug>.*)/$', views.PostCommitView.as_view(), name='post_view'),
)