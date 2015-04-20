from time import time
from markdown import markdown

from django.conf import settings
from django.db import models
from django.utils.text import slugify

from user.models import User
from core.core import _createId


class Sub(models.Model):
	slug = models.SlugField(primary_key=True, max_length=100)
	created = models.DateTimeField(auto_now_add=True)

	def get_absolute_url(self):
		return '/sub/%s' % (str(self.slug))

	def __str__(self):
		return str(self.slug)


class PostQuerySet(models.QuerySet):
	def published(self):
		return self.filter(draft=False)

	def by_sub(self, sub):
		return self.filter(sub=sub, draft=False)

	def by_user(self, user):
		return self.filter(user=user)

	def by_post(self, pk, slug):
		return self.filter(pk=pk, slug=slug)


class Post(models.Model):
	post_id = models.CharField(primary_key=True, max_length=16, default=_createId)
	user = models.ForeignKey(User, related_name="posts")
	sub = models.ForeignKey(Sub, related_name="posts")
	title = models.CharField(max_length=100)
	slug = models.CharField(max_length=100)
	body = models.TextField(max_length=3000, default='', blank=True)
	body_html  = models.TextField(blank=True, null=True)
	draft = models.BooleanField(default=False)
	created = models.DateTimeField(auto_now_add=True)
	last_commented = models.DateTimeField(auto_now_add=True)
	comment_number = models.IntegerField(default=0)
	show = models.BooleanField(default=True)

	objects = PostQuerySet.as_manager()

	def save(self, *args, **kwargs):
		self.slug = slugify(self.title.replace(' ', '_'))
		if not self.slug: self.slug = '_'
		self.body_html = markdown(self.body, safe_mode=True)
		super(Post, self).save(*args, **kwargs)

	def get_absolute_url(self):
		if not hasattr(self.post_id, 'decode'): post_id = self.post_id
		else: post_id = self.post_id.decode('utf-8')
		return '/%s/%s/' % (post_id, self.slug)

	def get_edit_url(self):
		return '%sedit/' % (self.get_absolute_url())
	def get_comment_url(self):
		return '%scomment/' % (self.get_absolute_url())

	def __str__(self): return self.title

	class Meta: ordering = ['-last_commented']


class Comment(models.Model):
	comment_id = models.CharField(primary_key=True, max_length=16, default=_createId) 
	user = models.ForeignKey(User, related_name="comments")
	post = models.ForeignKey(Post, related_name="comments")
	body = models.TextField(max_length=500, default='')
	body_html  = models.TextField(blank=True, null=True)
	created = models.DateTimeField(auto_now_add=True)

	def save(self, *args, **kwargs):
		self.body_html = markdown(self.body, safe_mode=True)
		super(Comment, self).save(*args, **kwargs)

	def get_absolute_url(self):
		return self.post.get_absolute_url()

	def __str__(self): 
		return '%s, %s' % (self.post, self.comment_id)

	class Meta:
		ordering = ['-created']


class Photo(models.Model):
	def get_post_image(instance, filename):
		return 's/media/img/content/%s_%s' % (str(time()).replace('.', '_'), filename)

	photo_id = models.CharField(primary_key=True, max_length=16, default=_createId) 
	photo = models.FileField(upload_to=get_post_image)
	post = models.ForeignKey(Post, related_name='photo')

	def __str__(self):
		return self.photo