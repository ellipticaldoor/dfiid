from markdown import markdown

from django.db import models
from django.utils.text import slugify

from core.core import _createId


class AnonPostQuerySet(models.QuerySet):
	def published(self):
		return self.filter(show=True)

	def by_post(self, pk, slug):
		return self.get(pk=pk, slug=slug, show=True)


class AnonPost(models.Model):
	def get_image(instance, filename):
		return 's/media/anon/post/%s.png' % (instance.postid)

	postid = models.CharField(primary_key=True, max_length=16, default=_createId)
	title = models.CharField(max_length=100)
	slug = models.SlugField(max_length=100)
	body = models.TextField(max_length=3000, default='', blank=True)
	body_html  = models.TextField(blank=True, null=True)
	image = models.ImageField(upload_to=get_image, blank=True, null=True)
	created = models.DateTimeField(auto_now_add=True)
	last_commited = models.DateTimeField(auto_now_add=True)
	commit_number = models.IntegerField(default=0)
	show = models.BooleanField(default=True)

	objects = AnonPostQuerySet.as_manager()

	def save(self, *args, **kwargs):
		self.slug = slugify(self.title.replace(' ', '_'))
		if not self.slug: self.slug = '_'
		self.body_html = markdown(self.body, safe_mode=True, extensions=['video'])
		super(AnonPost, self).save(*args, **kwargs)

	def get_absolute_url(self):
		if not hasattr(self.postid, 'decode'): postid = self.postid
		else: postid = self.postid.decode('utf-8')
		return '/anon/%s/%s/' % (postid, self.slug)

	def get_view_commits_url(self): return '%s#commits' % (self.get_absolute_url())

	def __str__(self): return self.title

	class Meta: ordering = ['-last_commited']


class AnonCommit(models.Model):
	commitid = models.CharField(primary_key=True, max_length=16, default=_createId) 
	post = models.ForeignKey(AnonPost, related_name="commits")
	body = models.TextField(max_length=500, default='')
	body_html  = models.TextField(blank=True, null=True)
	created = models.DateTimeField(auto_now_add=True)

	def save(self, *args, **kwargs):
		self.body_html = markdown(self.body, safe_mode=True, extensions=['video'])
		super(AnonCommit, self).save(*args, **kwargs)

	def get_absolute_url(self): return self.post.get_absolute_url()

	def __str__(self): return '%s, %s' % (self.post, self.commitid)

	class Meta: ordering = ['-created']