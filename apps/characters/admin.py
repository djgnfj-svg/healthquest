from django.contrib import admin
from .models import Character, Achievement, UserAchievement, StatHistory


@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'level', 'health_score', 'total_stats', 'created_at')
    list_filter = ('level', 'created_at')
    search_fields = ('name', 'user__nickname', 'user__email')
    readonly_fields = ('created_at', 'updated_at', 'health_score', 'total_stats')
    
    fieldsets = (
        ('기본 정보', {
            'fields': ('user', 'name', 'level', 'experience_points')
        }),
        ('스탯', {
            'fields': (
                'stamina', 'strength', 'mental', 'endurance',
                'cardio', 'flexibility', 'nutrition', 'recovery'
            )
        }),
        ('보상', {
            'fields': ('gold', 'gems')
        }),
        ('외관', {
            'fields': ('skin', 'avatar_url')
        }),
        ('시간 정보', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'requirement_type', 'requirement_value', 'is_active')
    list_filter = ('category', 'requirement_type', 'is_active')
    search_fields = ('name', 'description')


@admin.register(UserAchievement)
class UserAchievementAdmin(admin.ModelAdmin):
    list_display = ('user', 'achievement', 'achieved_at', 'is_displayed')
    list_filter = ('achieved_at', 'is_displayed', 'achievement__category')
    search_fields = ('user__nickname', 'achievement__name')


@admin.register(StatHistory)
class StatHistoryAdmin(admin.ModelAdmin):
    list_display = ('character', 'stat_type', 'old_value', 'new_value', 'change_reason', 'created_at')
    list_filter = ('stat_type', 'created_at')
    search_fields = ('character__name', 'change_reason')
    readonly_fields = ('created_at',)