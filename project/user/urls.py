from django.conf.urls import patterns, url

from user import views, forms


urlpatterns = patterns(
	'',
	url(r'^signup/$', views.SignUpView.as_view(), name='register'),
	url(r'^login/$', 'django.contrib.auth.views.login',
		{'template_name':'user/login.html', 'authentication_form': forms.LoginForm},
		name = "login"),
	url(r'^logout/$', 'django.contrib.auth.views.logout_then_login', name = "logout"),
)