from django.contrib import admin
from user.models import User
# Register your models here.


# admin.site.register(User)
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username','email', 'is_staff', 'role']
    list_filter = ['is_staff', 'role']
    search_fields = ['username', 'first_name', 'last_name']
    ordering = ['date_joined']
