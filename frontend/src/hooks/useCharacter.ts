import { useState, useEffect } from 'react';
import { characterAPI } from '../services/api';
import type { Character, LoadingState } from '../types';

export function useCharacter() {
  const [character, setCharacter] = useState<Character | null>(null);
  const [loading, setLoading] = useState<LoadingState>('idle');
  const [error, setError] = useState<string | null>(null);

  const fetchCharacter = async () => {
    setLoading('loading');
    setError(null);
    
    try {
      const response = await characterAPI.getCharacter();
      setCharacter(response.data);
      setLoading('succeeded');
    } catch (err: any) {
      setError(err.response?.data?.error || '캐릭터 정보를 불러올 수 없습니다.');
      setLoading('failed');
    }
  };

  const updateCharacter = async (data: Partial<Character>) => {
    try {
      const response = await characterAPI.updateCharacter(data);
      setCharacter(response.data);
      return response.data;
    } catch (err: any) {
      setError(err.response?.data?.error || '캐릭터 정보 업데이트에 실패했습니다.');
      throw err;
    }
  };

  useEffect(() => {
    fetchCharacter();
  }, []);

  return {
    character,
    loading,
    error,
    refetch: fetchCharacter,
    updateCharacter,
  };
}