from rest_framework import generics, permissions, status, viewsets
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from django.db.models import Count, Avg, Q
from django.utils import timezone
from datetime import timedelta
from .models import (
    Character, StatHistory, UserAchievement,
    NutritionLog, Supplement, UserSupplement, SupplementLog
)
from .serializers import (
    CharacterSerializer, StatHistorySerializer, UserAchievementSerializer,
    NutritionLogSerializer, SupplementSerializer, UserSupplementSerializer,
    SupplementLogSerializer, NutritionStatsSerializer
)


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


class NutritionLogViewSet(viewsets.ModelViewSet):
    """영양 기록 관리"""
    serializer_class = NutritionLogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = NutritionLog.objects.filter(user=self.request.user)
        
        # 날짜 필터링
        date = self.request.query_params.get('date')
        if date:
            queryset = queryset.filter(date=date)
        
        # 식사 타입 필터링
        meal_type = self.request.query_params.get('meal_type')
        if meal_type:
            queryset = queryset.filter(meal_type=meal_type)
        
        return queryset.order_by('-date', '-created_at')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def stats(self, request):
        """영양 통계 조회"""
        user = request.user
        now = timezone.now()
        
        # 기간별 통계
        daily_logs = NutritionLog.objects.filter(
            user=user,
            date=now.date()
        )
        
        weekly_logs = NutritionLog.objects.filter(
            user=user,
            date__gte=now.date() - timedelta(days=7)
        )
        
        monthly_logs = NutritionLog.objects.filter(
            user=user,
            date__gte=now.date() - timedelta(days=30)
        )
        
        all_logs = NutritionLog.objects.filter(user=user)
        
        # 평균 점수 계산
        daily_avg = sum(log.nutrition_score for log in daily_logs) / len(daily_logs) if daily_logs else 0
        weekly_avg = sum(log.nutrition_score for log in weekly_logs) / len(weekly_logs) if weekly_logs else 0
        monthly_avg = sum(log.nutrition_score for log in monthly_logs) / len(monthly_logs) if monthly_logs else 0
        
        # 품질별 통계
        quality_stats = all_logs.values('meal_quality').annotate(count=Count('id'))
        quality_counts = {item['meal_quality']: item['count'] for item in quality_stats}
        
        # 체크리스트 통계
        total_logs = all_logs.count()
        vegetables_count = all_logs.filter(included_vegetables=True).count()
        protein_count = all_logs.filter(included_protein=True).count()
        grains_count = all_logs.filter(included_grains=True).count()
        proper_portion_count = all_logs.filter(proper_portion=True).count()
        
        stats_data = {
            'daily_average_score': round(daily_avg, 2),
            'weekly_average_score': round(weekly_avg, 2),
            'monthly_average_score': round(monthly_avg, 2),
            'total_logs': total_logs,
            'excellent_meals': quality_counts.get('excellent', 0),
            'good_meals': quality_counts.get('good', 0),
            'fair_meals': quality_counts.get('fair', 0),
            'poor_meals': quality_counts.get('poor', 0),
            'vegetables_percentage': round((vegetables_count / total_logs * 100) if total_logs else 0, 2),
            'protein_percentage': round((protein_count / total_logs * 100) if total_logs else 0, 2),
            'grains_percentage': round((grains_count / total_logs * 100) if total_logs else 0, 2),
            'proper_portion_percentage': round((proper_portion_count / total_logs * 100) if total_logs else 0, 2),
        }
        
        serializer = NutritionStatsSerializer(stats_data)
        return Response(serializer.data)


class SupplementViewSet(viewsets.ReadOnlyModelViewSet):
    """영양제 마스터 데이터 조회"""
    serializer_class = SupplementSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Supplement.objects.filter(is_active=True)
        
        # 카테고리 필터링
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category=category)
        
        # 검색
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) | Q(description__icontains=search)
            )
        
        return queryset.order_by('category', 'name')


class UserSupplementViewSet(viewsets.ModelViewSet):
    """사용자 영양제 관리"""
    serializer_class = UserSupplementSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = UserSupplement.objects.filter(user=self.request.user)
        
        # 활성/비활성 필터링
        is_active = self.request.query_params.get('is_active')
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')
        
        return queryset.select_related('supplement').order_by('-is_active', 'supplement__name')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class SupplementLogViewSet(viewsets.ModelViewSet):
    """영양제 복용 기록 관리"""
    serializer_class = SupplementLogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # 사용자의 영양제만 조회 가능
        user_supplements = UserSupplement.objects.filter(user=self.request.user)
        queryset = SupplementLog.objects.filter(user_supplement__in=user_supplements)
        
        # 날짜 필터링
        date = self.request.query_params.get('date')
        if date:
            queryset = queryset.filter(taken_at__date=date)
        
        # 영양제 필터링
        supplement_id = self.request.query_params.get('supplement_id')
        if supplement_id:
            queryset = queryset.filter(user_supplement__supplement_id=supplement_id)
        
        return queryset.select_related(
            'user_supplement__supplement'
        ).order_by('-taken_at')

    def perform_create(self, serializer):
        # 사용자의 영양제인지 확인
        user_supplement_id = serializer.validated_data['user_supplement_id']
        user_supplement = UserSupplement.objects.get(
            id=user_supplement_id,
            user=self.request.user
        )
        serializer.save(user_supplement=user_supplement)