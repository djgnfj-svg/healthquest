from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.characters.models import Character
import random

User = get_user_model()


class Command(BaseCommand):
    help = 'Create test users for development'

    def handle(self, *args, **options):
        self.stdout.write('테스트 유저 생성 시작...\n')

        # 테스트 유저 데이터
        test_users = [
            {
                'username': 'user1',
                'email': 'user1@test.com',
                'nickname': '건강왕',
                'password': '1234',
                'gender': 'male',
                'height': 175,
                'weight': 70,
                'activity_level': 'active'
            },
            {
                'username': 'user2', 
                'email': 'user2@test.com',
                'nickname': '운동러버',
                'password': '1234',
                'gender': 'female',
                'height': 165,
                'weight': 55,
                'activity_level': 'very_active'
            },
            {
                'username': 'user3',
                'email': 'user3@test.com', 
                'nickname': '요가마스터',
                'password': '1234',
                'gender': 'female',
                'height': 160,
                'weight': 50,
                'activity_level': 'moderate'
            },
            {
                'username': 'user4',
                'email': 'user4@test.com',
                'nickname': '헬스킹',
                'password': '1234', 
                'gender': 'male',
                'height': 180,
                'weight': 80,
                'activity_level': 'very_active'
            },
            {
                'username': 'user5',
                'email': 'user5@test.com',
                'nickname': '다이어터',
                'password': '1234',
                'gender': 'female', 
                'height': 158,
                'weight': 48,
                'activity_level': 'light'
            },
            {
                'username': 'user6',
                'email': 'user6@test.com',
                'nickname': '마라토너',
                'password': '1234',
                'gender': 'male',
                'height': 172,
                'weight': 65,
                'activity_level': 'very_active'
            },
            {
                'username': 'user7',
                'email': 'user7@test.com',
                'nickname': '필라테스퀸',
                'password': '1234',
                'gender': 'female',
                'height': 167,
                'weight': 58,
                'activity_level': 'active'
            },
            {
                'username': 'user8',
                'email': 'user8@test.com',
                'nickname': '수영선수',
                'password': '1234',
                'gender': 'male',
                'height': 178,
                'weight': 75,
                'activity_level': 'very_active'
            },
            {
                'username': 'user9',
                'email': 'user9@test.com',
                'nickname': '명상러',
                'password': '1234',
                'gender': 'other',
                'height': 170,
                'weight': 60,
                'activity_level': 'moderate'
            },
            {
                'username': 'user10',
                'email': 'user10@test.com',
                'nickname': '초보자',
                'password': '1234',
                'gender': 'male',
                'height': 169,
                'weight': 68,
                'activity_level': 'sedentary'
            }
        ]

        created_count = 0
        
        for user_data in test_users:
            try:
                # 이미 존재하는 유저는 건너뛰기
                if User.objects.filter(email=user_data['email']).exists():
                    self.stdout.write(f"WARNING: {user_data['nickname']} ({user_data['email']}) 이미 존재함")
                    continue
                
                # 유저 생성
                user = User.objects.create_user(
                    username=user_data['username'],
                    email=user_data['email'], 
                    nickname=user_data['nickname'],
                    password=user_data['password'],
                    gender=user_data['gender'],
                    height=user_data['height'],
                    weight=user_data['weight'],
                    activity_level=user_data['activity_level']
                )
                
                # 캐릭터 생성 (랜덤 스탯으로 다양성 추가)
                character = Character.objects.create(
                    user=user,
                    name=f"{user_data['nickname']}의 캐릭터",
                    level=random.randint(1, 10),
                    experience_points=random.randint(0, 500),
                    stamina=random.randint(10, 30),
                    strength=random.randint(10, 30), 
                    mental=random.randint(10, 30),
                    endurance=random.randint(10, 30),
                    cardio=random.randint(10, 30),
                    flexibility=random.randint(10, 30),
                    nutrition=random.randint(10, 30),
                    recovery=random.randint(10, 30),
                    gold=random.randint(100, 1000),
                    gems=random.randint(0, 100)
                )
                
                created_count += 1
                self.stdout.write(
                    f"SUCCESS: {user_data['nickname']} (Lv.{character.level}) - {user_data['email']} / {user_data['password']}"
                )
                
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f"ERROR: {user_data['nickname']} 생성 실패: {e}")
                )

        self.stdout.write('\n' + '='*60)
        self.stdout.write(f'테스트 유저 {created_count}명 생성 완료!')
        self.stdout.write('\n로그인 정보:')
        self.stdout.write('   이메일: user1@test.com ~ user10@test.com')
        self.stdout.write('   비밀번호: 1234 (모든 계정 동일)')
        self.stdout.write('\n사용법:')
        self.stdout.write('   1. 프론트엔드에서 user1@test.com / 1234 로 로그인')
        self.stdout.write('   2. 각 유저마다 다른 캐릭터 스탯과 레벨을 가지고 있음')
        self.stdout.write('   3. 테스트용이므로 언제든 다시 생성 가능')
        self.stdout.write('='*60)