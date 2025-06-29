import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { Button } from '../components/ui/Button';
import { Input } from '../components/ui/Input';
import { Card } from '../components/ui/Card';
import type { RegisterData } from '../types';

export function RegisterPage() {
  const [formData, setFormData] = useState<RegisterData>({
    email: '',
    username: '',
    nickname: '',
    password: '',
    password_confirm: '',
    gender: undefined,
    height: undefined,
    weight: undefined,
    activity_level: 'moderate',
  });
  
  const [errors, setErrors] = useState<Partial<RegisterData>>({});
  const { register, loading, error } = useAuth();
  const navigate = useNavigate();

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value, type } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'number' ? (value ? parseFloat(value) : undefined) : value,
    }));
    
    // Clear error when user starts typing
    if (errors[name as keyof RegisterData]) {
      setErrors(prev => ({ ...prev, [name]: undefined }));
    }
  };

  const validateForm = () => {
    const newErrors: Partial<RegisterData> = {};
    
    if (!formData.email.trim()) {
      newErrors.email = '이메일을 입력해주세요.';
    } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
      newErrors.email = '올바른 이메일 형식이 아닙니다.';
    }
    
    if (!formData.username.trim()) {
      newErrors.username = '사용자명을 입력해주세요.';
    } else if (formData.username.length < 3) {
      newErrors.username = '사용자명은 3자 이상이어야 합니다.';
    }
    
    if (!formData.nickname.trim()) {
      newErrors.nickname = '닉네임을 입력해주세요.';
    }
    
    if (!formData.password) {
      newErrors.password = '비밀번호를 입력해주세요.';
    } else if (formData.password.length < 8) {
      newErrors.password = '비밀번호는 8자 이상이어야 합니다.';
    }
    
    if (!formData.password_confirm) {
      newErrors.password_confirm = '비밀번호 확인을 입력해주세요.';
    } else if (formData.password !== formData.password_confirm) {
      newErrors.password_confirm = '비밀번호가 일치하지 않습니다.';
    }
    
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!validateForm()) return;
    
    try {
      await register(formData);
      navigate('/');
    } catch (error) {
      // Error is handled by the auth context
    }
  };

  return (
    <div className="min-h-screen bg-gradient-bg flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        <div className="text-center">
          <h1 className="text-4xl font-bold text-white mb-2">🎮 HealthQuest</h1>
          <h2 className="text-xl text-white/90">건강한 모험을 시작하세요</h2>
        </div>

        <Card className="mt-8">
          <div className="text-center mb-6">
            <h3 className="text-2xl font-bold text-gray-900">회원가입</h3>
            <p className="text-gray-600 mt-2">새로운 모험가가 되어보세요</p>
          </div>

          {error && (
            <div className="bg-danger-50 border border-danger-200 rounded-lg p-4 mb-6">
              <p className="text-danger-700 text-sm">{error}</p>
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-4">
            <Input
              label="이메일"
              name="email"
              type="email"
              value={formData.email}
              onChange={handleChange}
              error={errors.email}
              placeholder="이메일을 입력하세요"
              autoComplete="email"
            />

            <div className="grid grid-cols-2 gap-4">
              <Input
                label="사용자명"
                name="username"
                value={formData.username}
                onChange={handleChange}
                error={errors.username}
                placeholder="사용자명"
                autoComplete="username"
              />

              <Input
                label="닉네임"
                name="nickname"
                value={formData.nickname}
                onChange={handleChange}
                error={errors.nickname}
                placeholder="닉네임"
              />
            </div>

            <div className="grid grid-cols-2 gap-4">
              <Input
                label="비밀번호"
                name="password"
                type="password"
                value={formData.password}
                onChange={handleChange}
                error={errors.password}
                placeholder="비밀번호"
                autoComplete="new-password"
              />

              <Input
                label="비밀번호 확인"
                name="password_confirm"
                type="password"
                value={formData.password_confirm}
                onChange={handleChange}
                error={errors.password_confirm}
                placeholder="비밀번호 확인"
                autoComplete="new-password"
              />
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  성별
                </label>
                <select
                  name="gender"
                  value={formData.gender || ''}
                  onChange={handleChange}
                  className="w-full rounded-lg border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500"
                >
                  <option value="">선택 안함</option>
                  <option value="male">남성</option>
                  <option value="female">여성</option>
                  <option value="other">기타</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  활동 수준
                </label>
                <select
                  name="activity_level"
                  value={formData.activity_level}
                  onChange={handleChange}
                  className="w-full rounded-lg border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500"
                >
                  <option value="sedentary">좌식생활</option>
                  <option value="light">가벼운 활동</option>
                  <option value="moderate">보통 활동</option>
                  <option value="active">활발한 활동</option>
                  <option value="very_active">매우 활발한 활동</option>
                </select>
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <Input
                label="키 (cm)"
                name="height"
                type="number"
                value={formData.height || ''}
                onChange={handleChange}
                placeholder="170"
                min="100"
                max="250"
              />

              <Input
                label="몸무게 (kg)"
                name="weight"
                type="number"
                value={formData.weight || ''}
                onChange={handleChange}
                placeholder="70"
                min="30"
                max="200"
                step="0.1"
              />
            </div>

            <Button
              type="submit"
              className="w-full"
              loading={loading === 'loading'}
              disabled={loading === 'loading'}
            >
              회원가입
            </Button>
          </form>

          <div className="mt-6 text-center">
            <p className="text-gray-600">
              이미 계정이 있으신가요?{' '}
              <Link to="/login" className="text-primary-600 hover:text-primary-500 font-medium">
                로그인
              </Link>
            </p>
          </div>
        </Card>
      </div>
    </div>
  );
}