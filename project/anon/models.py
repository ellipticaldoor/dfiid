from markdown import markdown

from django.db import models
from django.utils.text import slugify

from core.core import _createId
from core.video_embed import CustomVideoExtension

from django_resized import ResizedImageField


class AnonPostQuerySet(models.QuerySet):
	def last_commited(self):
		return self.filter(show=True).order_by('-last_commited')

	def created(self):
		return self.filter(show=True).order_by('-created')

	def by_post(self, pk, slug):
		return self.get(pk=pk, slug=slug, show=True)


class AnonPost(models.Model):
	def get_image(instance, filename):
		if not hasattr(instance.postid, 'decode'): postid = instance.postid
		else: postid = instance.postid.decode('utf-8')
		return 's/media/post/%s.png' % (postid)

	postid = models.CharField(primary_key=True, max_length=16, default=_createId)
	title = models.CharField(max_length=100)
	slug = models.SlugField(max_length=100)
	body = models.TextField(max_length=3000)
	body_html  = models.TextField(blank=True, null=True)
	image = ResizedImageField(size=[950, 950], upload_to=get_image, blank=True, null=True)
	created = models.DateTimeField(auto_now_add=True)
	last_commited = models.DateTimeField(auto_now_add=True)
	commit_number = models.IntegerField(default=0)
	show = models.BooleanField(default=True)

	objects = AnonPostQuerySet.as_manager()

	def save(self, *args, **kwargs):
		self.slug = slugify(self.title.replace(' ', '_'))
		if not self.slug: self.slug = '_'
		self.body_html = markdown(self.body, safe_mode=True, extensions=[CustomVideoExtension()])
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
		self.body_html = markdown(self.body, safe_mode=True, extensions=[CustomVideoExtension()])
		super(AnonCommit, self).save(*args, **kwargs)

	def get_absolute_url(self): return self.post.get_absolute_url()

	def __str__(self): return '%s, %s' % (self.post, self.commitid)

	class Meta: ordering = ['-created']