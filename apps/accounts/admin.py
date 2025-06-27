from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, UserProfile


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = '프로필'


class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('email', 'nickname', 'username', 'is_staff', 'date_joined')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'date_joined', 'gender', 'activity_level')
    search_fields = ('email', 'nickname', 'username')
    ordering = ('-date_joined',)
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('추가 정보', {
            'fields': ('nickname', 'birth_date', 'gender', 'height', 'weight', 'activity_level', 'timezone')
        }),
    )
    
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('추가 정보', {
            'fields': ('email', 'nickname', 'birth_date', 'gender', 'height', 'weight', 'activity_level')
        }),
    )


admin.site.register(User, UserAdmin)
admin.site.register(UserProfile)