from django.contrib import admin

from user.models import User


class UserAdmin(admin.ModelAdmin):
	readonly_fields = ('created',)


admin.site.register(User, UserAdmin)
