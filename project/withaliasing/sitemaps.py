from datetime import datetime

from django.contrib.sitemaps import Sitemap
from django.core.urlresolvers import reverse
from user.models import User
from blog.models import Post, Tag
from core.core import archivize


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
	priority = 0.9

	def items(self):
		return Post.objects.published()

	def lastmod(self, obj):
		return obj.pub_date

	def location(self, obj):
		return obj.get_absolute_url()


class TagSitemap(Sitemap):
	changefreq = 'never'
	priority = 0.8

	def items(self):
		return Tag.objects.all()

	def location(self, obj):
		return obj.get_absolute_url()


class UserSitemap(Sitemap):
	changefreq = 'never'
	priority = 0.7

	def items(self):
		return User.objects.all()

	def location(self, obj):
		return obj.profile.get_absolute_url()