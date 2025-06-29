from rest_framework import serializers
from .models import (
    Character, Achievement, UserAchievement, StatHistory,
    NutritionLog, Supplement, UserSupplement, SupplementLog
)


class CharacterSerializer(serializers.ModelSerializer):
    health_score = serializers.ReadOnlyField()
    total_stats = serializers.ReadOnlyField()
    
    class Meta:
        model = Character
        fields = (
            'id', 'name', 'level', 'experience_points',
            'stamina', 'strength', 'mental', 'endurance',
            'cardio', 'flexibility', 'nutrition', 'recovery',
            'gold', 'gems', 'skin', 'avatar_url',
            'health_score', 'total_stats', 'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'user', 'level', 'experience_points', 'gold', 'gems', 'created_at', 'updated_at')


class StatHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = StatHistory
        fields = '__all__'
        read_only_fields = ('id', 'character', 'created_at')


class AchievementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Achievement
        fields = '__all__'


class UserAchievementSerializer(serializers.ModelSerializer):
    achievement = AchievementSerializer(read_only=True)
    
    class Meta:
        model = UserAchievement
        fields = '__all__'
        read_only_fields = ('id', 'user', 'achieved_at')


class NutritionLogSerializer(serializers.ModelSerializer):
    nutrition_score = serializers.ReadOnlyField()
    meal_type_display = serializers.CharField(source='get_meal_type_display', read_only=True)
    meal_quality_display = serializers.CharField(source='get_meal_quality_display', read_only=True)
    
    class Meta:
        model = NutritionLog
        fields = (
            'id', 'date', 'meal_type', 'meal_type_display', 
            'meal_quality', 'meal_quality_display',
            'included_vegetables', 'included_protein', 
            'included_grains', 'proper_portion',
            'notes', 'calories_estimate', 'meal_image',
            'nutrition_score', 'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'user', 'nutrition_score', 'created_at', 'updated_at')


class SupplementSerializer(serializers.ModelSerializer):
    user_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Supplement
        fields = (
            'id', 'name', 'category', 'description', 
            'default_dosage', 'precautions', 'user_count', 
            'is_active', 'created_at'
        )
        read_only_fields = ('id', 'user_count', 'created_at')
    
    def get_user_count(self, obj):
        return obj.usersupplement_set.filter(is_active=True).count()


class UserSupplementSerializer(serializers.ModelSerializer):
    supplement = SupplementSerializer(read_only=True)
    supplement_id = serializers.IntegerField(write_only=True)
    schedule_display = serializers.SerializerMethodField()
    
    class Meta:
        model = UserSupplement
        fields = (
            'id', 'supplement', 'supplement_id', 'dosage', 'frequency',
            'morning', 'afternoon', 'evening', 'schedule_display',
            'personal_notes', 'is_active', 'started_date', 'ended_date',
            'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'user', 'created_at', 'updated_at')
    
    def get_schedule_display(self, obj):
        times = []
        if obj.morning:
            times.append('아침')
        if obj.afternoon:
            times.append('오후')
        if obj.evening:
            times.append('저녁')
        return ', '.join(times) if times else '미설정'


class SupplementLogSerializer(serializers.ModelSerializer):
    supplement_name = serializers.CharField(source='user_supplement.supplement.name', read_only=True)
    user_supplement_id = serializers.IntegerField(write_only=True)
    time_of_day_display = serializers.CharField(source='get_time_of_day_display', read_only=True)
    
    class Meta:
        model = SupplementLog
        fields = (
            'id', 'user_supplement_id', 'supplement_name', 
            'taken_at', 'dosage_taken', 'time_of_day', 'time_of_day_display',
            'notes', 'side_effects', 'created_at'
        )
        read_only_fields = ('id', 'created_at')


class NutritionStatsSerializer(serializers.Serializer):
    """영양 통계 시리얼라이저"""
    daily_average_score = serializers.FloatField()
    weekly_average_score = serializers.FloatField()
    monthly_average_score = serializers.FloatField()
    total_logs = serializers.IntegerField()
    excellent_meals = serializers.IntegerField()
    good_meals = serializers.IntegerField()
    fair_meals = serializers.IntegerField()
    poor_meals = serializers.IntegerField()
    vegetables_percentage = serializers.FloatField()
    protein_percentage = serializers.FloatField()
    grains_percentage = serializers.FloatField()
    proper_portion_percentage = serializers.FloatField()