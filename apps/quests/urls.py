from django.urls import path
from . import views

urlpatterns = [
    path('', views.QuestListView.as_view(), name='quest_list'),
    path('<int:pk>/', views.QuestDetailView.as_view(), name='quest_detail'),
    path('<int:quest_id>/start/', views.start_quest_view, name='start_quest'),
    path('<int:quest_id>/complete/', views.complete_quest_view, name='complete_quest'),
    path('daily/', views.daily_quests_view, name='daily_quests'),
    path('streak/', views.user_streak_view, name='user_streak'),
    path('completions/', views.QuestCompletionHistoryView.as_view(), name='quest_completions'),
    path('templates/', views.QuestTemplateListView.as_view(), name='quest_templates'),
]