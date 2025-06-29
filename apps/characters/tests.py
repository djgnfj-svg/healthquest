from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Character, Achievement, UserAchievement, StatHistory

User = get_user_model()


class CharacterModelTest(TestCase):
    """캐릭터 모델 테스트"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            nickname='테스트유저',
            password='testpass123'
        )
    
    def test_create_character(self):
        """캐릭터 생성 테스트"""
        character = Character.objects.create(
            user=self.user,
            name='테스트 캐릭터'
        )
        
        self.assertEqual(character.user, self.user)
        self.assertEqual(character.name, '테스트 캐릭터')
        self.assertEqual(character.level, 1)
        self.assertEqual(character.experience_points, 0)
        
        # 모든 스탯이 기본값 10으로 설정되었는지 확인
        self.assertEqual(character.stamina, 10)
        self.assertEqual(character.strength, 10)
        self.assertEqual(character.mental, 10)
        self.assertEqual(character.endurance, 10)
        self.assertEqual(character.cardio, 10)
        self.assertEqual(character.flexibility, 10)
        self.assertEqual(character.nutrition, 10)
        self.assertEqual(character.recovery, 10)
        
        # 기본 화폐
        self.assertEqual(character.gold, 100)
        self.assertEqual(character.gems, 0)
    
    def test_character_str_method(self):
        """캐릭터 __str__ 메서드 테스트"""
        character = Character.objects.create(
            user=self.user,
            name='테스트 캐릭터'
        )
        expected_str = f"{self.user.nickname}의 테스트 캐릭터 (Lv.1)"
        self.assertEqual(str(character), expected_str)
    
    def test_total_stats_property(self):
        """총 스탯 계산 프로퍼티 테스트"""
        character = Character.objects.create(
            user=self.user,
            name='테스트 캐릭터',
            stamina=15,
            strength=20,
            mental=10,
            endurance=12,
            cardio=18,
            flexibility=8,
            nutrition=14,
            recovery=16
        )
        
        expected_total = 15 + 20 + 10 + 12 + 18 + 8 + 14 + 16
        self.assertEqual(character.total_stats, expected_total)
    
    def test_health_score_property(self):
        """건강 점수 계산 프로퍼티 테스트"""
        character = Character.objects.create(
            user=self.user,
            name='테스트 캐릭터',
            stamina=20,
            strength=20,
            mental=20,
            endurance=20,
            cardio=20,
            flexibility=20,
            nutrition=20,
            recovery=20
        )
        
        # 총 스탯 160 -> 건강 점수 80
        expected_health_score = min(100, 160 // 2)
        self.assertEqual(character.health_score, expected_health_score)
        
        # 건강 점수는 최대 100
        character.stamina = 100
        character.strength = 100
        character.save()
        self.assertEqual(character.health_score, 100)
    
    def test_gain_experience(self):
        """경험치 획득 및 레벨업 테스트"""
        character = Character.objects.create(
            user=self.user,
            name='테스트 캐릭터'
        )
        
        # 경험치 50 획득 (레벨업 안됨)
        character.gain_experience(50)
        self.assertEqual(character.experience_points, 50)
        self.assertEqual(character.level, 1)
        
        # 경험치 추가 획득으로 레벨업
        character.gain_experience(60)  # 총 110, 레벨업 필요 경험치 100
        self.assertEqual(character.level, 2)
        self.assertEqual(character.experience_points, 10)  # 레벨업 후 남은 경험치
    
    def test_distribute_stat_points(self):
        """스탯 포인트 분배 테스트"""
        character = Character.objects.create(
            user=self.user,
            name='테스트 캐릭터'
        )
        
        initial_total = character.total_stats
        character.distribute_stat_points(8)  # 8포인트 분배
        
        # 모든 스탯이 1씩 증가했는지 확인 (8개 스탯)
        self.assertEqual(character.total_stats, initial_total + 8)


class AchievementModelTest(TestCase):
    """업적 모델 테스트"""
    
    def test_create_achievement(self):
        """업적 생성 테스트"""
        achievement = Achievement.objects.create(
            name='첫 걸음',
            description='첫 번째 퀘스트를 완료하세요',
            icon='🏆',
            category='quest',
            requirement_type='quest_count',
            requirement_value=1,
            reward_gold=100,
            reward_gems=10,
            reward_experience=50
        )
        
        self.assertEqual(achievement.name, '첫 걸음')
        self.assertEqual(achievement.category, 'quest')
        self.assertEqual(achievement.requirement_value, 1)
        self.assertEqual(achievement.reward_gold, 100)
    
    def test_achievement_str_method(self):
        """업적 __str__ 메서드 테스트"""
        achievement = Achievement.objects.create(
            name='첫 걸음',
            description='첫 번째 퀘스트를 완료하세요',
            requirement_type='quest_count',
            requirement_value=1
        )
        self.assertEqual(str(achievement), '첫 걸음')


class UserAchievementModelTest(TestCase):
    """사용자 업적 모델 테스트"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            nickname='테스트유저',
            password='testpass123'
        )
        
        self.achievement = Achievement.objects.create(
            name='첫 걸음',
            description='첫 번째 퀘스트를 완료하세요',
            requirement_type='quest_count',
            requirement_value=1
        )
    
    def test_create_user_achievement(self):
        """사용자 업적 생성 테스트"""
        user_achievement = UserAchievement.objects.create(
            user=self.user,
            achievement=self.achievement,
            is_displayed=True
        )
        
        self.assertEqual(user_achievement.user, self.user)
        self.assertEqual(user_achievement.achievement, self.achievement)
        self.assertTrue(user_achievement.is_displayed)
    
    def test_user_achievement_str_method(self):
        """사용자 업적 __str__ 메서드 테스트"""
        user_achievement = UserAchievement.objects.create(
            user=self.user,
            achievement=self.achievement
        )
        expected_str = f"{self.user.nickname} - {self.achievement.name}"
        self.assertEqual(str(user_achievement), expected_str)
    
    def test_unique_together_constraint(self):
        """사용자-업적 유니크 제약 조건 테스트"""
        UserAchievement.objects.create(
            user=self.user,
            achievement=self.achievement
        )
        
        # 같은 사용자가 같은 업적을 중복으로 획득할 수 없음
        with self.assertRaises(Exception):
            UserAchievement.objects.create(
                user=self.user,
                achievement=self.achievement
            )


class StatHistoryModelTest(TestCase):
    """스탯 변화 기록 모델 테스트"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            nickname='테스트유저',
            password='testpass123'
        )
        
        self.character = Character.objects.create(
            user=self.user,
            name='테스트 캐릭터'
        )
    
    def test_create_stat_history(self):
        """스탯 변화 기록 생성 테스트"""
        stat_history = StatHistory.objects.create(
            character=self.character,
            stat_type='stamina',
            old_value=10,
            new_value=12,
            change_reason='퀘스트 완료: 체력 단련'
        )
        
        self.assertEqual(stat_history.character, self.character)
        self.assertEqual(stat_history.stat_type, 'stamina')
        self.assertEqual(stat_history.old_value, 10)
        self.assertEqual(stat_history.new_value, 12)
        self.assertEqual(stat_history.change_reason, '퀘스트 완료: 체력 단련')
    
    def test_stat_history_str_method(self):
        """스탯 변화 기록 __str__ 메서드 테스트"""
        stat_history = StatHistory.objects.create(
            character=self.character,
            stat_type='stamina',
            old_value=10,
            new_value=12,
            change_reason='퀘스트 완료'
        )
        expected_str = f"{self.character.name} stamina: 10 → 12"
        self.assertEqual(str(stat_history), expected_str)


class CharacterAPITest(APITestCase):
    """캐릭터 API 테스트"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            nickname='테스트유저',
            password='testpass123'
        )
        
        self.character_url = reverse('characters:character-detail')
        self.stats_url = reverse('characters:character-stats')
        self.stats_history_url = reverse('characters:stats-history')
        self.achievements_url = reverse('characters:achievements')
    
    def test_get_character_creates_if_not_exists(self):
        """캐릭터가 없으면 자동 생성하는 테스트"""
        self.client.force_authenticate(user=self.user)
        
        response = self.client.get(self.character_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # 캐릭터가 자동으로 생성되었는지 확인
        character = Character.objects.get(user=self.user)
        self.assertEqual(character.name, f"{self.user.nickname}의 캐릭터")
    
    def test_get_character_stats(self):
        """캐릭터 스탯 조회 테스트"""
        character = Character.objects.create(
            user=self.user,
            name='테스트 캐릭터',
            stamina=15,
            strength=20
        )
        
        self.client.force_authenticate(user=self.user)
        
        response = self.client.get(self.stats_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        
        self.assertEqual(data['stamina'], 15)
        self.assertEqual(data['strength'], 20)
        self.assertEqual(data['level'], 1)
        self.assertIn('total_stats', data)
        self.assertIn('health_score', data)
    
    def test_update_character(self):
        """캐릭터 정보 업데이트 테스트"""
        character = Character.objects.create(
            user=self.user,
            name='테스트 캐릭터'
        )
        
        self.client.force_authenticate(user=self.user)
        
        update_data = {
            'name': '새로운 캐릭터 이름'
        }
        
        response = self.client.put(
            self.character_url,
            data=update_data,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # 캐릭터 정보가 실제로 업데이트되었는지 확인
        character.refresh_from_db()
        self.assertEqual(character.name, '새로운 캐릭터 이름')
    
    def test_unauthorized_access(self):
        """인증되지 않은 접근 테스트"""
        response = self.client.get(self.character_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)