from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from dfiid import sitemaps, feeds


sitemaps = {
	'site': sitemaps.SiteSitemap(['front', 'search', 'feed']),
	'content': sitemaps.ContentSitemap,
	'sub': sitemaps.SubSitemap,
	'user': sitemaps.UserSitemap,
}


urlpatterns = patterns(
	'',
	url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps':sitemaps}),
	url(r'^feed/$', feeds.ContentFeed(), name='feed'),
	url(r'^admin/', include(admin.site.urls)),

	url(r'^', include('user.urls')),
	url(r'^', include('user_profile.urls')),
	url(r'^', include('cms.urls')),
	url(r'^', include('sub.urls')),
	url(r'^', include('content.urls')),
)

if settings.DEBUG:
	import debug_toolbar
	urlpatterns += patterns('',
		url(r'^', include(debug_toolbar.urls)),
	)