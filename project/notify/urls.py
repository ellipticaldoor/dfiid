from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from notify import views

urlpatterns = patterns(
	'',
	url(r'^notify/$', views.Notify.as_view(), name='new', kwargs={'notify':'new'}),
    url(r'^notify/all$', views.Notify.as_view(), name='new', kwargs={'notify':'all'}),
)
