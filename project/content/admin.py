from django.contrib import admin

from content.models import Sub, SubFollow, Post, Commit


admin.site.register(Sub)
admin.site.register(SubFollow)
admin.site.register(Post)
admin.site.register(Commit)