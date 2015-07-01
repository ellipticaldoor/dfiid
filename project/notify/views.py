from django.db import models

from user.models import User
from core.core import _createId


class Noty(models.Model):
    NOTY_CHOICES = (
        ('P', 'post'),
        ('C', 'commit'),
        ('F', 'follow'),
        ('M', 'message'),
    )

    notyid = models.CharField(primary_key=True, max_length=16, default=_createId)
    user = models.ForeignKey(User, related_name='notys')
    url = models.CharField(max_length=2200)
    description = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    show = models.BooleanField(default=True)
    categoty = models.CharField(max_length=2, choices=NOTY_CHOICES)

    def __str__(self):
        return self.notyid

	class Meta:
		ordering = ['-created']
