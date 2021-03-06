from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from user import views, forms


urlpatterns = patterns(
	'',
	url(r'^signup/$', views.SignUpView.as_view(), name='register'),
	url(r'^login/$', 'django.contrib.auth.views.login',
		{'template_name':'user/login.html', 'authentication_form': forms.LoginForm}, name="login"),
	url(r'^logout/$', 'django.contrib.auth.views.logout_then_login', name="logout"),

	url(r'^blog/$', views.BlogView.as_view(), name='blog'),
	url(r'^follow/(?P<followed>[-\w]+)/$', login_required(views.UserFollowCreate.as_view()), name='follow'),
	url(r'^unfollow/(?P<unfollowed>[-\w]+)/$', login_required(views.UserFollowDelete.as_view()), name='unfollow'),

	url(r'^(?P<pk>[-\w]+)/edit/$', login_required(views.UserEdit.as_view()), name='profile_edit'),
	url(r'^(?P<profile>[-\w]+)/commit/$', views.ProfileCommitView.as_view(), name='profile_commit'),
	url(r'^(?P<profile>[-\w]+)/(?P<show>[-\w]+)/$', views.ProfileShowView.as_view(), name='profile_show'),
	url(r'^(?P<profile>[-\w]+)/$', views.ProfilePostView.as_view(), name='profile'),
)
