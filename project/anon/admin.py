from django.contrib import admin

from anon.models import AnonPost, AnonCommit


admin.site.register(AnonPost)
admin.site.register(AnonCommit)