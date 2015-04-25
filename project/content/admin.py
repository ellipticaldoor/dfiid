from django.contrib import admin

from content.models import Sub, Post, Commit, Photo


admin.site.register(Sub)
admin.site.register(Post)
admin.site.register(Commit)
admin.site.register(Photo)