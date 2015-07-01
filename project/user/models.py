from django.db import models
from django.conf import settings
from django.db.utils import IntegrityError
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

from time import time
from markdown import markdown


class UserManager(BaseUserManager):
	def create_user(self, password, *args, **kwargs):
		user = self.model(*args, **kwargs)
		user.set_password(password)
		user.save()
		return user

	def create_superuser(self, username, password, *args, **kwargs):
		superuser = self.create_user(username=username, password=password)
		superuser.is_staff = superuser.is_admin = superuser.is_superuser = True
		superuser.set_password(password)
		superuser.save()
		return superuser


class User(AbstractBaseUser, PermissionsMixin):
	def get_avatar(instance, filename):
		return 'user/avatar/%s.png' % instance.pk

	def get_cover(instance, filename):
		return 'user/cover/%s.png' % instance.pk

	username = models.SlugField(primary_key=True, max_length=16)
	USERNAME_FIELD = 'username'

	created = models.DateTimeField(auto_now_add=True)
	last_commited = models.DateTimeField(auto_now_add=True)

	is_active = models.BooleanField(default=True)
	is_admin = models.BooleanField(default=False)
	is_staff = models.BooleanField(default=False)

	avatar = models.ImageField(upload_to=get_avatar)
	cover = models.ImageField(upload_to=get_cover, blank=True, null=True)

	# Follow related fields
	follower_number = models.IntegerField(default=0)
	following_number = models.IntegerField(default=0)
	sub_following_number = models.IntegerField(default=0)

	# Notify related fields
	noty_number = models.IntegerField(default=0)

	objects = UserManager()

	def get_short_name(self):
		return self.pk
	def get_full_name(self):
		return self.pk
	def get_absolute_url(self):
		return '/%s' % (self.pk)
	def get_avatar_url(self):
		return '/m/%s' % (self.avatar)
	def get_avatar_thumb_url(self):
		return '/m/user/avatar/%s_thumb.png' % (self.pk)
	def get_cover_url(self):
		return '/m/%s' % (self.cover)

	class Meta:
		ordering = ['-last_commited']


class UserFollowQuerySet(models.QuerySet):
	def by_id(self, followid):
		return self.filter(followid=followid)


class UserFollow(models.Model):
	followid = models.CharField(primary_key=True, max_length=33, blank=True)
	follower = models.ForeignKey(User, related_name='follower')
	followed = models.ForeignKey(User, related_name='followed')

	objects = UserFollowQuerySet.as_manager()

	def save(self, *args, **kwargs):
		self.followid = '%s>%s' % (self.follower, self.followed)
		super(UserFollow, self).save(*args, **kwargs)

	def get_follower_avatar(self):
		return '/m/user/avatar/%s.png' % (self.follower_id)
	def get_followed_avatar(self):
		return '/m/user/avatar/%s.png' % (self.followed_id)
	def get_followed_avatar_thumb(self):
		return '/m/user/avatar/%s_thumb.png' % (self.followed_id)

	def __str__(self):
		return self.followid
