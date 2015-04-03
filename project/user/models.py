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

class UserQuerySet(models.QuerySet):
	def published(self):
		# TODO: Publicar solo entradas con pub_date menor a la fecha actual
		return self.filter(draft=False)

	def by_post(self, pk, slug):
		return self.filter(pk=pk, slug=slug, draft=False)

	def by_author(self, author):
		return self.filter(author=author, draft=False)

	def by_tag(self, tag):
		return self.filter(tag=tag, draft=False)

	def by_date(self, year, month):
		return self.filter(pub_date__year=year, pub_date__month=month, draft=False)

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

	def get_absolute_url(self):
		if not hasattr(self.user, 'decode'): user = self.user
		else: user = self.user.decode('utf-8')
		return '/author/%s' % (user)

	def __str__(self): return str(self.user)