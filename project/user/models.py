from time import time
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
		superuser.save()

		return superuser


class User(AbstractBaseUser, PermissionsMixin):
	username = models.CharField(primary_key=True, max_length=16, default=_createId)
	USERNAME_FIELD = 'username'

	created = models.DateTimeField(auto_now_add=True)

	is_active = models.BooleanField(default=True)
	is_admin = models.BooleanField(default=False)
	is_staff = models.BooleanField(default=False)

	objects = UserManager()

	def get_short_name(self): return self.username
	def get_full_name(self): return self.username


class Profile(models.Model):
	def get_profile_image(instance, filename):
		return 's/media/img/user/profile/%s_%s' % (str(time()).replace('.', '_'), filename)

	user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='profile', primary_key=True)
	email = models.EmailField(unique=True)
	image = models.FileField(upload_to=get_profile_image, blank=True)
	bio = models.CharField(max_length=255, blank=True)

	def __str__(self): return str(self.user)