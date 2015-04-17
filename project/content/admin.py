from django.contrib import admin

from content.models import Post, Comment, Sub, Photo


admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Sub)
admin.site.register(Photo)