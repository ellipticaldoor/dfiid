from time import time
from django.conf import settings
from django.db import models
from django.contrib.auth.models import BaseUserManager


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
	bio = models.CharField(max_length=255, blank=True)

	objects = ProfileManager()

	def get_absolute_url(self):
		if not hasattr(self.user, 'decode'): user = self.user
		else: user = self.user.decode('utf-8')
		return '/user/%s' % (user)

	def __str__(self): return str(self.user)