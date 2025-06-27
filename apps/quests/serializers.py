from rest_framework import serializers
from .models import QuestTemplate, Quest, QuestCompletion, DailyStreak


class QuestTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestTemplate
        fields = '__all__'


class QuestSerializer(serializers.ModelSerializer):
    template = QuestTemplateSerializer(read_only=True)
    title = serializers.ReadOnlyField()
    description = serializers.ReadOnlyField()
    is_overdue = serializers.SerializerMethodField()
    
    class Meta:
        model = Quest
        fields = (
            'id', 'template', 'custom_title', 'custom_description',
            'title', 'description', 'target_stats', 'experience_reward',
            'gold_reward', 'gems_reward', 'status', 'assigned_date',
            'start_date', 'due_date', 'completed_date', 'progress_percentage',
            'requires_verification', 'verification_image', 'verification_note',
            'is_overdue', 'created_at', 'updated_at'
        )
        read_only_fields = (
            'id', 'user', 'assigned_date', 'start_date', 'completed_date',
            'created_at', 'updated_at'
        )

    def get_is_overdue(self, obj):
        return obj.is_overdue()


class QuestCompletionSerializer(serializers.ModelSerializer):
    quest = QuestSerializer(read_only=True)
    
    class Meta:
        model = QuestCompletion
        fields = '__all__'
        read_only_fields = ('id', 'completion_time')


class DailyStreakSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyStreak
        fields = '__all__'
        read_only_fields = ('id', 'user')


class QuestStartSerializer(serializers.Serializer):
    """퀘스트 시작 시리얼라이저"""
    pass


class QuestCompleteSerializer(serializers.Serializer):
    """퀘스트 완료 시리얼라이저"""
    verification_image = serializers.ImageField(required=False)
    verification_note = serializers.CharField(max_length=500, required=False)
    difficulty_rating = serializers.IntegerField(min_value=1, max_value=5, required=False)
    satisfaction_rating = serializers.IntegerField(min_value=1, max_value=5, required=False)
    user_notes = serializers.CharField(max_length=1000, required=False)