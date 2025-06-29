from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = 'Create admin user for development'

    def handle(self, *args, **options):
        self.stdout.write('관리자 계정 생성 중...\n')

        admin_data = {
            'username': 'admin',
            'email': 'admin@healthquest.com',
            'nickname': '관리자',
            'password': 'admin123'
        }

        try:
            # 이미 존재하는지 확인
            if User.objects.filter(email=admin_data['email']).exists():
                self.stdout.write('WARNING: 관리자 계정이 이미 존재합니다.')
                admin_user = User.objects.get(email=admin_data['email'])
                self.stdout.write(f'이메일: {admin_user.email}')
                self.stdout.write('비밀번호: admin123 (기본값)')
                return

            # 관리자 계정 생성
            admin_user = User.objects.create_superuser(
                username=admin_data['username'],
                email=admin_data['email'],
                nickname=admin_data['nickname'],
                password=admin_data['password']
            )

            self.stdout.write('관리자 계정 생성 완료!')
            self.stdout.write('\n' + '='*50)
            self.stdout.write('관리자 로그인 정보:')
            self.stdout.write(f'   이메일: {admin_data["email"]}')
            self.stdout.write(f'   비밀번호: {admin_data["password"]}')
            self.stdout.write('\nDjango Admin 접속:')
            self.stdout.write('   http://localhost:8000/admin')
            self.stdout.write('='*50)

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'관리자 계정 생성 실패: {e}')
            )