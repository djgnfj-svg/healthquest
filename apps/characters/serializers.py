from rest_framework import serializers
from .models import Character, Achievement, UserAchievement, StatHistory


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