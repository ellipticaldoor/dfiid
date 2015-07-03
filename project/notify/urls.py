from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from notify import views

urlpatterns = patterns(
	'',
	url(r'^notify/$', views.Notify.as_view(), name='new', kwargs={'tab':'new'}),
    url(r'^notify/read/(?P<notyid>[-\w]+)/$', login_required(views.ReadNoty.as_view()), name='read_noty'),
	url(r'^notify/all$', views.Notify.as_view(), name='new', kwargs={'tab':'all'}),
)
