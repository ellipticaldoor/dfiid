from datetime import datetime

from django.contrib.sitemaps import Sitemap
from django.core.urlresolvers import reverse
from blog.models import Post


class SiteSitemap(Sitemap):
	priority = 1

	def __init__(self, names):
		self.names = names

	def items(self):
		return self.names

	def changefreq(self, obj):
		return 'daily'

	def lastmod(self, obj):
		return datetime.now()

	def location(self, obj):
		return reverse(obj)


class BlogSitemap(Sitemap):
	changefreq = 'never'
	priority = 0.5

	def items(self):
		return Post.objects.published()

	def lastmod(self, obj):
		return obj.pub_date

	def location(self, obj):
		return '/'