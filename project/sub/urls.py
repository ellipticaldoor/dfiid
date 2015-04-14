from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from sub import views


urlpatterns = patterns(
	'',
	url(r'^create_sub/$', login_required(views.CreateSubView.as_view()), name="create_sub"),
	url(r'^sub/$', views.SubView.as_view(), name="sub"),
	url(r'^sub/(?P<sub>\S+)/$', views.SubContentView.as_view(), name='sub_view'),
)