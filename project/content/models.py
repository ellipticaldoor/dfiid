from markdown import markdown

from django.db import models
from django.utils.text import slugify

from user.models import User
from core.core import _createId


class Sub(models.Model):
	def get_image(instance, filename):
		return 's/media/sub/image/%s.png' % (instance.slug)

	slug = models.SlugField(primary_key=True, max_length=100)
	image = models.FileField(upload_to=get_image)
	created = models.DateTimeField(auto_now_add=True)
	last_commited = models.DateTimeField(auto_now_add=True)

	def get_absolute_url(self):
		return '/sub/%s' % (str(self.slug))

	def __str__(self):
		return str(self.slug)

	class Meta:
		ordering = ['-last_commited']


class PostQuerySet(models.QuerySet):
	def published(self):
		return self.filter(draft=False, show=True)

	def by_sub(self, sub):
		return self.filter(sub=sub, draft=False, show=True)

	def by_user(self, user):
		return self.filter(user=user, show=True)

	def by_post(self, pk, slug):
		return self.filter(pk=pk, slug=slug, draft=False, show=True)


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
	last_commited = models.DateTimeField(auto_now_add=True)
	commit_number = models.IntegerField(default=0)
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

	def get_commit_url(self):
		return '%scommit/' % (self.get_absolute_url())

	def get_view_commits_url(self):
		return '%s#commits' % (self.get_absolute_url())

	# Don't use it until refactor!!
	def get_avatar_url(self):
		return '/s/media/user/avatar/%s.png' % (self.user)

	def __str__(self): return self.title

	class Meta:
		ordering = ['-last_commited']


class Commit(models.Model):
	commit_id = models.CharField(primary_key=True, max_length=16, default=_createId) 
	user = models.ForeignKey(User, related_name="commits")
	post = models.ForeignKey(Post, related_name="commits")
	body = models.TextField(max_length=500, default='')
	body_html  = models.TextField(blank=True, null=True)
	created = models.DateTimeField(auto_now_add=True)

	def save(self, *args, **kwargs):
		self.body_html = markdown(self.body, safe_mode=True)
		super(Commit, self).save(*args, **kwargs)

	def get_absolute_url(self):
		return self.post.get_absolute_url()

	def __str__(self): 
		return '%s, %s' % (self.post, self.commit_id)

	class Meta:
		ordering = ['-created']


class Photo(models.Model):
	def get_post_image(instance, filename):
		return 's/media/photo/%s.png' % (instance.photo_id)

	photo_id = models.CharField(primary_key=True, max_length=16, default=_createId) 
	photo = models.FileField(upload_to=get_post_image)
	post = models.ForeignKey(Post, related_name='photo')
	created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.photo