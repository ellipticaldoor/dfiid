from django.contrib import admin

from content.models import Post, PostPhoto


class PostAdmin(admin.ModelAdmin):
	list_display = ('title', 'pub_date')


admin.site.register(PostPhoto)
admin.site.register(Post, PostAdmin)