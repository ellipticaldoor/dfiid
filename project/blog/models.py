from time import time
from urllib.parse import quote
from django.db import models
from django.core.urlresolvers import reverse
from django.utils.text import slugify

from user.models import User
from core.core import _createId


class Tag(models.Model):
	slug = models.SlugField(max_length=100, primary_key=True)

	def __str__(self): return str(self.slug)


class PostQuerySet(models.QuerySet):
	def published(self):
		# TODO: Publicar solo entradas con pub_date menor a la fecha actual
		return self.filter(draft=False)

	def by_post(self, pk, slug):
		return self.filter(pk=pk, slug=slug, draft=False)

	def by_author(self, author):
		return self.filter(author=author, draft=False)

	def by_tag(self, tag):
		return self.filter(tag=tag, draft=False)

	def by_date(self, year, month):
		return self.filter(pub_date__year=year, pub_date__month=month, draft=False)


class Post(models.Model):
	post_id = models.CharField(primary_key=True, max_length=16, default=_createId)
	title = models.CharField(max_length=100)
	slug = models.CharField(max_length=100)
	body = models.TextField()
	draft = models.BooleanField(default=True)
	author = models.ForeignKey(User)
	pub_date = models.DateTimeField()
	tag = models.ForeignKey(Tag)

	objects = PostQuerySet.as_manager()

	def get_absolute_url(self):
		if not hasattr(self.post_id, 'decode'): post_id = self.post_id
		else: post_id = self.post_id.decode('utf-8')
		return '/%s/%s' % (post_id, str(self.slug))

	def get_edit_url(self):
		return str(self.get_absolute_url() + '/edit')

	def __str__(self): return str(self.title)

	def save(self, *args, **kwargs):
		self.slug = slugify(self.title.replace(' ', '_'))
		if not self.slug: self.slug = '_'
		super(Post, self).save(*args, **kwargs)

	class Meta:
		ordering = ['-pub_date']


class PostPhoto(models.Model):
	def get_post_image(instance, filename):
		# TODO: cambiar filename por photo_id
		return 's/media/img/blog/%s_%s' % (str(time()).replace('.', '_'), filename)

	photo_id = models.CharField(primary_key=True, max_length=16, default=_createId) 
	photo = models.FileField(upload_to=get_post_image)
	post = models.ForeignKey(Post, related_name='photo')

	def __str__(self): return str(self.photo)