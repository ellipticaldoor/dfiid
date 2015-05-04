from django.contrib import admin

from user.models import User, UserFollow


admin.site.register(User)
admin.site.register(UserFollow)