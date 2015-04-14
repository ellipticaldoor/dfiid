from django.conf.urls import patterns, url
from content import views


urlpatterns = patterns(
	'',
	# web views
	url(r'^$', views.FrontView.as_view(), name='front'),
	url(r'^(?P<pk>[-\w]+)/(?P<slug>.*)/$',  views.PostView.as_view(), name='post_view'),
	url(r'^sub/(?P<sub>\S+)/$', views.PostBySubView.as_view(), name='sub_view'),

	# ajax views
	url(r'^ajax_content/', views.AjaxContentView.as_view()),
)