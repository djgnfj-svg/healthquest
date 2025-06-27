from django.urls import path
from . import views

urlpatterns = [
    path('', views.GuildListView.as_view(), name='guild_list'),
    path('create/', views.create_guild_view, name='create_guild'),
    path('join/', views.join_guild_view, name='join_guild'),
    path('my/', views.my_guild_view, name='my_guild'),
    path('<int:pk>/', views.GuildDetailView.as_view(), name='guild_detail'),
    path('<int:guild_id>/leave/', views.leave_guild_view, name='leave_guild'),
    path('<int:guild_id>/members/', views.GuildMembersView.as_view(), name='guild_members'),
    path('<int:guild_id>/quests/', views.GuildQuestListView.as_view(), name='guild_quests'),
    path('<int:guild_id>/messages/', views.GuildMessageListView.as_view(), name='guild_messages'),
]