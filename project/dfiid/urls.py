from django.conf.urls import patterns, include, url
from django.contrib import admin
from dfiid import sitemaps


sitemaps = {
	'site': sitemaps.SiteSitemap(['front', 'search', 'feed']),
	'content': sitemaps.ContentSitemap,
	'tag': sitemaps.TagSitemap,
	'user': sitemaps.UserSitemap,
}

urlpatterns = patterns(
	'',
	url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps':sitemaps}),
	url(r'^admin/', include(admin.site.urls)),

	url(r'^', include('user.urls')),
	url(r'^', include('cms.urls')),
	url(r'^', include('content.urls')),
)