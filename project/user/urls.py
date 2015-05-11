from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from user import views, forms


urlpatterns = patterns(
	'',
	url(r'^signup/$', views.SignUpView.as_view(), name='register'),
	url(r'^login/$', 'django.contrib.auth.views.login',
		{'template_name':'user/login.html', 'authentication_form': forms.LoginForm}, name = "login"),
	url(r'^logout/$', 'django.contrib.auth.views.logout_then_login', name = "logout"),

	url(r'^user/(?P<profile>[-\w]+)/$', views.ProfileView.as_view(), name='profile'),
	url(r'^user/(?P<pk>[-\w]+)/edit/$', login_required(views.UserEdit.as_view()), name='profile_edit'),
	url(r'^user/(?P<profile>[-\w]+)/(?P<show>[-\w]+)/$', views.ProfileView.as_view(), name='profile_bio_commits'),
	url(r'^user/$', views.UserView.as_view(), name='user'),

	url(r'^user_follow/(?P<followed>[-\w]+)/$', login_required(views.UserFollowCreate.as_view()), name='follow'),
	url(r'^user_unfollow/(?P<unfollowed>[-\w]+)/$', login_required(views.UserFollowDelete.as_view()), name='unfollow'),
)