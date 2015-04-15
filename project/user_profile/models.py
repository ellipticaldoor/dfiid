from time import time
from markdown import markdown

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