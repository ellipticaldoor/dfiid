from django.contrib import admin

from content.models import Post, Comment, Photo


admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Photo)