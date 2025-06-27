from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


class QuestTemplate(models.Model):
    """퀘스트 템플릿 (관리자가 생성하는 퀘스트 유형)"""
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(
        max_length=20,
        choices=[
            ('morning', '아침'),
            ('work', '업무/학습'),
            ('evening', '저녁'),
            ('night', '밤'),
            ('weekly', '주간'),
            ('challenge', '도전'),
        ],
        default='morning'
    )
    
    # 목표 스탯 (이 퀘스트를 완료하면 어떤 스탯이 증가하는지)
    target_stats = models.JSONField(
        default=dict,
        help_text="{'stamina': 2, 'strength': 1} 형태로 저장"
    )
    
    # 기본 보상
    base_experience = models.PositiveIntegerField(default=10)
    base_gold = models.PositiveIntegerField(default=5)
    base_gems = models.PositiveIntegerField(default=0)
    
    # 퀘스트 속성
    difficulty = models.CharField(
        max_length=10,
        choices=[
            ('easy', '쉬움'),
            ('normal', '보통'),
            ('hard', '어려움'),
            ('expert', '전문가'),
        ],
        default='normal'
    )
    
    duration_minutes = models.PositiveIntegerField(default=30, help_text="예상 소요 시간(분)")
    required_level = models.PositiveIntegerField(default=1)
    
    # 퀘스트 활성화 조건
    weather_condition = models.CharField(
        max_length=20,
        choices=[
            ('any', '모든 날씨'),
            ('sunny', '맑음'),
            ('cloudy', '흐림'),
            ('rainy', '비'),
            ('snowy', '눈'),
        ],
        default='any'
    )
    
    time_of_day = models.CharField(
        max_length=20,
        choices=[
            ('any', '모든 시간'),
            ('morning', '아침 (06:00-12:00)'),
            ('afternoon', '오후 (12:00-18:00)'),
            ('evening', '저녁 (18:00-22:00)'),
            ('night', '밤 (22:00-06:00)'),
        ],
        default='any'
    )
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'quest_templates'
        verbose_name = '퀘스트 템플릿'
        verbose_name_plural = '퀘스트 템플릿들'

    def __str__(self):
        return f"{self.title} ({self.category})"


class Quest(models.Model):
    """사용자에게 할당된 개별 퀘스트"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    template = models.ForeignKey(QuestTemplate, on_delete=models.CASCADE)
    
    # 개인화된 내용 (AI가 조정 가능)
    custom_title = models.CharField(max_length=200, blank=True)
    custom_description = models.TextField(blank=True)
    
    # 개인화된 목표 및 보상
    target_stats = models.JSONField(default=dict)
    experience_reward = models.PositiveIntegerField()
    gold_reward = models.PositiveIntegerField()
    gems_reward = models.PositiveIntegerField(default=0)
    
    # 퀘스트 상태
    status = models.CharField(
        max_length=20,
        choices=[
            ('assigned', '할당됨'),
            ('in_progress', '진행 중'),
            ('completed', '완료'),
            ('failed', '실패'),
            ('expired', '만료'),
        ],
        default='assigned'
    )
    
    # 퀘스트 스케줄
    assigned_date = models.DateTimeField(auto_now_add=True)
    start_date = models.DateTimeField(null=True, blank=True)
    due_date = models.DateTimeField()
    completed_date = models.DateTimeField(null=True, blank=True)
    
    # 진행 상황
    progress_percentage = models.FloatField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    
    # 퀘스트 검증
    requires_verification = models.BooleanField(default=False)
    verification_image = models.ImageField(upload_to='quest_verifications/', blank=True, null=True)
    verification_note = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'quests'
        verbose_name = '퀘스트'
        verbose_name_plural = '퀘스트들'
        ordering = ['-created_at']

    def __str__(self):
        title = self.custom_title or self.template.title
        return f"{self.user.nickname} - {title} ({self.status})"

    @property
    def title(self):
        return self.custom_title or self.template.title

    @property
    def description(self):
        return self.custom_description or self.template.description

    def start_quest(self):
        """퀘스트 시작"""
        if self.status == 'assigned':
            self.status = 'in_progress'
            self.start_date = timezone.now()
            self.save()

    def complete_quest(self):
        """퀘스트 완료 처리"""
        if self.status == 'in_progress':
            self.status = 'completed'
            self.completed_date = timezone.now()
            self.progress_percentage = 100
            self.save()
            
            # 보상 지급
            self._give_rewards()

    def _give_rewards(self):
        """보상 지급"""
        character = self.user.character
        
        # 경험치 및 화폐 지급
        character.gain_experience(self.experience_reward)
        character.gold += self.gold_reward
        character.gems += self.gems_reward
        
        # 스탯 증가
        for stat, value in self.target_stats.items():
            if hasattr(character, stat):
                old_value = getattr(character, stat)
                new_value = old_value + value
                setattr(character, stat, new_value)
                
                # 스탯 변화 기록
                from apps.characters.models import StatHistory
                StatHistory.objects.create(
                    character=character,
                    stat_type=stat,
                    old_value=old_value,
                    new_value=new_value,
                    change_reason=f"퀘스트 완료: {self.title}"
                )
        
        character.save()

    def fail_quest(self):
        """퀘스트 실패 처리"""
        if self.status in ['assigned', 'in_progress']:
            self.status = 'failed'
            self.save()

    def is_overdue(self):
        """퀘스트 만료 확인"""
        return timezone.now() > self.due_date and self.status not in ['completed', 'failed']


class QuestCompletion(models.Model):
    """퀘스트 완료 기록"""
    quest = models.OneToOneField(Quest, on_delete=models.CASCADE)
    completion_time = models.DateTimeField(auto_now_add=True)
    actual_duration = models.DurationField(null=True, blank=True)
    difficulty_rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        null=True,
        blank=True,
        help_text="사용자가 평가한 난이도 (1-5)"
    )
    satisfaction_rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        null=True,
        blank=True,
        help_text="사용자 만족도 (1-5)"
    )
    user_notes = models.TextField(blank=True)

    class Meta:
        db_table = 'quest_completions'
        verbose_name = '퀘스트 완료 기록'
        verbose_name_plural = '퀘스트 완료 기록들'

    def __str__(self):
        return f"{self.quest.title} 완료 기록"


class DailyStreak(models.Model):
    """연속 완료 기록"""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    current_streak = models.PositiveIntegerField(default=0)
    longest_streak = models.PositiveIntegerField(default=0)
    last_completion_date = models.DateField(null=True, blank=True)
    streak_start_date = models.DateField(null=True, blank=True)

    class Meta:
        db_table = 'daily_streaks'
        verbose_name = '연속 완료 기록'
        verbose_name_plural = '연속 완료 기록들'

    def __str__(self):
        return f"{self.user.nickname} - 현재 {self.current_streak}일, 최고 {self.longest_streak}일"

    def update_streak(self, completion_date):
        """연속 기록 업데이트"""
        if not self.last_completion_date:
            # 첫 완료
            self.current_streak = 1
            self.longest_streak = 1
            self.streak_start_date = completion_date
        elif completion_date == self.last_completion_date:
            # 같은 날 완료 (중복 처리 방지)
            return
        elif completion_date == self.last_completion_date + timezone.timedelta(days=1):
            # 연속 완료
            self.current_streak += 1
            if self.current_streak > self.longest_streak:
                self.longest_streak = self.current_streak
        else:
            # 연속 끊김
            self.current_streak = 1
            self.streak_start_date = completion_date

        self.last_completion_date = completion_date
        self.save()