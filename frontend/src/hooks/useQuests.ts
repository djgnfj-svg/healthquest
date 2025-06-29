import { useState, useEffect } from 'react';
import { questAPI } from '../services/api';
import type { Quest, DailyStreak, LoadingState } from '../types';

export function useQuests() {
  const [quests, setQuests] = useState<Quest[]>([]);
  const [dailyQuests, setDailyQuests] = useState<{
    date: string;
    quests: Quest[];
    total_count: number;
    completed_count: number;
  } | null>(null);
  const [streak, setStreak] = useState<DailyStreak | null>(null);
  const [loading, setLoading] = useState<LoadingState>('idle');
  const [error, setError] = useState<string | null>(null);

  const fetchQuests = async (status?: string) => {
    setLoading('loading');
    setError(null);
    
    try {
      const response = await questAPI.getQuests(status);
      setQuests(response.data.results);
      setLoading('succeeded');
    } catch (err: any) {
      setError(err.response?.data?.error || '퀘스트를 불러올 수 없습니다.');
      setLoading('failed');
    }
  };

  const fetchDailyQuests = async () => {
    try {
      const response = await questAPI.getDailyQuests();
      setDailyQuests(response.data);
    } catch (err: any) {
      setError(err.response?.data?.error || '오늘의 퀘스트를 불러올 수 없습니다.');
    }
  };

  const fetchStreak = async () => {
    try {
      const response = await questAPI.getStreak();
      setStreak(response.data);
    } catch (err: any) {
      setError(err.response?.data?.error || '연속 기록을 불러올 수 없습니다.');
    }
  };

  const startQuest = async (questId: number) => {
    try {
      const response = await questAPI.startQuest(questId);
      // Update the quest in the local state
      setQuests(prev => prev.map(q => 
        q.id === questId ? response.data.quest : q
      ));
      return response.data;
    } catch (err: any) {
      setError(err.response?.data?.error || '퀘스트 시작에 실패했습니다.');
      throw err;
    }
  };

  const completeQuest = async (questId: number, data: any) => {
    try {
      const response = await questAPI.completeQuest(questId, data);
      // Update the quest in the local state
      setQuests(prev => prev.map(q => 
        q.id === questId ? response.data.quest : q
      ));
      setStreak(response.data.streak);
      return response.data;
    } catch (err: any) {
      setError(err.response?.data?.error || '퀘스트 완료에 실패했습니다.');
      throw err;
    }
  };

  useEffect(() => {
    fetchQuests();
    fetchDailyQuests();
    fetchStreak();
  }, []);

  return {
    quests,
    dailyQuests,
    streak,
    loading,
    error,
    fetchQuests,
    fetchDailyQuests,
    startQuest,
    completeQuest,
    refetch: fetchQuests,
  };
}