from time import time
from markdown import markdown

from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from core.core import _createId


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
	username = models.CharField(primary_key=True, max_length=16)
	USERNAME_FIELD = 'username'

	created = models.DateTimeField(auto_now_add=True)

	is_active = models.BooleanField(default=True)
	is_admin = models.BooleanField(default=False)
	is_staff = models.BooleanField(default=False)

	objects = UserManager()

	def get_short_name(self): return self.username
	def get_full_name(self): return self.username

	class Meta:
		ordering = ['-created']


class ProfileManager(BaseUserManager):
	def create_profile(self, *args, **kwargs):
		profile = self.model(*args, **kwargs)
		profile.save()
		return profile


class Profile(models.Model):
	def get_profile_image(instance, filename):
		return 's/media/img/profile/%s_%s' % (str(time()).replace('.', '_'), filename)

	user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='profile', primary_key=True)
	image = models.FileField(upload_to=get_profile_image, blank=True)
	bio = models.TextField(max_length=500, blank=True)
	bio_html = models.TextField(blank=True, null=True)

	objects = ProfileManager()

	def save(self):
		self.bio_html = markdown(self.bio, safe_mode=True)
		super(Profile, self).save()

	def get_absolute_url(self):
		if not hasattr(self.user, 'decode'): user = self.user
		else: user = self.user.decode('utf-8')
		return '/user/%s' % (user)

	def __str__(self): return str(self.user)