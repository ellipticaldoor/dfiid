from markdown import markdown

from django.db import models
from django.utils.text import slugify

from user.models import User
from core.core import _createId
from core.video_embed import CustomVideoExtension

from django_resized import ResizedImageField


class Sub(models.Model):
	def get_image(instance, filename):
		return 's/media/sub/image/%s.png' % (instance.slug)

	slug = models.SlugField(primary_key=True, max_length=10)
	image = models.ImageField(upload_to=get_image)
	created = models.DateTimeField(auto_now_add=True)
	last_commited = models.DateTimeField(auto_now_add=True)
	follower_number = models.IntegerField(default=0)

	def get_absolute_url(self): return '/sub/%s' % (str(self.slug))

	def __str__(self): return str(self.slug)

	class Meta: ordering = ['-last_commited']


class SubFollowQuerySet(models.QuerySet):
	def by_id(self, sub_followid):
		return self.filter(sub_followid=sub_followid)


class SubFollow(models.Model):
	sub_followid = models.CharField(primary_key=True, max_length=33, blank=True)
	follower = models.ForeignKey(User, related_name='sub_follower')
	sub = models.ForeignKey(Sub, related_name='sub_followed')

	objects = SubFollowQuerySet.as_manager()

	def save(self, *args, **kwargs):
		self.sub_followid = '%s>%s' % (self.follower, self.sub)
		super(SubFollow, self).save(*args, **kwargs)

	def __str__(self): return self.sub_followid


class PostQuerySet(models.QuerySet):
	def last_commited(self):
		return self.filter(draft=False, show=True).order_by('-last_commited')

	def created(self):
		return self.filter(draft=False, show=True).order_by('-created')

	def sub_last_commited(self, slug):
		return self.filter(draft=False, show=True, sub_id=slug).order_by('-last_commited')

	def sub_created(self, slug):
		return self.filter(draft=False, show=True, sub_id=slug).order_by('-created')

	def by_user(self, user):
		return self.filter(user=user, show=True).order_by('-created')

	def by_post(self, pk, slug):
		return self.get(pk=pk, slug=slug, draft=False, show=True)


class Post(models.Model):
	def get_image(instance, filename):
		if not hasattr(instance.postid, 'decode'): postid = instance.postid
		else: postid = instance.postid.decode('utf-8')
		return 's/media/post/%s.png' % (postid)

	postid = models.CharField(primary_key=True, max_length=16, default=_createId)
	user = models.ForeignKey(User, related_name='posts')
	sub = models.ForeignKey(Sub, related_name='posts')
	title = models.CharField(max_length=100)
	slug = models.SlugField(max_length=100)
	body = models.TextField(max_length=3000)
	body_html  = models.TextField(blank=True, null=True)
	image = ResizedImageField(size=[950, 950], quality=90, upload_to=get_image, blank=True, null=True)
	draft = models.BooleanField(default=False)
	created = models.DateTimeField(auto_now_add=True)
	last_commited = models.DateTimeField(null=True)
	commit_number = models.IntegerField(default=0)
	show = models.BooleanField(default=True)

	objects = PostQuerySet.as_manager()

	def save(self, *args, **kwargs):
		self.slug = slugify(self.title.replace(' ', '_'))
		if not self.slug: self.slug = '_'
		self.body_html = markdown(self.body, safe_mode=True, extensions=[CustomVideoExtension()])
		super(Post, self).save(*args, **kwargs)	

	def get_absolute_url(self):
		if not hasattr(self.postid, 'decode'): postid = self.postid
		else: postid = self.postid.decode('utf-8')
		return '/post/%s/%s/' % (postid, self.slug)

	def get_edit_url(self): return '%sedit/' % (self.get_absolute_url())
	def get_view_commits_url(self): return '%s#commits' % (self.get_absolute_url())
	def get_avatar_url(self): return '/s/media/user/avatar/%s.png' % (self.user_id)

	def __str__(self): return self.title


class Commit(models.Model):
	commitid = models.CharField(primary_key=True, max_length=16, default=_createId) 
	user = models.ForeignKey(User, related_name="commits")
	post = models.ForeignKey(Post, related_name="commits")
	body = models.TextField(max_length=500, default='')
	body_html  = models.TextField(blank=True, null=True)
	created = models.DateTimeField(auto_now_add=True)
	show = models.BooleanField(default=True)

	def save(self, *args, **kwargs):
		self.body_html = markdown(self.body, safe_mode=True, extensions=['video'])
		super(Commit, self).save(*args, **kwargs)

	def get_absolute_url(self): return self.post.get_absolute_url()
	def get_avatar_url(self): return '/s/media/user/avatar/%s.png' % (self.user_id)

	def __str__(self): return '%s, %s' % (self.post, self.commitid)

	class Meta: ordering = ['-created']