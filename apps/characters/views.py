from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Character, StatHistory, UserAchievement
from .serializers import CharacterSerializer, StatHistorySerializer, UserAchievementSerializer


class CharacterDetailView(generics.RetrieveUpdateAPIView):
    """캐릭터 정보 조회/수정"""
    serializer_class = CharacterSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        character, created = Character.objects.get_or_create(
            user=self.request.user,
            defaults={
                'name': f"{self.request.user.nickname}의 캐릭터"
            }
        )
        return character


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def character_stats_view(request):
    """캐릭터 스탯 조회"""
    character = Character.objects.get_or_create(
        user=request.user,
        defaults={'name': f"{request.user.nickname}의 캐릭터"}
    )[0]
    
    stats = {
        'stamina': character.stamina,
        'strength': character.strength,
        'mental': character.mental,
        'endurance': character.endurance,
        'cardio': character.cardio,
        'flexibility': character.flexibility,
        'nutrition': character.nutrition,
        'recovery': character.recovery,
        'total_stats': character.total_stats,
        'health_score': character.health_score,
        'level': character.level,
        'experience_points': character.experience_points,
    }
    
    return Response(stats)


class StatHistoryListView(generics.ListAPIView):
    """스탯 변화 기록 조회"""
    serializer_class = StatHistorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        character = Character.objects.get_or_create(
            user=self.request.user,
            defaults={'name': f"{self.request.user.nickname}의 캐릭터"}
        )[0]
        return StatHistory.objects.filter(character=character)


class UserAchievementListView(generics.ListAPIView):
    """사용자 업적 조회"""
    serializer_class = UserAchievementSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserAchievement.objects.filter(user=self.request.user)