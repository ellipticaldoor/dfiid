from django.contrib import admin

from content.models import Post, PostComment, PostPhoto


class PostAdmin(admin.ModelAdmin):
	list_display = ('title', 'pub_date')


admin.site.register(Post, PostAdmin)
admin.site.register(PostComment)
admin.site.register(PostPhoto)