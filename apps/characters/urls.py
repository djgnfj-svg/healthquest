from django.urls import path
from . import views

urlpatterns = [
    path('', views.CharacterDetailView.as_view(), name='character_detail'),
    path('stats/', views.character_stats_view, name='character_stats'),
    path('stats-history/', views.StatHistoryListView.as_view(), name='stat_history'),
    path('achievements/', views.UserAchievementListView.as_view(), name='user_achievements'),
]