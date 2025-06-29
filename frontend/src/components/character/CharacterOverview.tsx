import React from 'react';
import { Card } from '../ui/Card';
import { ProgressBar } from '../ui/ProgressBar';
import type { Character } from '../../types';

interface CharacterOverviewProps {
  character: Character;
}

export function CharacterOverview({ character }: CharacterOverviewProps) {
  const nextLevelExp = Math.floor(100 * (character.level ** 1.2));
  const currentLevelExp = character.experience_points;
  const expProgress = (currentLevelExp / nextLevelExp) * 100;

  return (
    <Card className="bg-gradient-to-r from-primary-500 to-primary-600 text-white">
      <div className="flex items-center space-x-6">
        {/* Character Avatar */}
        <div className="flex-shrink-0">
          <div className="w-24 h-24 bg-white/20 rounded-full flex items-center justify-center">
            {character.avatar_url ? (
              <img 
                src={character.avatar_url} 
                alt={character.name}
                className="w-full h-full rounded-full object-cover"
              />
            ) : (
              <span className="text-4xl">👤</span>
            )}
          </div>
        </div>

        {/* Character Info */}
        <div className="flex-1">
          <h2 className="text-2xl font-bold mb-1">{character.name}</h2>
          <p className="text-primary-100 mb-4">레벨 {character.level} 모험가</p>
          
          {/* Experience Progress */}
          <div className="mb-4">
            <div className="flex justify-between items-center mb-1">
              <span className="text-sm font-medium">경험치</span>
              <span className="text-sm">{currentLevelExp} / {nextLevelExp}</span>
            </div>
            <div className="w-full bg-white/20 rounded-full h-2">
              <div 
                className="bg-white h-2 rounded-full transition-all duration-300"
                style={{ width: `${Math.min(100, expProgress)}%` }}
              />
            </div>
          </div>

          {/* Stats Summary */}
          <div className="grid grid-cols-3 gap-4 text-center">
            <div>
              <div className="text-2xl font-bold">{character.total_stats}</div>
              <div className="text-sm text-primary-100">총 스탯</div>
            </div>
            <div>
              <div className="text-2xl font-bold">{character.health_score}</div>
              <div className="text-sm text-primary-100">건강 점수</div>
            </div>
            <div className="flex items-center justify-center space-x-2">
              <span className="text-lg">💰</span>
              <div>
                <div className="text-lg font-bold">{character.gold}</div>
                <div className="text-xs text-primary-100">골드</div>
              </div>
              <span className="text-lg">💎</span>
              <div>
                <div className="text-lg font-bold">{character.gems}</div>
                <div className="text-xs text-primary-100">젬</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </Card>
  );
}