from django.db import models


class Sub(models.Model):
	slug = models.SlugField(max_length=100, primary_key=True)
	created = models.DateTimeField(auto_now_add=True)

	def get_absolute_url(self): return '/sub/%s' % (str(self.slug))

	def __str__(self): return str(self.slug)