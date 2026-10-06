from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class BaraholkaAdminUser(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (("Барахолка", {"fields": ("city",)}),)
    add_fieldsets = UserAdmin.add_fieldsets + (("Контакты", {"fields": ("email", "city")}),)
