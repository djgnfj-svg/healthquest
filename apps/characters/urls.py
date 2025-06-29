from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# ViewSet용 라우터
router = DefaultRouter()
router.register(r'nutrition-logs', views.NutritionLogViewSet, basename='nutrition-logs')
router.register(r'supplements', views.SupplementViewSet, basename='supplements')
router.register(r'user-supplements', views.UserSupplementViewSet, basename='user-supplements')
router.register(r'supplement-logs', views.SupplementLogViewSet, basename='supplement-logs')

urlpatterns = [
    path('', views.CharacterDetailView.as_view(), name='character_detail'),
    path('stats/', views.character_stats_view, name='character_stats'),
    path('stats-history/', views.StatHistoryListView.as_view(), name='stat_history'),
    path('achievements/', views.UserAchievementListView.as_view(), name='user_achievements'),
    
    # 영양 관련 API
    path('', include(router.urls)),
]