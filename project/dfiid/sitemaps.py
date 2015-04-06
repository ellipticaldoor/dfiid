from datetime import datetime

from django.contrib.sitemaps import Sitemap
from django.core.urlresolvers import reverse
from user.models import User
from content.models import Post, Sub


class SiteSitemap(Sitemap):

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


class ContentSitemap(Sitemap):
	changefreq = 'never'

	def items(self):
		return Post.objects.published()

	def lastmod(self, obj):
		return obj.pub_date

	def location(self, obj):
		return obj.get_absolute_url()


class SubSitemap(Sitemap):
	changefreq = 'never'

	def items(self):
		return Sub.objects.all()

	def location(self, obj):
		return obj.get_absolute_url()


class UserSitemap(Sitemap):
	changefreq = 'never'

	def items(self):
		return User.objects.all()

	def location(self, obj):
		return obj.get_absolute_url()