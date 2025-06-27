from django.contrib import admin
from .models import QuestTemplate, Quest, QuestCompletion, DailyStreak


@admin.register(QuestTemplate)
class QuestTemplateAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'difficulty', 'base_experience', 'required_level', 'is_active')
    list_filter = ('category', 'difficulty', 'is_active', 'weather_condition', 'time_of_day')
    search_fields = ('title', 'description')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Quest)
class QuestAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'status', 'progress_percentage', 'due_date', 'created_at')
    list_filter = ('status', 'template__category', 'template__difficulty', 'created_at')
    search_fields = ('user__nickname', 'template__title', 'custom_title')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('기본 정보', {
            'fields': ('user', 'template', 'custom_title', 'custom_description')
        }),
        ('보상', {
            'fields': ('target_stats', 'experience_reward', 'gold_reward', 'gems_reward')
        }),
        ('상태', {
            'fields': ('status', 'progress_percentage')
        }),
        ('일정', {
            'fields': ('assigned_date', 'start_date', 'due_date', 'completed_date')
        }),
        ('검증', {
            'fields': ('requires_verification', 'verification_image', 'verification_note')
        }),
        ('시간 정보', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(QuestCompletion)
class QuestCompletionAdmin(admin.ModelAdmin):
    list_display = ('quest', 'completion_time', 'difficulty_rating', 'satisfaction_rating')
    list_filter = ('completion_time', 'difficulty_rating', 'satisfaction_rating')
    search_fields = ('quest__template__title', 'quest__user__nickname')
    readonly_fields = ('completion_time',)


@admin.register(DailyStreak)
class DailyStreakAdmin(admin.ModelAdmin):
    list_display = ('user', 'current_streak', 'longest_streak', 'last_completion_date')
    search_fields = ('user__nickname', 'user__email')
    readonly_fields = ('streak_start_date',)