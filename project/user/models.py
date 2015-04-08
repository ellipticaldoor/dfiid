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