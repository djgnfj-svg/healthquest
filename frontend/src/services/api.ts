import axios, { AxiosResponse } from 'axios';
import type {
  User,
  Character,
  Quest,
  AuthResponse,
  LoginCredentials,
  RegisterData,
  DailyStreak,
  QuestCompletion,
  UserAchievement,
  StatHistory,
  PaginatedResponse,
} from '../types';

const API_BASE_URL = 'http://localhost:8000/api';

// Create axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add auth token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle token refresh
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      
      const refreshToken = localStorage.getItem('refresh_token');
      if (refreshToken) {
        try {
          const response = await axios.post(`${API_BASE_URL}/auth/token/refresh/`, {
            refresh: refreshToken,
          });
          
          const { access } = response.data;
          localStorage.setItem('access_token', access);
          api.defaults.headers.Authorization = `Bearer ${access}`;
          
          return api(originalRequest);
        } catch (refreshError) {
          // Refresh failed, redirect to login
          localStorage.removeItem('access_token');
          localStorage.removeItem('refresh_token');
          window.location.href = '/login';
        }
      }
    }
    
    return Promise.reject(error);
  }
);

// Auth API
export const authAPI = {
  register: (data: RegisterData): Promise<AxiosResponse<AuthResponse>> =>
    api.post('/auth/register/', data),
    
  login: (credentials: LoginCredentials): Promise<AxiosResponse<AuthResponse>> =>
    api.post('/auth/login/', credentials),
    
  logout: (): Promise<AxiosResponse<{ message: string }>> => {
    const refreshToken = localStorage.getItem('refresh_token');
    return api.post('/auth/logout/', { refresh: refreshToken });
  },
  
  getCurrentUser: (): Promise<AxiosResponse<User>> =>
    api.get('/auth/me/'),
    
  updateProfile: (data: Partial<User>): Promise<AxiosResponse<User>> =>
    api.put('/auth/profile/', data),
};

// Character API
export const characterAPI = {
  getCharacter: (): Promise<AxiosResponse<Character>> =>
    api.get('/characters/'),
    
  updateCharacter: (data: Partial<Character>): Promise<AxiosResponse<Character>> =>
    api.put('/characters/', data),
    
  getStats: (): Promise<AxiosResponse<Character>> =>
    api.get('/characters/stats/'),
    
  getStatsHistory: (): Promise<AxiosResponse<PaginatedResponse<StatHistory>>> =>
    api.get('/characters/stats-history/'),
    
  getAchievements: (): Promise<AxiosResponse<PaginatedResponse<UserAchievement>>> =>
    api.get('/characters/achievements/'),
};

// Quest API
export const questAPI = {
  getQuests: (status?: string): Promise<AxiosResponse<PaginatedResponse<Quest>>> => {
    const params = status ? { status } : {};
    return api.get('/quests/', { params });
  },
  
  getQuest: (id: number): Promise<AxiosResponse<Quest>> =>
    api.get(`/quests/${id}/`),
    
  startQuest: (id: number): Promise<AxiosResponse<{ message: string; quest: Quest }>> =>
    api.post(`/quests/${id}/start/`),
    
  completeQuest: (
    id: number,
    data: {
      verification_image?: File;
      verification_note?: string;
      difficulty_rating?: number;
      satisfaction_rating?: number;
      user_notes?: string;
    }
  ): Promise<AxiosResponse<{ message: string; quest: Quest; streak: DailyStreak }>> => {
    const formData = new FormData();
    if (data.verification_image) {
      formData.append('verification_image', data.verification_image);
    }
    if (data.verification_note) {
      formData.append('verification_note', data.verification_note);
    }
    if (data.difficulty_rating) {
      formData.append('difficulty_rating', data.difficulty_rating.toString());
    }
    if (data.satisfaction_rating) {
      formData.append('satisfaction_rating', data.satisfaction_rating.toString());
    }
    if (data.user_notes) {
      formData.append('user_notes', data.user_notes);
    }
    
    return api.post(`/quests/${id}/complete/`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
  },
  
  getDailyQuests: (): Promise<AxiosResponse<{
    date: string;
    quests: Quest[];
    total_count: number;
    completed_count: number;
  }>> =>
    api.get('/quests/daily/'),
    
  getStreak: (): Promise<AxiosResponse<DailyStreak>> =>
    api.get('/quests/streak/'),
    
  getCompletions: (): Promise<AxiosResponse<PaginatedResponse<QuestCompletion>>> =>
    api.get('/quests/completions/'),
};

// Nutrition API
export const nutritionAPI = {
  getNutritionLogs: (params?: { date?: string; meal_type?: string }): Promise<AxiosResponse<PaginatedResponse<any>>> =>
    api.get('/characters/nutrition-logs/', { params }),
    
  createNutritionLog: (data: {
    meal_type: string;
    meal_quality: string;
    included_vegetables?: boolean;
    included_protein?: boolean;
    included_grains?: boolean;
    proper_portion?: boolean;
    notes?: string;
    calories_estimate?: number;
    meal_image?: File;
  }): Promise<AxiosResponse<any>> => {
    const formData = new FormData();
    Object.entries(data).forEach(([key, value]) => {
      if (value !== undefined) {
        if (value instanceof File) {
          formData.append(key, value);
        } else {
          formData.append(key, value.toString());
        }
      }
    });
    
    return api.post('/characters/nutrition-logs/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
  },
    
  getNutritionStats: (): Promise<AxiosResponse<any>> =>
    api.get('/characters/nutrition-logs/stats/'),
    
  getSupplements: (params?: { category?: string; search?: string }): Promise<AxiosResponse<PaginatedResponse<any>>> =>
    api.get('/characters/supplements/', { params }),
    
  getUserSupplements: (params?: { is_active?: boolean }): Promise<AxiosResponse<PaginatedResponse<any>>> =>
    api.get('/characters/user-supplements/', { params }),
    
  addUserSupplement: (data: {
    supplement_id: number;
    dosage: string;
    frequency: string;
    morning?: boolean;
    afternoon?: boolean;
    evening?: boolean;
    personal_notes?: string;
  }): Promise<AxiosResponse<any>> =>
    api.post('/characters/user-supplements/', data),
    
  getSupplementLogs: (params?: { date?: string; supplement_id?: number }): Promise<AxiosResponse<PaginatedResponse<any>>> =>
    api.get('/characters/supplement-logs/', { params }),
    
  logSupplement: (data: {
    user_supplement_id: number;
    taken_at?: string;
    dosage_taken: string;
    time_of_day: string;
    notes?: string;
    side_effects?: string;
  }): Promise<AxiosResponse<any>> =>
    api.post('/characters/supplement-logs/', data),
};

// Utility functions
export const setAuthTokens = (access: string, refresh: string) => {
  localStorage.setItem('access_token', access);
  localStorage.setItem('refresh_token', refresh);
  api.defaults.headers.Authorization = `Bearer ${access}`;
};

export const clearAuthTokens = () => {
  localStorage.removeItem('access_token');
  localStorage.removeItem('refresh_token');
  delete api.defaults.headers.Authorization;
};

export const isAuthenticated = (): boolean => {
  return !!localStorage.getItem('access_token');
};

export default api;