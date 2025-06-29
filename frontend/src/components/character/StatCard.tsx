import React from 'react';
import { Card } from '../ui/Card';
import { ProgressBar } from '../ui/ProgressBar';
import { STAT_CONFIG, type StatType } from '../../types';

interface StatCardProps {
  statType: StatType;
  value: number;
  maxValue?: number;
  showProgress?: boolean;
}

export function StatCard({ statType, value, maxValue = 100, showProgress = true }: StatCardProps) {
  const config = STAT_CONFIG[statType];
  
  return (
    <Card variant="hover" className="p-4">
      <div className="flex items-center space-x-3 mb-3">
        <div className={`w-10 h-10 rounded-lg ${config.color} flex items-center justify-center text-white text-lg`}>
          {config.icon}
        </div>
        <div>
          <h3 className="font-semibold text-gray-900">{config.name}</h3>
          <p className="text-sm text-gray-500">{config.description}</p>
        </div>
      </div>
      
      <div className="flex items-center justify-between mb-2">
        <span className="text-2xl font-bold text-gray-900">{value}</span>
        <span className="text-sm text-gray-500">/ {maxValue}</span>
      </div>
      
      {showProgress && (
        <ProgressBar 
          value={value} 
          max={maxValue} 
          color={value >= maxValue * 0.8 ? 'success' : value >= maxValue * 0.5 ? 'primary' : 'warning'}
        />
      )}
    </Card>
  );
}