from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Count, Avg
from .models import (
    Character, Achievement, UserAchievement, StatHistory,
    NutritionLog, Supplement, UserSupplement, SupplementLog
)


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


@admin.register(NutritionLog)
class NutritionLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'meal_type', 'meal_quality', 'nutrition_score_display', 'created_at')
    list_filter = ('meal_type', 'meal_quality', 'date', 'included_vegetables', 'included_protein')
    search_fields = ('user__nickname', 'user__email', 'notes')
    readonly_fields = ('nutrition_score_display', 'created_at', 'updated_at')
    date_hierarchy = 'date'
    
    fieldsets = (
        ('기본 정보', {
            'fields': ('user', 'date', 'meal_type', 'meal_quality')
        }),
        ('영양 체크리스트', {
            'fields': (
                'included_vegetables', 'included_protein', 
                'included_grains', 'proper_portion'
            )
        }),
        ('추가 정보', {
            'fields': ('calories_estimate', 'notes', 'meal_image')
        }),
        ('점수 및 시간', {
            'fields': ('nutrition_score_display', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def nutrition_score_display(self, obj):
        score = obj.nutrition_score
        if score >= 80:
            color = 'green'
        elif score >= 60:
            color = 'orange'
        else:
            color = 'red'
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color, score
        )
    nutrition_score_display.short_description = '영양 점수'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')


@admin.register(Supplement)
class SupplementAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'default_dosage', 'user_count', 'is_active', 'created_at')
    list_filter = ('category', 'is_active', 'created_at')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'user_count')
    
    fieldsets = (
        ('기본 정보', {
            'fields': ('name', 'category', 'description')
        }),
        ('복용 정보', {
            'fields': ('default_dosage', 'precautions')
        }),
        ('상태', {
            'fields': ('is_active', 'user_count', 'created_at')
        }),
    )
    
    def user_count(self, obj):
        return obj.usersupplement_set.filter(is_active=True).count()
    user_count.short_description = '사용자 수'
    
    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('usersupplement_set')


@admin.register(UserSupplement)
class UserSupplementAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'supplement', 'dosage', 'frequency', 
        'schedule_display', 'is_active', 'started_date'
    )
    list_filter = ('frequency', 'is_active', 'started_date', 'supplement__category')
    search_fields = ('user__nickname', 'supplement__name')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'started_date'
    
    fieldsets = (
        ('기본 정보', {
            'fields': ('user', 'supplement', 'dosage', 'frequency')
        }),
        ('복용 시간', {
            'fields': ('morning', 'afternoon', 'evening')
        }),
        ('기간 설정', {
            'fields': ('started_date', 'ended_date', 'is_active')
        }),
        ('메모', {
            'fields': ('personal_notes',)
        }),
        ('시간 정보', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def schedule_display(self, obj):
        times = []
        if obj.morning:
            times.append('아침')
        if obj.afternoon:
            times.append('오후')
        if obj.evening:
            times.append('저녁')
        return ', '.join(times) if times else '미설정'
    schedule_display.short_description = '복용 시간'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'supplement')


@admin.register(SupplementLog)
class SupplementLogAdmin(admin.ModelAdmin):
    list_display = (
        'supplement_name', 'user_name', 'taken_at', 
        'time_of_day', 'dosage_taken', 'has_side_effects'
    )
    list_filter = ('time_of_day', 'taken_at', 'user_supplement__supplement__category')
    search_fields = (
        'user_supplement__user__nickname', 
        'user_supplement__supplement__name',
        'notes', 'side_effects'
    )
    readonly_fields = ('created_at',)
    date_hierarchy = 'taken_at'
    
    fieldsets = (
        ('복용 정보', {
            'fields': ('user_supplement', 'taken_at', 'time_of_day', 'dosage_taken')
        }),
        ('기록', {
            'fields': ('notes', 'side_effects')
        }),
        ('시간 정보', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def supplement_name(self, obj):
        return obj.user_supplement.supplement.name
    supplement_name.short_description = '영양제'
    
    def user_name(self, obj):
        return obj.user_supplement.user.nickname
    user_name.short_description = '사용자'
    
    def has_side_effects(self, obj):
        return bool(obj.side_effects)
    has_side_effects.boolean = True
    has_side_effects.short_description = '부작용 있음'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'user_supplement__user', 
            'user_supplement__supplement'
        )