from time import time
from markdown import markdown

from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


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
		return 's/media/img/avatar/%s.png' % (instance.username)

	username = models.CharField(primary_key=True, max_length=16)
	USERNAME_FIELD = 'username'

	created = models.DateTimeField(auto_now_add=True)

	is_active = models.BooleanField(default=True)
	is_admin = models.BooleanField(default=False)
	is_staff = models.BooleanField(default=False)

	avatar = models.FileField(upload_to=get_avatar)
	bio = models.TextField(max_length=500, default=':3')
	bio_html = models.TextField(blank=True, null=True)

	objects = UserManager()

	def save(self, *args, **kwargs):
		self.bio_html = markdown(self.bio, safe_mode=True)
		super(User, self).save()

	def get_short_name(self): return self.username

	def get_full_name(self): return self.username

	def get_absolute_url(self):
		if not hasattr(self.user, 'decode'): user = self.user
		else: user = self.user.decode('utf-8')
		return '/user/%s' % (user)

	class Meta: ordering = ['-created']
 