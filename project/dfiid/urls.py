from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin

from dfiid import sitemaps, feeds, views


sitemaps = {
	'site': sitemaps.SiteSitemap(['front', 'new', 'sub', 'create', 'blog']),
	'post': sitemaps.PostSitemap,
	'sub': sitemaps.SubSitemap,
	'user': sitemaps.UserSitemap,
}


urlpatterns = patterns('',)


if settings.DEBUG:
	import debug_toolbar
	from django.conf.urls.static import static

	urlpatterns += patterns('',
		url(r'^debug/', include(debug_toolbar.urls)),
	) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


urlpatterns += patterns(
	'',
	url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps':sitemaps}),
	# url(r'^feed/$', feeds.ContentFeed(), name='feed'),
	url(r'^admin/', include(admin.site.urls)),

	url(r'^about/', views.About.as_view()),
	url(r'^', include('notify.urls')),
	url(r'^', include('content.urls')),
	url(r'^', include('user.urls')),
)


handler404 = 'dfiid.views.handler404'


handler500 = 'dfiid.views.handler500'
