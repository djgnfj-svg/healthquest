from rest_framework import serializers
from .models import Guild, GuildMembership, GuildQuest, GuildMessage, GuildRanking
from apps.accounts.serializers import UserSerializer


class GuildSerializer(serializers.ModelSerializer):
    member_count = serializers.ReadOnlyField()
    is_full = serializers.ReadOnlyField()
    
    class Meta:
        model = Guild
        fields = (
            'id', 'name', 'description', 'motto', 'max_members', 'is_private',
            'join_code', 'level', 'experience_points', 'total_quests_completed',
            'emblem', 'color_theme', 'member_count', 'is_full', 'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'level', 'experience_points', 'total_quests_completed', 'created_at', 'updated_at')


class GuildMembershipSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    guild = GuildSerializer(read_only=True)
    
    class Meta:
        model = GuildMembership
        fields = '__all__'
        read_only_fields = ('id', 'joined_at', 'updated_at')


class GuildQuestSerializer(serializers.ModelSerializer):
    progress_percentage = serializers.ReadOnlyField()
    guild = GuildSerializer(read_only=True)
    
    class Meta:
        model = GuildQuest
        fields = '__all__'
        read_only_fields = ('id', 'guild', 'current_progress', 'created_at', 'updated_at')


class GuildMessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    recipient = UserSerializer(read_only=True)
    
    class Meta:
        model = GuildMessage
        fields = '__all__'
        read_only_fields = ('id', 'sender', 'created_at')


class GuildRankingSerializer(serializers.ModelSerializer):
    guild = GuildSerializer(read_only=True)
    
    class Meta:
        model = GuildRanking
        fields = '__all__'


class GuildCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guild
        fields = ('name', 'description', 'motto', 'max_members', 'is_private', 'emblem', 'color_theme')


class GuildJoinSerializer(serializers.Serializer):
    join_code = serializers.CharField(max_length=10, required=False)
    guild_id = serializers.IntegerField(required=False)
    
    def validate(self, attrs):
        if not attrs.get('join_code') and not attrs.get('guild_id'):
            raise serializers.ValidationError("길드 코드 또는 길드 ID가 필요합니다.")
        return attrs