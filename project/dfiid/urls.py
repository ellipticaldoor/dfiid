from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from dfiid import sitemaps, feeds


sitemaps = {
	'site': sitemaps.SiteSitemap(['front', 'new', 'sub', 'anon_front',
								  'anon_new_front', 'create', 'blog']),
	'post': sitemaps.PostSitemap,
	'anon_post': sitemaps.AnonPostSitemap,
	'sub': sitemaps.SubSitemap,
	'user': sitemaps.UserSitemap,
}

urlpatterns = patterns('',)

if settings.DEBUG:
	import debug_toolbar
	urlpatterns += patterns('',
		url(r'^debug/', include(debug_toolbar.urls)),
	)

urlpatterns += patterns(
	'',
	url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps':sitemaps}),
	# url(r'^feed/$', feeds.ContentFeed(), name='feed'),
	url(r'^admin/', include(admin.site.urls)),

	url(r'^', include('content.urls')),
	url(r'^', include('anon.urls')),
	url(r'^', include('user.urls')),
)

handler404 = 'dfiid.views.handler404'

handler500 = 'dfiid.views.handler500'