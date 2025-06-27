from django.contrib import admin
from .models import Guild, GuildMembership, GuildQuest, GuildMessage, GuildRanking


@admin.register(Guild)
class GuildAdmin(admin.ModelAdmin):
    list_display = ('name', 'level', 'member_count', 'is_private', 'created_at')
    list_filter = ('is_private', 'level', 'created_at')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at', 'member_count')
    
    fieldsets = (
        ('기본 정보', {
            'fields': ('name', 'description', 'motto')
        }),
        ('설정', {
            'fields': ('max_members', 'is_private', 'join_code')
        }),
        ('통계', {
            'fields': ('level', 'experience_points', 'total_quests_completed')
        }),
        ('외관', {
            'fields': ('emblem', 'color_theme')
        }),
        ('시간 정보', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(GuildMembership)
class GuildMembershipAdmin(admin.ModelAdmin):
    list_display = ('user', 'guild', 'role', 'status', 'joined_at')
    list_filter = ('role', 'status', 'joined_at')
    search_fields = ('user__nickname', 'guild__name')
    readonly_fields = ('joined_at', 'updated_at')


@admin.register(GuildQuest)
class GuildQuestAdmin(admin.ModelAdmin):
    list_display = ('title', 'guild', 'status', 'progress_percentage', 'start_date', 'end_date')
    list_filter = ('status', 'target_type', 'start_date')
    search_fields = ('title', 'guild__name')
    readonly_fields = ('created_at', 'updated_at', 'progress_percentage')


@admin.register(GuildMessage)
class GuildMessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'guild', 'message_type', 'content_preview', 'created_at')
    list_filter = ('message_type', 'created_at')
    search_fields = ('sender__nickname', 'guild__name', 'content')
    readonly_fields = ('created_at',)
    
    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = '메시지 미리보기'


@admin.register(GuildRanking)
class GuildRankingAdmin(admin.ModelAdmin):
    list_display = ('guild', 'ranking_type', 'rank_position', 'score', 'start_date', 'end_date')
    list_filter = ('ranking_type', 'start_date')
    search_fields = ('guild__name',)
    readonly_fields = ('created_at',)