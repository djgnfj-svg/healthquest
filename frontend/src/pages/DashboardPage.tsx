import React from 'react';
import { Link } from 'react-router-dom';
import { Card } from '../components/ui/Card';
import { Button } from '../components/ui/Button';
import { LoadingSpinner } from '../components/ui/LoadingSpinner';
import { CharacterOverview } from '../components/character/CharacterOverview';
import { StatCard } from '../components/character/StatCard';
import { useCharacter } from '../hooks/useCharacter';
import { useQuests } from '../hooks/useQuests';
import { STAT_CONFIG, type StatType } from '../types';

export function DashboardPage() {
  const { character, loading: characterLoading } = useCharacter();
  const { dailyQuests, streak, loading: questsLoading } = useQuests();

  if (characterLoading === 'loading' || questsLoading === 'loading') {
    return (
      <div className="flex items-center justify-center min-h-96">
        <LoadingSpinner size="lg" />
      </div>
    );
  }

  if (!character) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-500">캐릭터 정보를 불러올 수 없습니다.</p>
      </div>
    );
  }

  const todayQuests = dailyQuests?.quests || [];
  const completedToday = dailyQuests?.completed_count || 0;
  const totalToday = dailyQuests?.total_count || 0;

  return (
    <div className="space-y-8">
      {/* Welcome Header */}
      <div className="text-center">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">
          안녕하세요, {character.name}님! 👋
        </h1>
        <p className="text-gray-600">
          오늘도 건강한 모험을 시작해볼까요?
        </p>
      </div>

      {/* Character Overview */}
      <CharacterOverview character={character} />

      {/* Quick Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Daily Progress */}
        <Card>
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-gray-900">오늘의 진행</h3>
            <span className="text-2xl">🎯</span>
          </div>
          <div className="text-center">
            <div className="text-3xl font-bold text-primary-600 mb-1">
              {completedToday} / {totalToday}
            </div>
            <p className="text-sm text-gray-500">완료한 퀘스트</p>
          </div>
          <div className="mt-4">
            <Link to="/quests">
              <Button className="w-full" size="sm">
                퀘스트 보기
              </Button>
            </Link>
          </div>
        </Card>

        {/* Streak */}
        <Card>
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-gray-900">연속 완료</h3>
            <span className="text-2xl">🔥</span>
          </div>
          <div className="text-center">
            <div className="text-3xl font-bold text-orange-600 mb-1">
              {streak?.current_streak || 0}일
            </div>
            <p className="text-sm text-gray-500">
              최고 기록: {streak?.longest_streak || 0}일
            </p>
          </div>
          {(streak?.current_streak || 0) > 0 && (
            <div className="mt-4 text-center">
              <span className="text-sm text-green-600 font-medium">
                잘하고 있어요! 🎉
              </span>
            </div>
          )}
        </Card>

        {/* Health Score */}
        <Card>
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-gray-900">건강 점수</h3>
            <span className="text-2xl">❤️</span>
          </div>
          <div className="text-center">
            <div className="text-3xl font-bold text-red-600 mb-1">
              {character.health_score}
            </div>
            <p className="text-sm text-gray-500">/ 100</p>
          </div>
          <div className="mt-4">
            <div className="w-full bg-gray-200 rounded-full h-2">
              <div 
                className="bg-red-600 h-2 rounded-full transition-all duration-300"
                style={{ width: `${character.health_score}%` }}
              />
            </div>
          </div>
        </Card>
      </div>

      {/* Character Stats */}
      <div>
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-2xl font-bold text-gray-900">캐릭터 스탯</h2>
          <Link to="/character">
            <Button variant="ghost" size="sm">
              상세 보기 →
            </Button>
          </Link>
        </div>
        
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {Object.keys(STAT_CONFIG).map((statKey) => {
            const statType = statKey as StatType;
            const value = character[statType];
            return (
              <StatCard
                key={statType}
                statType={statType}
                value={value}
                maxValue={100}
              />
            );
          })}
        </div>
      </div>

      {/* Today's Quests Preview */}
      {todayQuests.length > 0 && (
        <div>
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-2xl font-bold text-gray-900">오늘의 퀘스트</h2>
            <Link to="/quests">
              <Button variant="ghost" size="sm">
                모두 보기 →
              </Button>
            </Link>
          </div>
          
          <div className="space-y-4">
            {todayQuests.slice(0, 3).map((quest) => (
              <Card key={quest.id} variant="quest" className="p-4">
                <div className="flex items-center justify-between">
                  <div className="flex-1">
                    <h3 className="font-semibold text-gray-900 mb-1">
                      {quest.title}
                    </h3>
                    <p className="text-sm text-gray-600 line-clamp-2">
                      {quest.description}
                    </p>
                    <div className="flex items-center space-x-4 mt-2">
                      <span className="text-xs px-2 py-1 bg-primary-100 text-primary-700 rounded-full">
                        {quest.template.category}
                      </span>
                      <span className="text-xs text-gray-500">
                        {quest.template.difficulty}
                      </span>
                    </div>
                  </div>
                  <div className="flex items-center space-x-2 ml-4">
                    <span className="text-sm text-green-600">
                      +{quest.experience_reward} EXP
                    </span>
                    <span className="text-lg">
                      {quest.status === 'completed' ? '✅' : 
                       quest.status === 'in_progress' ? '🔄' : '⏳'}
                    </span>
                  </div>
                </div>
              </Card>
            ))}
          </div>
        </div>
      )}

      {/* Quick Actions */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Card className="text-center p-8">
          <div className="text-4xl mb-4">🎯</div>
          <h3 className="text-xl font-semibold text-gray-900 mb-2">
            새로운 퀘스트
          </h3>
          <p className="text-gray-600 mb-4">
            건강한 습관을 만들어보세요
          </p>
          <Link to="/quests">
            <Button>퀘스트 시작하기</Button>
          </Link>
        </Card>

        <Card className="text-center p-8">
          <div className="text-4xl mb-4">⚔️</div>
          <h3 className="text-xl font-semibold text-gray-900 mb-2">
            길드 활동
          </h3>
          <p className="text-gray-600 mb-4">
            친구들과 함께 도전하세요
          </p>
          <Link to="/guilds">
            <Button variant="secondary">길드 보기</Button>
          </Link>
        </Card>
      </div>
    </div>
  );
}