from django.contrib import admin
from .models import Product

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from weights.models import PigeonUser


class PigeonUserInline(admin.StackedInline):
    model = PigeonUser
    can_delete = False
    verbose_name_plural = 'pigeonuser'


class UserAdmin(BaseUserAdmin):
    inlines = (PigeonUserInline, )

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# Register your models here.
admin.site.register(Product)
