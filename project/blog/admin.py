from django.contrib import admin
from django.db import models

from blog.models import Tag, Post, PostPhoto


class PostAdmin(admin.ModelAdmin):
	list_display = ('title', 'pub_date')

admin.site.register(Tag)
admin.site.register(PostPhoto)
admin.site.register(Post, PostAdmin)
