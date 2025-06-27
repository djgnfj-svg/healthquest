from django.core.management.base import BaseCommand
from apps.quests.models import QuestTemplate


class Command(BaseCommand):
    help = '샘플 퀘스트 템플릿 생성'

    def handle(self, *args, **options):
        quest_templates = [
            # 아침 퀘스트
            {
                'title': '일찍 일어나기',
                'description': '오전 7시 이전에 일어나서 하루를 시작하세요.',
                'category': 'morning',
                'target_stats': {'mental': 1, 'recovery': 1},
                'base_experience': 15,
                'base_gold': 10,
                'difficulty': 'easy',
                'duration_minutes': 5,
                'time_of_day': 'morning',
            },
            {
                'title': '아침 스트레칭',
                'description': '10분간 가벼운 스트레칭으로 몸을 깨워보세요.',
                'category': 'morning',
                'target_stats': {'flexibility': 2, 'stamina': 1},
                'base_experience': 20,
                'base_gold': 15,
                'difficulty': 'easy',
                'duration_minutes': 10,
                'time_of_day': 'morning',
            },
            {
                'title': '물 한 잔 마시기',
                'description': '일어나자마자 물 한 잔으로 몸에 수분을 공급하세요.',
                'category': 'morning',
                'target_stats': {'nutrition': 1, 'stamina': 1},
                'base_experience': 10,
                'base_gold': 5,
                'difficulty': 'easy',
                'duration_minutes': 2,
                'time_of_day': 'morning',
            },
            
            # 업무/학습 퀘스트
            {
                'title': '30분 집중 작업',
                'description': '30분간 집중해서 중요한 업무나 학습을 진행하세요.',
                'category': 'work',
                'target_stats': {'mental': 2, 'endurance': 1},
                'base_experience': 25,
                'base_gold': 20,
                'difficulty': 'normal',
                'duration_minutes': 30,
                'time_of_day': 'any',
            },
            {
                'title': '계단 오르기',
                'description': '엘리베이터 대신 계단을 이용해 보세요.',
                'category': 'work',
                'target_stats': {'cardio': 2, 'strength': 1},
                'base_experience': 15,
                'base_gold': 10,
                'difficulty': 'easy',
                'duration_minutes': 5,
                'time_of_day': 'any',
            },
            
            # 저녁 퀘스트
            {
                'title': '산책하기',
                'description': '20분간 가벼운 산책으로 하루의 스트레스를 해소하세요.',
                'category': 'evening',
                'target_stats': {'cardio': 2, 'mental': 1, 'stamina': 1},
                'base_experience': 30,
                'base_gold': 25,
                'difficulty': 'normal',
                'duration_minutes': 20,
                'time_of_day': 'evening',
                'weather_condition': 'any',
            },
            {
                'title': '홈트레이닝',
                'description': '15분간 홈트레이닝으로 근력을 기르세요.',
                'category': 'evening',
                'target_stats': {'strength': 3, 'endurance': 1},
                'base_experience': 35,
                'base_gold': 30,
                'difficulty': 'normal',
                'duration_minutes': 15,
                'time_of_day': 'evening',
            },
            {
                'title': '건강한 저녁 식사',
                'description': '균형잡힌 저녁 식사를 준비해서 드세요.',
                'category': 'evening',
                'target_stats': {'nutrition': 3, 'stamina': 1},
                'base_experience': 25,
                'base_gold': 20,
                'difficulty': 'normal',
                'duration_minutes': 30,
                'time_of_day': 'evening',
            },
            
            # 밤 퀘스트
            {
                'title': '독서하기',
                'description': '잠들기 전 15분간 독서로 마음을 진정시키세요.',
                'category': 'night',
                'target_stats': {'mental': 2, 'recovery': 1},
                'base_experience': 20,
                'base_gold': 15,
                'difficulty': 'easy',
                'duration_minutes': 15,
                'time_of_day': 'night',
            },
            {
                'title': '일찍 잠자리에 들기',
                'description': '밤 11시 이전에 잠자리에 들어 충분한 수면을 취하세요.',
                'category': 'night',
                'target_stats': {'recovery': 3, 'mental': 1},
                'base_experience': 25,
                'base_gold': 20,
                'difficulty': 'normal',
                'duration_minutes': 5,
                'time_of_day': 'night',
            },
            
            # 주간 퀘스트
            {
                'title': '주 3회 운동하기',
                'description': '일주일에 최소 3번은 30분 이상 운동하세요.',
                'category': 'weekly',
                'target_stats': {'stamina': 3, 'strength': 3, 'cardio': 3},
                'base_experience': 100,
                'base_gold': 80,
                'base_gems': 5,
                'difficulty': 'normal',
                'duration_minutes': 90,
                'time_of_day': 'any',
            },
            {
                'title': '주간 건강 체크',
                'description': '일주일간의 건강 상태를 점검하고 다음 주 목표를 세우세요.',
                'category': 'weekly',
                'target_stats': {'mental': 2, 'nutrition': 2},
                'base_experience': 50,
                'base_gold': 40,
                'base_gems': 3,
                'difficulty': 'easy',
                'duration_minutes': 20,
                'time_of_day': 'any',
            },
            
            # 도전 퀘스트
            {
                'title': '7일 연속 스트레칭',
                'description': '7일 연속으로 매일 스트레칭을 실시하세요.',
                'category': 'challenge',
                'target_stats': {'flexibility': 5, 'endurance': 3, 'mental': 2},
                'base_experience': 200,
                'base_gold': 150,
                'base_gems': 10,
                'difficulty': 'hard',
                'duration_minutes': 70,
                'required_level': 3,
                'time_of_day': 'any',
            },
            {
                'title': '만보 걷기 챌린지',
                'description': '하루에 10,000보를 걸어보세요.',
                'category': 'challenge',
                'target_stats': {'cardio': 4, 'stamina': 3, 'endurance': 3},
                'base_experience': 150,
                'base_gold': 120,
                'base_gems': 8,
                'difficulty': 'hard',
                'duration_minutes': 120,
                'required_level': 2,
                'time_of_day': 'any',
                'weather_condition': 'any',
            },
        ]

        created_count = 0
        updated_count = 0

        for template_data in quest_templates:
            template, created = QuestTemplate.objects.get_or_create(
                title=template_data['title'],
                defaults=template_data
            )
            
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'✓ 퀘스트 템플릿 생성: {template.title}')
                )
            else:
                # 기존 템플릿 업데이트
                for key, value in template_data.items():
                    setattr(template, key, value)
                template.save()
                updated_count += 1
                self.stdout.write(
                    self.style.WARNING(f'• 퀘스트 템플릿 업데이트: {template.title}')
                )

        self.stdout.write(
            self.style.SUCCESS(
                f'\n완료! 생성: {created_count}개, 업데이트: {updated_count}개'
            )
        )