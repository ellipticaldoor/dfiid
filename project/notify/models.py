from django.db import models

from user.models import User, UserFollow
from content.models import Post, Commit
from core.core import _createId


class Noty(models.Model):
	NOTY_CHOICES = (
		('P', 'post'),
		('C', 'commit'),
		('F', 'follow'),
	)

	notyid = models.CharField(primary_key=True, max_length=16, default=_createId)
	user = models.ForeignKey(User, related_name='notys')
	category = models.CharField(max_length=2, choices=NOTY_CHOICES)
	post = models.ForeignKey(Post, related_name='notys_post', blank=True, null=True)
	commit = models.ForeignKey(Commit, related_name='notys_post', blank=True, null=True)
	follow = models.ForeignKey(UserFollow, related_name='notys_follow', blank=True, null=True)
	description = models.TextField(blank=True, null=True)
	created = models.DateTimeField(auto_now_add=True)
	show = models.BooleanField(default=True)

	def get_absolute_url(self):
		if self.category == 'P':
			return self.post.get_absolute_url()
		elif self.category == 'C':
			return self.commit.get_absolute_url()
		elif self.category == 'F':
			return self.follow.get_absolute_url()

	def __str__(self):
		return self.notyid

	class Meta: ordering = ['-created']
