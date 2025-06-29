// API Response Types
export interface ApiResponse<T> {
  data?: T;
  message?: string;
  error?: string;
}

// User Types
export interface User {
  id: number;
  email: string;
  username: string;
  nickname: string;
  birth_date?: string;
  gender?: 'male' | 'female' | 'other';
  height?: number;
  weight?: number;
  activity_level: 'sedentary' | 'light' | 'moderate' | 'active' | 'very_active';
  timezone: string;
  created_at: string;
  updated_at: string;
}

export interface UserProfile {
  bio?: string;
  avatar?: string;
  notification_enabled: boolean;
  email_notification: boolean;
  push_notification: boolean;
  privacy_level: 'public' | 'friends' | 'private';
}

// Character Types
export interface Character {
  id: number;
  user: number;
  name: string;
  level: number;
  experience_points: number;
  stamina: number;
  strength: number;
  mental: number;
  endurance: number;
  cardio: number;
  flexibility: number;
  nutrition: number;
  recovery: number;
  gold: number;
  gems: number;
  skin: string;
  avatar_url?: string;
  total_stats: number;
  health_score: number;
  created_at: string;
  updated_at: string;
}

export interface StatHistory {
  id: number;
  character: number;
  stat_type: 'stamina' | 'strength' | 'mental' | 'endurance' | 'cardio' | 'flexibility' | 'nutrition' | 'recovery';
  old_value: number;
  new_value: number;
  change_reason: string;
  created_at: string;
}

export interface Achievement {
  id: number;
  name: string;
  description: string;
  icon: string;
  category: 'quest' | 'stats' | 'social' | 'special';
  requirement_type: 'quest_count' | 'streak' | 'stat_level' | 'level' | 'special';
  requirement_value: number;
  reward_gold: number;
  reward_gems: number;
  reward_experience: number;
  is_active: boolean;
  created_at: string;
}

export interface UserAchievement {
  id: number;
  user: number;
  achievement: Achievement;
  achieved_at: string;
  is_displayed: boolean;
}

// Quest Types
export interface QuestTemplate {
  id: number;
  title: string;
  description: string;
  category: 'morning' | 'work' | 'evening' | 'night' | 'weekly' | 'challenge';
  target_stats: Record<string, number>;
  base_experience: number;
  base_gold: number;
  base_gems: number;
  difficulty: 'easy' | 'normal' | 'hard' | 'expert';
  duration_minutes: number;
  required_level: number;
  weather_condition: 'any' | 'sunny' | 'cloudy' | 'rainy' | 'snowy';
  time_of_day: 'any' | 'morning' | 'afternoon' | 'evening' | 'night';
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface Quest {
  id: number;
  user: number;
  template: QuestTemplate;
  custom_title?: string;
  custom_description?: string;
  target_stats: Record<string, number>;
  experience_reward: number;
  gold_reward: number;
  gems_reward: number;
  status: 'assigned' | 'in_progress' | 'completed' | 'failed' | 'expired';
  assigned_date: string;
  start_date?: string;
  due_date: string;
  completed_date?: string;
  progress_percentage: number;
  requires_verification: boolean;
  verification_image?: string;
  verification_note?: string;
  title: string;
  description: string;
  created_at: string;
  updated_at: string;
}

export interface QuestCompletion {
  id: number;
  quest: Quest;
  completion_time: string;
  actual_duration?: string;
  difficulty_rating?: number;
  satisfaction_rating?: number;
  user_notes?: string;
}

export interface DailyStreak {
  id: number;
  user: number;
  current_streak: number;
  longest_streak: number;
  last_completion_date?: string;
  streak_start_date?: string;
}

// Nutrition Types
export interface NutritionLog {
  id: number;
  user: number;
  date: string;
  meal_type: 'breakfast' | 'lunch' | 'dinner' | 'snack';
  meal_type_display: string;
  meal_quality: 'excellent' | 'good' | 'fair' | 'poor';
  meal_quality_display: string;
  included_vegetables: boolean;
  included_protein: boolean;
  included_grains: boolean;
  proper_portion: boolean;
  notes?: string;
  calories_estimate?: number;
  meal_image?: string;
  nutrition_score: number;
  created_at: string;
  updated_at: string;
}

export interface Supplement {
  id: number;
  name: string;
  category: 'vitamin' | 'mineral' | 'protein' | 'omega' | 'herb' | 'other';
  description: string;
  default_dosage: string;
  precautions?: string;
  user_count: number;
  is_active: boolean;
  created_at: string;
}

export interface UserSupplement {
  id: number;
  supplement: Supplement;
  dosage: string;
  frequency: 'daily' | 'weekly' | 'as_needed';
  morning: boolean;
  afternoon: boolean;
  evening: boolean;
  schedule_display: string;
  personal_notes?: string;
  is_active: boolean;
  started_date: string;
  ended_date?: string;
  created_at: string;
  updated_at: string;
}

export interface SupplementLog {
  id: number;
  supplement_name: string;
  taken_at: string;
  dosage_taken: string;
  time_of_day: 'morning' | 'afternoon' | 'evening' | 'night';
  time_of_day_display: string;
  notes?: string;
  side_effects?: string;
  created_at: string;
}

export interface NutritionStats {
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

// Auth Types
export interface LoginCredentials {
  email: string;
  password: string;
}

export interface RegisterData {
  email: string;
  username: string;
  nickname: string;
  password: string;
  password_confirm: string;
  gender?: 'male' | 'female' | 'other';
  height?: number;
  weight?: number;
  activity_level: 'sedentary' | 'light' | 'moderate' | 'active' | 'very_active';
}

export interface AuthTokens {
  access: string;
  refresh: string;
}

export interface AuthResponse {
  message: string;
  user: User;
  tokens: AuthTokens;
}

// UI Types
export type LoadingState = 'idle' | 'loading' | 'succeeded' | 'failed';

export interface PaginatedResponse<T> {
  count: number;
  next?: string;
  previous?: string;
  results: T[];
}

// Stat Colors and Icons
export const STAT_CONFIG = {
  stamina: { color: 'bg-red-500', icon: '💪', name: '체력', description: '기초 체력, 에너지 관리' },
  strength: { color: 'bg-orange-500', icon: '🏋️', name: '근력', description: '근육 운동, 저항 운동' },
  mental: { color: 'bg-purple-500', icon: '🧠', name: '정신력', description: '스트레스 관리, 집중력' },
  endurance: { color: 'bg-blue-500', icon: '🏃', name: '지구력', description: '유산소, 지속력' },
  cardio: { color: 'bg-pink-500', icon: '❤️', name: '심폐', description: '심혈관 건강' },
  flexibility: { color: 'bg-green-500', icon: '🤸', name: '유연성', description: '스트레칭, 요가' },
  nutrition: { color: 'bg-yellow-500', icon: '🥗', name: '영양', description: '균형잡힌 식단' },
  recovery: { color: 'bg-indigo-500', icon: '😴', name: '회복', description: '수면, 휴식' },
} as const;

export type StatType = keyof typeof STAT_CONFIG;