from django.conf import settings
from django.db import models


class Info(models.Model):
	SUB, USER, POST = 'S', 'U', 'P'
	URL_TYPE = ((SUB, 'sub'), (USER, 'user'), (POST, 'post'))

	url = models.SlugField(max_length=100)
	url_type = models.CharField(max_length=1, choices=URL_TYPE)
	user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='gallery')

	def __str__(self):
		return self.slug