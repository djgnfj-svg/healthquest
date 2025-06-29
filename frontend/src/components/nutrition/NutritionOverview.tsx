import React, { useState, useEffect } from 'react';
import { Card } from '../ui/Card';
import { Button } from '../ui/Button';
import { ProgressBar } from '../ui/ProgressBar';
import { LoadingSpinner } from '../ui/LoadingSpinner';
import api from '../../services/api';

interface NutritionLog {
  id: number;
  date: string;
  meal_type: string;
  meal_type_display: string;
  meal_quality: string;
  meal_quality_display: string;
  included_vegetables: boolean;
  included_protein: boolean;
  included_grains: boolean;
  proper_portion: boolean;
  nutrition_score: number;
  notes?: string;
  calories_estimate?: number;
}

interface NutritionStats {
  daily_average_score: number;
  weekly_average_score: number;
  monthly_average_score: number;
  total_logs: number;
  excellent_meals: number;
  good_meals: number;
  fair_meals: number;
  poor_meals: number;
  vegetables_percentage: number;
  protein_percentage: number;
  grains_percentage: number;
  proper_portion_percentage: number;
}

export function NutritionOverview() {
  const [stats, setStats] = useState<NutritionStats | null>(null);
  const [recentLogs, setRecentLogs] = useState<NutritionLog[]>([]);
  const [loading, setLoading] = useState(true);
  const [showAddForm, setShowAddForm] = useState(false);

  useEffect(() => {
    fetchNutritionData();
  }, []);

  const fetchNutritionData = async () => {
    try {
      setLoading(true);
      
      // 영양 통계 조회
      const statsResponse = await api.get('/characters/nutrition-logs/stats/');
      setStats(statsResponse.data);
      
      // 최근 영양 기록 조회 (최대 5개)
      const logsResponse = await api.get('/characters/nutrition-logs/?limit=5');
      setRecentLogs(logsResponse.data.results || []);
      
    } catch (error) {
      console.error('영양 데이터 조회 실패:', error);
    } finally {
      setLoading(false);
    }
  };

  const getScoreColor = (score: number) => {
    if (score >= 80) return 'text-green-600';
    if (score >= 60) return 'text-yellow-600';
    return 'text-red-600';
  };

  const getScoreBgColor = (score: number) => {
    if (score >= 80) return 'bg-green-100';
    if (score >= 60) return 'bg-yellow-100';
    return 'bg-red-100';
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center py-12">
        <LoadingSpinner size="lg" />
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* 헤더 */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">영양 관리</h1>
          <p className="text-gray-600 mt-1">건강한 식습관을 기록하고 관리하세요</p>
        </div>
        <Button onClick={() => setShowAddForm(true)}>
          🍽️ 식사 기록 추가
        </Button>
      </div>

      {/* 영양 통계 카드들 */}
      {stats && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {/* 오늘 평균 점수 */}
          <Card className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">오늘 평균</p>
                <p className={`text-2xl font-bold ${getScoreColor(stats.daily_average_score)}`}>
                  {stats.daily_average_score.toFixed(1)}
                </p>
              </div>
              <div className={`w-12 h-12 rounded-full flex items-center justify-center ${getScoreBgColor(stats.daily_average_score)}`}>
                <span className="text-xl">📊</span>
              </div>
            </div>
          </Card>

          {/* 주간 평균 점수 */}
          <Card className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">주간 평균</p>
                <p className={`text-2xl font-bold ${getScoreColor(stats.weekly_average_score)}`}>
                  {stats.weekly_average_score.toFixed(1)}
                </p>
              </div>
              <div className={`w-12 h-12 rounded-full flex items-center justify-center ${getScoreBgColor(stats.weekly_average_score)}`}>
                <span className="text-xl">📈</span>
              </div>
            </div>
          </Card>

          {/* 월간 평균 점수 */}
          <Card className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">월간 평균</p>
                <p className={`text-2xl font-bold ${getScoreColor(stats.monthly_average_score)}`}>
                  {stats.monthly_average_score.toFixed(1)}
                </p>
              </div>
              <div className={`w-12 h-12 rounded-full flex items-center justify-center ${getScoreBgColor(stats.monthly_average_score)}`}>
                <span className="text-xl">📅</span>
              </div>
            </div>
          </Card>

          {/* 총 기록 수 */}
          <Card className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">총 기록</p>
                <p className="text-2xl font-bold text-gray-900">{stats.total_logs}</p>
              </div>
              <div className="w-12 h-12 rounded-full bg-blue-100 flex items-center justify-center">
                <span className="text-xl">📝</span>
              </div>
            </div>
          </Card>
        </div>
      )}

      {/* 영양소별 달성률 */}
      {stats && (
        <Card className="p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">영양소별 달성률</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <div className="flex justify-between items-center mb-2">
                <span className="text-sm font-medium text-gray-600">🥬 채소 포함</span>
                <span className="text-sm font-bold text-gray-900">{stats.vegetables_percentage.toFixed(1)}%</span>
              </div>
              <ProgressBar 
                progress={stats.vegetables_percentage} 
                className="mb-4"
                color={stats.vegetables_percentage >= 70 ? 'green' : stats.vegetables_percentage >= 40 ? 'yellow' : 'red'}
              />
            </div>

            <div>
              <div className="flex justify-between items-center mb-2">
                <span className="text-sm font-medium text-gray-600">🥩 단백질 포함</span>
                <span className="text-sm font-bold text-gray-900">{stats.protein_percentage.toFixed(1)}%</span>
              </div>
              <ProgressBar 
                progress={stats.protein_percentage} 
                className="mb-4"
                color={stats.protein_percentage >= 70 ? 'green' : stats.protein_percentage >= 40 ? 'yellow' : 'red'}
              />
            </div>

            <div>
              <div className="flex justify-between items-center mb-2">
                <span className="text-sm font-medium text-gray-600">🌾 곡물 포함</span>
                <span className="text-sm font-bold text-gray-900">{stats.grains_percentage.toFixed(1)}%</span>
              </div>
              <ProgressBar 
                progress={stats.grains_percentage} 
                className="mb-4"
                color={stats.grains_percentage >= 70 ? 'green' : stats.grains_percentage >= 40 ? 'yellow' : 'red'}
              />
            </div>

            <div>
              <div className="flex justify-between items-center mb-2">
                <span className="text-sm font-medium text-gray-600">⚖️ 적절한 양</span>
                <span className="text-sm font-bold text-gray-900">{stats.proper_portion_percentage.toFixed(1)}%</span>
              </div>
              <ProgressBar 
                progress={stats.proper_portion_percentage} 
                className="mb-4"
                color={stats.proper_portion_percentage >= 70 ? 'green' : stats.proper_portion_percentage >= 40 ? 'yellow' : 'red'}
              />
            </div>
          </div>
        </Card>
      )}

      {/* 최근 식사 기록 */}
      <Card className="p-6">
        <div className="flex justify-between items-center mb-4">
          <h3 className="text-lg font-semibold text-gray-900">최근 식사 기록</h3>
          <Button variant="ghost" size="sm">
            전체 보기
          </Button>
        </div>

        {recentLogs.length === 0 ? (
          <div className="text-center py-8">
            <span className="text-4xl mb-2 block">🍽️</span>
            <p className="text-gray-600">아직 식사 기록이 없습니다.</p>
            <p className="text-gray-500 text-sm">첫 번째 식사를 기록해보세요!</p>
          </div>
        ) : (
          <div className="space-y-3">
            {recentLogs.map((log) => (
              <div key={log.id} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                <div className="flex items-center space-x-3">
                  <div className={`w-10 h-10 rounded-full flex items-center justify-center ${getScoreBgColor(log.nutrition_score)}`}>
                    <span className={`font-bold ${getScoreColor(log.nutrition_score)}`}>
                      {log.nutrition_score}
                    </span>
                  </div>
                  <div>
                    <p className="font-medium text-gray-900">
                      {log.meal_type_display} - {log.meal_quality_display}
                    </p>
                    <p className="text-sm text-gray-600">{log.date}</p>
                  </div>
                </div>
                <div className="flex space-x-1">
                  {log.included_vegetables && <span>🥬</span>}
                  {log.included_protein && <span>🥩</span>}
                  {log.included_grains && <span>🌾</span>}
                  {log.proper_portion && <span>⚖️</span>}
                </div>
              </div>
            ))}
          </div>
        )}
      </Card>

      {/* 식사 기록 추가 모달 (간단한 플레이스홀더) */}
      {showAddForm && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 max-w-md w-full mx-4">
            <h3 className="text-lg font-semibold mb-4">식사 기록 추가</h3>
            <p className="text-gray-600 mb-4">상세한 식사 기록 폼이 곧 구현될 예정입니다!</p>
            <div className="flex justify-end space-x-2">
              <Button variant="ghost" onClick={() => setShowAddForm(false)}>
                취소
              </Button>
              <Button onClick={() => setShowAddForm(false)}>
                확인
              </Button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}