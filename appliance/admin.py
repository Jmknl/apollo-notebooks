from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

admin.site.unregister(User)

@admin.register(User)
class CentroDeComandoAdmin(UserAdmin):
    list_display = ("username", "email", "is_active", "date_joined", "last_login")

    list_filter = ("is_active", "is_staff", "date_joined")

    search_fields = ("username", "email")

    ordering = ("-date_joined",)


