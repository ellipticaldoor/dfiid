from django.conf.urls import patterns, include, url
from django.contrib import admin
from withaliasing.sitemaps import SiteSitemap, BlogSitemap


sitemaps = {
	'site': SiteSitemap(['front', 'search', 'feed']),
	'blog': BlogSitemap
}

urlpatterns = patterns(
	'',
	url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps':sitemaps}),
	url(r'^admin/', include(admin.site.urls)),

	url(r'^', include('user.urls')),
	url(r'^', include('cms.urls')),
	url(r'^', include('blog.urls')),
)