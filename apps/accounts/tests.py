from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from .models import UserProfile

User = get_user_model()


class UserModelTest(TestCase):
    """사용자 모델 테스트"""
    
    def setUp(self):
        self.user_data = {
            'email': 'test@example.com',
            'username': 'testuser',
            'nickname': '테스트유저',
            'password': 'testpass123',
            'height': 175.0,
            'weight': 70.0,
            'activity_level': 'moderate'
        }
    
    def test_create_user(self):
        """사용자 생성 테스트"""
        user = User.objects.create_user(**self.user_data)
        
        self.assertEqual(user.email, self.user_data['email'])
        self.assertEqual(user.nickname, self.user_data['nickname'])
        self.assertEqual(user.height, self.user_data['height'])
        self.assertEqual(user.weight, self.user_data['weight'])
        self.assertEqual(user.activity_level, self.user_data['activity_level'])
        self.assertTrue(user.check_password(self.user_data['password']))
    
    def test_create_superuser(self):
        """슈퍼유저 생성 테스트"""
        user = User.objects.create_superuser(
            email='admin@example.com',
            username='admin',
            nickname='관리자',
            password='admin123'
        )
        
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
    
    def test_user_str_method(self):
        """사용자 __str__ 메서드 테스트"""
        user = User.objects.create_user(**self.user_data)
        expected_str = f"{user.nickname} ({user.email})"
        self.assertEqual(str(user), expected_str)


class UserProfileModelTest(TestCase):
    """사용자 프로필 모델 테스트"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            nickname='테스트유저',
            password='testpass123'
        )
    
    def test_create_user_profile(self):
        """사용자 프로필 생성 테스트"""
        profile = UserProfile.objects.create(
            user=self.user,
            bio='테스트 바이오',
            notification_enabled=True,
            email_notification=False,
            privacy_level='friends'
        )
        
        self.assertEqual(profile.user, self.user)
        self.assertEqual(profile.bio, '테스트 바이오')
        self.assertTrue(profile.notification_enabled)
        self.assertFalse(profile.email_notification)
        self.assertEqual(profile.privacy_level, 'friends')
    
    def test_user_profile_str_method(self):
        """사용자 프로필 __str__ 메서드 테스트"""
        profile = UserProfile.objects.create(user=self.user)
        expected_str = f"{self.user.nickname}의 프로필"
        self.assertEqual(str(profile), expected_str)


class AuthAPITest(APITestCase):
    """인증 API 테스트"""
    
    def setUp(self):
        self.client = Client()
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')
        self.profile_url = reverse('profile')
        self.user_detail_url = reverse('user_detail')
        
        self.user_data = {
            'email': 'test@example.com',
            'username': 'testuser',
            'nickname': '테스트유저',
            'password': 'testpass123',
            'password_confirm': 'testpass123',
            'gender': 'male',
            'height': 175,
            'weight': 70,
            'activity_level': 'moderate'
        }
    
    def test_user_registration(self):
        """사용자 회원가입 테스트"""
        response = self.client.post(
            self.register_url,
            data=self.user_data,
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('message', response.json())
        self.assertIn('user', response.json())
        self.assertIn('tokens', response.json())
        
        # 사용자가 실제로 생성되었는지 확인
        user = User.objects.get(email=self.user_data['email'])
        self.assertEqual(user.nickname, self.user_data['nickname'])
    
    def test_user_registration_password_mismatch(self):
        """비밀번호 불일치 회원가입 테스트"""
        self.user_data['password_confirm'] = 'different_password'
        
        response = self.client.post(
            self.register_url,
            data=self.user_data,
            content_type='application/json'
        )
        
        self.assertNotEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_user_login(self):
        """사용자 로그인 테스트"""
        # 먼저 사용자 생성
        user = User.objects.create_user(
            email=self.user_data['email'],
            username=self.user_data['username'],
            nickname=self.user_data['nickname'],
            password=self.user_data['password']
        )
        
        login_data = {
            'email': self.user_data['email'],
            'password': self.user_data['password']
        }
        
        response = self.client.post(
            self.login_url,
            data=login_data,
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.json())
        self.assertIn('user', response.json())
        self.assertIn('tokens', response.json())
    
    def test_user_login_invalid_credentials(self):
        """잘못된 인증 정보로 로그인 테스트"""
        login_data = {
            'email': 'wrong@example.com',
            'password': 'wrongpassword'
        }
        
        response = self.client.post(
            self.login_url,
            data=login_data,
            content_type='application/json'
        )
        
        self.assertNotEqual(response.status_code, status.HTTP_200_OK)
    
    def test_get_current_user(self):
        """현재 사용자 정보 조회 테스트"""
        # 사용자 생성 및 로그인
        user = User.objects.create_user(
            email=self.user_data['email'],
            username=self.user_data['username'],
            nickname=self.user_data['nickname'],
            password=self.user_data['password']
        )
        
        self.client.force_authenticate(user=user)
        
        response = self.client.get(self.user_detail_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['email'], user.email)
        self.assertEqual(response.json()['nickname'], user.nickname)
    
    def test_update_profile(self):
        """프로필 업데이트 테스트"""
        user = User.objects.create_user(
            email=self.user_data['email'],
            username=self.user_data['username'],
            nickname=self.user_data['nickname'],
            password=self.user_data['password']
        )
        
        self.client.force_authenticate(user=user)
        
        update_data = {
            'nickname': '새로운닉네임',
            'height': 180,
            'weight': 75
        }
        
        response = self.client.put(
            self.profile_url,
            data=update_data,
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # 사용자 정보가 실제로 업데이트되었는지 확인
        user.refresh_from_db()
        self.assertEqual(user.nickname, update_data['nickname'])
        self.assertEqual(user.height, update_data['height'])
        self.assertEqual(user.weight, update_data['weight'])


class UserAuthenticationTest(TestCase):
    """사용자 인증 관련 테스트"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            nickname='테스트유저',
            password='testpass123'
        )
    
    def test_user_authentication(self):
        """사용자 인증 테스트"""
        # 올바른 비밀번호
        self.assertTrue(self.user.check_password('testpass123'))
        
        # 잘못된 비밀번호
        self.assertFalse(self.user.check_password('wrongpassword'))
    
    def test_email_unique_constraint(self):
        """이메일 유니크 제약 조건 테스트"""
        with self.assertRaises(Exception):
            User.objects.create_user(
                email='test@example.com',  # 이미 존재하는 이메일
                username='testuser2',
                nickname='테스트유저2',
                password='testpass123'
            )
    
    def test_nickname_unique_constraint(self):
        """닉네임 유니크 제약 조건 테스트"""
        with self.assertRaises(Exception):
            User.objects.create_user(
                email='test2@example.com',
                username='testuser2',
                nickname='테스트유저',  # 이미 존재하는 닉네임
                password='testpass123'
            )