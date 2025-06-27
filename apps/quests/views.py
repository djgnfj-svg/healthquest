from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta
from .models import Quest, QuestTemplate, QuestCompletion, DailyStreak
from .serializers import (
    QuestSerializer, QuestTemplateSerializer, QuestCompletionSerializer,
    DailyStreakSerializer, QuestStartSerializer, QuestCompleteSerializer
)


class QuestListView(generics.ListAPIView):
    """사용자 퀘스트 목록 조회"""
    serializer_class = QuestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        status_filter = self.request.query_params.get('status', None)
        queryset = Quest.objects.filter(user=self.request.user)
        
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        return queryset.order_by('-created_at')


class QuestDetailView(generics.RetrieveAPIView):
    """퀘스트 상세 조회"""
    serializer_class = QuestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Quest.objects.filter(user=self.request.user)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def start_quest_view(request, quest_id):
    """퀘스트 시작"""
    try:
        quest = Quest.objects.get(id=quest_id, user=request.user)
        
        if quest.status != 'assigned':
            return Response(
                {'error': '시작할 수 없는 퀘스트입니다.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        quest.start_quest()
        
        return Response({
            'message': '퀘스트를 시작했습니다.',
            'quest': QuestSerializer(quest).data
        })
        
    except Quest.DoesNotExist:
        return Response(
            {'error': '퀘스트를 찾을 수 없습니다.'},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def complete_quest_view(request, quest_id):
    """퀘스트 완료"""
    try:
        quest = Quest.objects.get(id=quest_id, user=request.user)
        
        if quest.status != 'in_progress':
            return Response(
                {'error': '완료할 수 없는 퀘스트입니다.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = QuestCompleteSerializer(data=request.data)
        if serializer.is_valid():
            # 검증 정보 저장
            if serializer.validated_data.get('verification_image'):
                quest.verification_image = serializer.validated_data['verification_image']
            if serializer.validated_data.get('verification_note'):
                quest.verification_note = serializer.validated_data['verification_note']
            
            quest.complete_quest()
            
            # 완료 기록 생성
            completion_data = {
                'difficulty_rating': serializer.validated_data.get('difficulty_rating'),
                'satisfaction_rating': serializer.validated_data.get('satisfaction_rating'),
                'user_notes': serializer.validated_data.get('user_notes'),
            }
            
            if quest.start_date:
                completion_data['actual_duration'] = timezone.now() - quest.start_date
            
            QuestCompletion.objects.create(
                quest=quest,
                **completion_data
            )
            
            # 연속 완료 기록 업데이트
            streak, created = DailyStreak.objects.get_or_create(user=request.user)
            streak.update_streak(timezone.now().date())
            
            return Response({
                'message': '퀘스트를 완료했습니다!',
                'quest': QuestSerializer(quest).data,
                'streak': DailyStreakSerializer(streak).data
            })
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    except Quest.DoesNotExist:
        return Response(
            {'error': '퀘스트를 찾을 수 없습니다.'},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def daily_quests_view(request):
    """오늘의 퀘스트 조회"""
    today = timezone.now().date()
    tomorrow = today + timedelta(days=1)
    
    quests = Quest.objects.filter(
        user=request.user,
        due_date__date=today,
        status__in=['assigned', 'in_progress']
    )
    
    return Response({
        'date': today,
        'quests': QuestSerializer(quests, many=True).data,
        'total_count': quests.count(),
        'completed_count': quests.filter(status='completed').count()
    })


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_streak_view(request):
    """사용자 연속 완료 기록 조회"""
    streak, created = DailyStreak.objects.get_or_create(user=request.user)
    return Response(DailyStreakSerializer(streak).data)


class QuestCompletionHistoryView(generics.ListAPIView):
    """퀘스트 완료 기록 조회"""
    serializer_class = QuestCompletionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return QuestCompletion.objects.filter(
            quest__user=self.request.user
        ).order_by('-completion_time')


class QuestTemplateListView(generics.ListAPIView):
    """퀘스트 템플릿 목록 (관리자용)"""
    serializer_class = QuestTemplateSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = QuestTemplate.objects.filter(is_active=True)