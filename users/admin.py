from django.contrib import admin

from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'username')

    def save_model(self, request, instance, form, change):
        if "password" in form.changed_data:
            instance.set_password(instance.password)
        super().save_model(request, instance, form, change)
