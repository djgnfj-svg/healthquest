import type { 
  User, 
  Character, 
  Quest, 
  DailyStreak, 
  AuthResponse 
} from '../../types';

// Mock user data
export const mockUser: User = {
  id: 1,
  email: 'test@example.com',
  username: 'testuser',
  nickname: '테스트유저',
  birth_date: '1990-01-01',
  gender: 'male',
  height: 175,
  weight: 70,
  activity_level: 'moderate',
  timezone: 'Asia/Seoul',
  created_at: '2024-01-01T00:00:00Z',
  updated_at: '2024-01-01T00:00:00Z',
};

// Mock character data
export const mockCharacter: Character = {
  id: 1,
  user: 1,
  name: '테스트 캐릭터',
  level: 5,
  experience_points: 150,
  stamina: 25,
  strength: 20,
  mental: 18,
  endurance: 22,
  cardio: 19,
  flexibility: 16,
  nutrition: 21,
  recovery: 17,
  gold: 500,
  gems: 50,
  skin: 'default',
  avatar_url: null,
  total_stats: 158,
  health_score: 79,
  created_at: '2024-01-01T00:00:00Z',
  updated_at: '2024-01-01T00:00:00Z',
};

// Mock quest data
export const mockQuest: Quest = {
  id: 1,
  user: 1,
  template: {
    id: 1,
    title: '아침 스트레칭',
    description: '10분간 전신 스트레칭을 해보세요',
    category: 'morning',
    target_stats: { flexibility: 2, recovery: 1 },
    base_experience: 20,
    base_gold: 10,
    base_gems: 0,
    difficulty: 'easy',
    duration_minutes: 10,
    required_level: 1,
    weather_condition: 'any',
    time_of_day: 'morning',
    is_active: true,
    created_at: '2024-01-01T00:00:00Z',
    updated_at: '2024-01-01T00:00:00Z',
  },
  custom_title: '',
  custom_description: '',
  target_stats: { flexibility: 2, recovery: 1 },
  experience_reward: 20,
  gold_reward: 10,
  gems_reward: 0,
  status: 'assigned',
  assigned_date: '2024-01-01T00:00:00Z',
  start_date: null,
  due_date: '2024-01-01T23:59:59Z',
  completed_date: null,
  progress_percentage: 0,
  requires_verification: false,
  verification_image: null,
  verification_note: '',
  title: '아침 스트레칭',
  description: '10분간 전신 스트레칭을 해보세요',
  created_at: '2024-01-01T00:00:00Z',
  updated_at: '2024-01-01T00:00:00Z',
};

// Mock daily streak data
export const mockDailyStreak: DailyStreak = {
  id: 1,
  user: 1,
  current_streak: 5,
  longest_streak: 12,
  last_completion_date: '2024-01-01',
  streak_start_date: '2023-12-28',
};

// Mock auth response
export const mockAuthResponse: AuthResponse = {
  message: '로그인 성공',
  user: mockUser,
  tokens: {
    access: 'mock-access-token',
    refresh: 'mock-refresh-token',
  },
};

// Mock API functions
export const mockAPI = {
  // Auth API
  authAPI: {
    register: vi.fn().mockResolvedValue({ data: mockAuthResponse }),
    login: vi.fn().mockResolvedValue({ data: mockAuthResponse }),
    logout: vi.fn().mockResolvedValue({ data: { message: '로그아웃 되었습니다.' } }),
    getCurrentUser: vi.fn().mockResolvedValue({ data: mockUser }),
    updateProfile: vi.fn().mockResolvedValue({ data: mockUser }),
  },

  // Character API
  characterAPI: {
    getCharacter: vi.fn().mockResolvedValue({ data: mockCharacter }),
    updateCharacter: vi.fn().mockResolvedValue({ data: mockCharacter }),
    getStats: vi.fn().mockResolvedValue({ data: mockCharacter }),
    getStatsHistory: vi.fn().mockResolvedValue({ 
      data: { 
        count: 0, 
        results: [] 
      } 
    }),
    getAchievements: vi.fn().mockResolvedValue({ 
      data: { 
        count: 0, 
        results: [] 
      } 
    }),
  },

  // Quest API
  questAPI: {
    getQuests: vi.fn().mockResolvedValue({ 
      data: { 
        count: 1, 
        results: [mockQuest] 
      } 
    }),
    getQuest: vi.fn().mockResolvedValue({ data: mockQuest }),
    startQuest: vi.fn().mockResolvedValue({ 
      data: { 
        message: '퀘스트를 시작했습니다.', 
        quest: { ...mockQuest, status: 'in_progress' } 
      } 
    }),
    completeQuest: vi.fn().mockResolvedValue({ 
      data: { 
        message: '퀘스트를 완료했습니다!', 
        quest: { ...mockQuest, status: 'completed' },
        streak: mockDailyStreak
      } 
    }),
    getDailyQuests: vi.fn().mockResolvedValue({ 
      data: {
        date: '2024-01-01',
        quests: [mockQuest],
        total_count: 1,
        completed_count: 0
      } 
    }),
    getStreak: vi.fn().mockResolvedValue({ data: mockDailyStreak }),
    getCompletions: vi.fn().mockResolvedValue({ 
      data: { 
        count: 0, 
        results: [] 
      } 
    }),
  },

  // Nutrition API
  nutritionAPI: {
    getNutritionLogs: vi.fn().mockResolvedValue({ 
      data: { 
        count: 0, 
        results: [] 
      } 
    }),
    createNutritionLog: vi.fn().mockResolvedValue({ 
      data: {
        id: 1,
        meal_type: 'breakfast',
        meal_quality: 'good',
        nutrition_score: 85,
        created_at: new Date().toISOString()
      }
    }),
    getNutritionStats: vi.fn().mockResolvedValue({ 
      data: {
        daily_average_score: 75.0,
        weekly_average_score: 78.5,
        monthly_average_score: 80.2,
        total_logs: 15,
        excellent_meals: 3,
        good_meals: 8,
        fair_meals: 3,
        poor_meals: 1,
        vegetables_percentage: 80.0,
        protein_percentage: 75.0,
        grains_percentage: 70.0,
        proper_portion_percentage: 85.0
      }
    }),
    getSupplements: vi.fn().mockResolvedValue({ 
      data: { 
        count: 0, 
        results: [] 
      } 
    }),
    getUserSupplements: vi.fn().mockResolvedValue({ 
      data: { 
        count: 0, 
        results: [] 
      } 
    }),
    addUserSupplement: vi.fn().mockResolvedValue({ data: null }),
    getSupplementLogs: vi.fn().mockResolvedValue({ 
      data: { 
        count: 0, 
        results: [] 
      } 
    }),
    logSupplement: vi.fn().mockResolvedValue({ data: null }),
  },
};