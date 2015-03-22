from django.contrib import admin

from user.models import User, Profile


class UserAdmin(admin.ModelAdmin):
	readonly_fields = ('created',)


admin.site.register(User, UserAdmin)
admin.site.register(Profile)