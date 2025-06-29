import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { Button } from '../components/ui/Button';
import { Input } from '../components/ui/Input';
import { Card } from '../components/ui/Card';

export function LoginPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [errors, setErrors] = useState<{ email?: string; password?: string }>({});
  
  const { login, loading, error } = useAuth();
  const navigate = useNavigate();

  const validateForm = () => {
    const newErrors: { email?: string; password?: string } = {};
    
    if (!email.trim()) {
      newErrors.email = '이메일을 입력해주세요.';
    } else if (!/\S+@\S+\.\S+/.test(email)) {
      newErrors.email = '올바른 이메일 형식이 아닙니다.';
    }
    
    if (!password.trim()) {
      newErrors.password = '비밀번호를 입력해주세요.';
    }
    
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!validateForm()) return;
    
    try {
      await login(email, password);
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
          <h2 className="text-xl text-white/90">건강한 삶을 위한 RPG 여정</h2>
        </div>

        <Card className="mt-8">
          <div className="text-center mb-6">
            <h3 className="text-2xl font-bold text-gray-900">로그인</h3>
            <p className="text-gray-600 mt-2">계정에 로그인하여 모험을 계속하세요</p>
          </div>

          {error && (
            <div className="bg-danger-50 border border-danger-200 rounded-lg p-4 mb-6">
              <p className="text-danger-700 text-sm">{error}</p>
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-6">
            <Input
              label="이메일"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              error={errors.email}
              placeholder="이메일을 입력하세요"
              autoComplete="email"
            />

            <Input
              label="비밀번호"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              error={errors.password}
              placeholder="비밀번호를 입력하세요"
              autoComplete="current-password"
            />

            <Button
              type="submit"
              className="w-full"
              loading={loading === 'loading'}
              disabled={loading === 'loading'}
            >
              로그인
            </Button>
          </form>

          <div className="mt-6 text-center">
            <p className="text-gray-600">
              계정이 없으신가요?{' '}
              <Link to="/register" className="text-primary-600 hover:text-primary-500 font-medium">
                회원가입
              </Link>
            </p>
          </div>
        </Card>

        <div className="text-center">
          <p className="text-white/70 text-sm">
            건강 습관을 게임처럼 재미있게 만들어보세요! 💪
          </p>
        </div>
      </div>
    </div>
  );
}