from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    help = 'Setup development environment with sample data'

    def handle(self, *args, **options):
        self.stdout.write('개발 환경 설정 시작...\n')

        try:
            # 1. 데이터베이스 마이그레이션
            self.stdout.write('데이터베이스 마이그레이션 실행...')
            call_command('migrate', verbosity=0)
            self.stdout.write('마이그레이션 완료\n')

            # 2. 관리자 계정 생성
            self.stdout.write('관리자 계정 생성...')
            call_command('create_admin')
            self.stdout.write('')

            # 3. 테스트 유저 생성
            self.stdout.write('테스트 유저 생성...')
            call_command('create_test_users')
            self.stdout.write('')

            # 4. 샘플 퀘스트 생성
            self.stdout.write('샘플 퀘스트 생성...')
            call_command('create_sample_quests')
            self.stdout.write('샘플 퀘스트 생성 완료\n')

            self.stdout.write('개발 환경 설정 완료!')
            self.stdout.write('\n' + '='*60)
            self.stdout.write('준비 완료된 서비스:')
            self.stdout.write('   - 프론트엔드: http://localhost:3000')
            self.stdout.write('   - API 서버: http://localhost:8000')
            self.stdout.write('   - Django Admin: http://localhost:8000/admin')
            self.stdout.write('\n빠른 테스트:')
            self.stdout.write('   - 테스트 계정: user1@test.com / 1234')
            self.stdout.write('   - 관리자: admin@healthquest.com / admin123')
            self.stdout.write('='*60)

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'설정 중 오류 발생: {e}')
            )