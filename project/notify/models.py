from django.db import models

from user.models import User, UserFollow
from content.models import Post, Commit
from core.core import _createId


class Noty(models.Model):
	NOTY_CHOICES = (
		('C', 'commit'),
		('F', 'follow'),
	)

	notyid = models.CharField(primary_key=True, max_length=16, default=_createId)
	user = models.ForeignKey(User, related_name='notys')
	category = models.CharField(max_length=2, choices=NOTY_CHOICES)
	commit = models.ForeignKey(Commit, related_name='notys_post', blank=True, null=True)
	follow = models.ForeignKey(UserFollow, related_name='notys_follow', blank=True, null=True)
	created = models.DateTimeField(auto_now_add=True)
	show = models.BooleanField(default=True)

	def get_absolute_url(self):
		return self.commit.get_commit_url()

	def get_read_url(self):
		return '/notify/read/%s' % self.notyid

	def create_noty(self):
		self.user.noty_number += 1
		self.user.save()
		return

	def read_noty(self):
		self.show = False
		self.save()
		self.user.noty_number -= 1
		self.user.save()
		return

	def __str__(self):
		return self.notyid

	class Meta:
		ordering = ['-created']
