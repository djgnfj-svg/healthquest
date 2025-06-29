from django.core.management.base import BaseCommand
from apps.characters.models import Supplement


class Command(BaseCommand):
    help = '기본 영양제 데이터 생성'

    def handle(self, *args, **options):
        self.stdout.write('기본 영양제 데이터 생성 시작...\n')

        supplements_data = [
            # 비타민
            {
                'name': '비타민 C',
                'category': 'vitamin',
                'description': '면역력 강화 및 항산화 효과',
                'default_dosage': '1000mg 1일 1회',
                'precautions': '공복 섭취 시 위장 장애 가능'
            },
            {
                'name': '비타민 D3',
                'category': 'vitamin',
                'description': '뼈 건강 및 칼슘 흡수 촉진',
                'default_dosage': '2000IU 1일 1회',
                'precautions': '과다 복용 시 고칼슘혈증 위험'
            },
            {
                'name': '비타민 B군 복합',
                'category': 'vitamin',
                'description': '에너지 대사 및 신경계 건강',
                'default_dosage': '1정 1일 1회',
                'precautions': '임신부는 의사와 상담 필요'
            },
            {
                'name': '엽산',
                'category': 'vitamin',
                'description': '세포 분열 및 DNA 합성',
                'default_dosage': '400㎍ 1일 1회',
                'precautions': '임신 계획 시 미리 복용 권장'
            },

            # 미네랄
            {
                'name': '마그네슘',
                'category': 'mineral',
                'description': '근육 이완 및 수면 질 개선',
                'default_dosage': '300mg 1일 1회',
                'precautions': '신장 질환자는 복용 전 상담 필요'
            },
            {
                'name': '아연',
                'category': 'mineral',
                'description': '면역력 강화 및 상처 치유',
                'default_dosage': '15mg 1일 1회',
                'precautions': '공복 복용 시 메스꺼움 가능'
            },
            {
                'name': '철분',
                'category': 'mineral',
                'description': '빈혈 예방 및 산소 운반',
                'default_dosage': '18mg 1일 1회',
                'precautions': '차, 커피와 함께 복용 금지'
            },
            {
                'name': '칼슘',
                'category': 'mineral',
                'description': '뼈와 치아 건강',
                'default_dosage': '600mg 1일 2회',
                'precautions': '비타민 D와 함께 복용 권장'
            },

            # 단백질
            {
                'name': '유청 단백질',
                'category': 'protein',
                'description': '근육 성장 및 회복',
                'default_dosage': '30g 운동 후',
                'precautions': '유당불내증 환자 주의'
            },
            {
                'name': '콜라겐',
                'category': 'protein',
                'description': '피부 탄력 및 관절 건강',
                'default_dosage': '10g 1일 1회',
                'precautions': '알레르기 반응 확인 필요'
            },

            # 오메가
            {
                'name': '오메가-3',
                'category': 'omega',
                'description': '심혈관 건강 및 뇌 기능 개선',
                'default_dosage': '1000mg 1일 1회',
                'precautions': '혈액응고제 복용자 상담 필요'
            },
            {
                'name': '감마리놀렌산 (GLA)',
                'category': 'omega',
                'description': '호르몬 균형 및 염증 완화',
                'default_dosage': '500mg 1일 1회',
                'precautions': '임신부 복용 금지'
            },

            # 허브
            {
                'name': '밀크씨슬',
                'category': 'herb',
                'description': '간 건강 및 해독 작용',
                'default_dosage': '150mg 1일 2회',
                'precautions': '국화과 알레르기 주의'
            },
            {
                'name': '홍삼',
                'category': 'herb',
                'description': '면역력 강화 및 피로 회복',
                'default_dosage': '1g 1일 1회',
                'precautions': '고혈압 환자 상담 필요'
            },
            {
                'name': '은행잎 추출물',
                'category': 'herb',
                'description': '혈액순환 및 기억력 개선',
                'default_dosage': '120mg 1일 1회',
                'precautions': '혈액응고제와 상호작용 주의'
            },

            # 기타
            {
                'name': '프로바이오틱스',
                'category': 'other',
                'description': '장 건강 및 소화 개선',
                'default_dosage': '100억 CFU 1일 1회',
                'precautions': '냉장 보관 권장'
            },
            {
                'name': '코큐텐 (CoQ10)',
                'category': 'other',
                'description': '심장 건강 및 에너지 생성',
                'default_dosage': '100mg 1일 1회',
                'precautions': '혈압약과 상호작용 가능'
            },
            {
                'name': '루테인',
                'category': 'other',
                'description': '눈 건강 및 시력 보호',
                'default_dosage': '20mg 1일 1회',
                'precautions': '베타카로틴과 함께 복용 권장'
            },
        ]

        created_count = 0
        
        for supplement_data in supplements_data:
            supplement, created = Supplement.objects.get_or_create(
                name=supplement_data['name'],
                defaults=supplement_data
            )
            
            if created:
                created_count += 1
                self.stdout.write(f"✓ 영양제 생성: {supplement.name} ({supplement.get_category_display()})")
            else:
                self.stdout.write(f"WARNING: {supplement.name} 이미 존재함")

        self.stdout.write('\n' + '='*60)
        self.stdout.write(f'기본 영양제 {created_count}개 생성 완료!')
        self.stdout.write('\n사용법:')
        self.stdout.write('   1. Admin 페이지에서 영양제 목록 확인')
        self.stdout.write('   2. API로 영양제 검색 및 구독')
        self.stdout.write('   3. 사용자별 복용 기록 관리')
        self.stdout.write('='*60)