from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from datetime import date


class Character(models.Model):
    """사용자의 RPG 캐릭터"""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='character')
    name = models.CharField(max_length=50, help_text="캐릭터 이름")
    level = models.PositiveIntegerField(default=1)
    experience_points = models.PositiveIntegerField(default=0)
    
    # 8개 핵심 스탯
    stamina = models.PositiveIntegerField(default=10, help_text="체력 - 기초 체력, 에너지 관리")
    strength = models.PositiveIntegerField(default=10, help_text="근력 - 근육 운동, 저항 운동")
    mental = models.PositiveIntegerField(default=10, help_text="정신력 - 스트레스 관리, 집중력")
    endurance = models.PositiveIntegerField(default=10, help_text="지구력 - 유산소, 지속력")
    cardio = models.PositiveIntegerField(default=10, help_text="심폐 - 심혈관 건강")
    flexibility = models.PositiveIntegerField(default=10, help_text="유연성 - 스트레칭, 요가")
    nutrition = models.PositiveIntegerField(default=10, help_text="영양 - 균형잡힌 식단")
    recovery = models.PositiveIntegerField(default=10, help_text="회복 - 수면, 휴식")
    
    # 게임 화폐 및 보상
    gold = models.PositiveIntegerField(default=100)
    gems = models.PositiveIntegerField(default=0)
    
    # 캐릭터 외관
    skin = models.CharField(max_length=50, default='default', help_text="캐릭터 스킨")
    avatar_url = models.URLField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'characters'
        verbose_name = '캐릭터'
        verbose_name_plural = '캐릭터들'

    def __str__(self):
        return f"{self.user.nickname}의 {self.name} (Lv.{self.level})"

    @property
    def total_stats(self):
        """전체 스탯 합계"""
        return (self.stamina + self.strength + self.mental + self.endurance + 
                self.cardio + self.flexibility + self.nutrition + self.recovery)

    @property
    def health_score(self):
        """종합 건강 점수 (0-100)"""
        return min(100, self.total_stats // 2)

    def gain_experience(self, points):
        """경험치 획득 및 레벨업 처리"""
        self.experience_points += points
        
        # 레벨업 계산 (100 * level^1.2)
        required_exp = int(100 * (self.level ** 1.2))
        
        while self.experience_points >= required_exp:
            self.experience_points -= required_exp
            self.level += 1
            # 레벨업 시 스탯 포인트 자동 배분 (나중에 사용자가 직접 배분하도록 변경 가능)
            self.distribute_stat_points(2)
            required_exp = int(100 * (self.level ** 1.2))
        
        self.save()

    def distribute_stat_points(self, points):
        """스탯 포인트 자동 배분 (균등 분배)"""
        stats = ['stamina', 'strength', 'mental', 'endurance', 
                'cardio', 'flexibility', 'nutrition', 'recovery']
        
        for i in range(points):
            stat = stats[i % len(stats)]
            current_value = getattr(self, stat)
            setattr(self, stat, current_value + 1)


class Achievement(models.Model):
    """업적/칭호 시스템"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    icon = models.CharField(max_length=50, default='trophy')
    category = models.CharField(
        max_length=20,
        choices=[
            ('quest', '퀘스트'),
            ('stats', '스탯'),
            ('social', '소셜'),
            ('special', '특별'),
        ],
        default='quest'
    )
    requirement_type = models.CharField(
        max_length=20,
        choices=[
            ('quest_count', '퀘스트 완료 수'),
            ('streak', '연속 완료'),
            ('stat_level', '스탯 레벨'),
            ('level', '캐릭터 레벨'),
            ('special', '특별 조건'),
        ]
    )
    requirement_value = models.PositiveIntegerField()
    reward_gold = models.PositiveIntegerField(default=0)
    reward_gems = models.PositiveIntegerField(default=0)
    reward_experience = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'achievements'
        verbose_name = '업적'
        verbose_name_plural = '업적들'

    def __str__(self):
        return self.name


class UserAchievement(models.Model):
    """사용자 획득 업적"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    achieved_at = models.DateTimeField(auto_now_add=True)
    is_displayed = models.BooleanField(default=True, help_text="프로필에 표시 여부")

    class Meta:
        db_table = 'user_achievements'
        unique_together = ('user', 'achievement')
        verbose_name = '사용자 업적'
        verbose_name_plural = '사용자 업적들'

    def __str__(self):
        return f"{self.user.nickname} - {self.achievement.name}"


class StatHistory(models.Model):
    """스탯 변화 기록"""
    character = models.ForeignKey(Character, on_delete=models.CASCADE, related_name='stat_history')
    stat_type = models.CharField(
        max_length=20,
        choices=[
            ('stamina', '체력'),
            ('strength', '근력'),
            ('mental', '정신력'),
            ('endurance', '지구력'),
            ('cardio', '심폐'),
            ('flexibility', '유연성'),
            ('nutrition', '영양'),
            ('recovery', '회복'),
        ]
    )
    old_value = models.PositiveIntegerField()
    new_value = models.PositiveIntegerField()
    change_reason = models.CharField(max_length=100, help_text="변화 사유")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'stat_history'
        verbose_name = '스탯 변화 기록'
        verbose_name_plural = '스탯 변화 기록들'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.character.name} {self.stat_type}: {self.old_value} → {self.new_value}"


class NutritionLog(models.Model):
    """사용자 영양 섭취 기록"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='nutrition_logs')
    date = models.DateField(default=date.today)
    
    # 간편 입력 옵션들
    meal_type = models.CharField(
        max_length=20,
        choices=[
            ('breakfast', '아침'),
            ('lunch', '점심'),
            ('dinner', '저녁'),
            ('snack', '간식'),
        ]
    )
    
    # 사용자 친화적 선택지
    meal_quality = models.CharField(
        max_length=20,
        choices=[
            ('excellent', '매우 건강함'),
            ('good', '건강함'),
            ('fair', '보통'),
            ('poor', '개선 필요'),
        ],
        default='fair'
    )
    
    # 간단한 체크리스트
    included_vegetables = models.BooleanField(default=False, help_text="채소 포함 여부")
    included_protein = models.BooleanField(default=False, help_text="단백질 포함 여부")
    included_grains = models.BooleanField(default=False, help_text="곡물 포함 여부")
    proper_portion = models.BooleanField(default=False, help_text="적절한 양 섭취 여부")
    
    # 선택적 상세 입력
    notes = models.TextField(blank=True, help_text="추가 메모")
    calories_estimate = models.PositiveIntegerField(null=True, blank=True, help_text="예상 칼로리")
    
    # 식사 사진
    meal_image = models.ImageField(upload_to='nutrition/meals/', blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'nutrition_logs'
        verbose_name = '영양 기록'
        verbose_name_plural = '영양 기록들'
        ordering = ['-date', '-created_at']
        unique_together = ('user', 'date', 'meal_type')

    def __str__(self):
        return f"{self.user.nickname} - {self.get_meal_type_display()} ({self.date})"

    @property
    def nutrition_score(self):
        """영양 점수 계산 (0-100)"""
        score = 0
        
        # 기본 품질 점수
        quality_scores = {
            'excellent': 40,
            'good': 30,
            'fair': 20,
            'poor': 10
        }
        score += quality_scores.get(self.meal_quality, 0)
        
        # 체크리스트 점수 (각각 15점)
        if self.included_vegetables:
            score += 15
        if self.included_protein:
            score += 15
        if self.included_grains:
            score += 15
        if self.proper_portion:
            score += 15
            
        return min(100, score)


class Supplement(models.Model):
    """영양제/보충제 마스터 데이터"""
    name = models.CharField(max_length=100, unique=True)
    category = models.CharField(
        max_length=20,
        choices=[
            ('vitamin', '비타민'),
            ('mineral', '미네랄'),
            ('protein', '단백질'),
            ('omega', '오메가'),
            ('herb', '허브'),
            ('other', '기타'),
        ],
        default='other'
    )
    description = models.TextField(blank=True, help_text="효능 및 설명")
    default_dosage = models.CharField(max_length=50, help_text="권장 복용량")
    precautions = models.TextField(blank=True, help_text="주의사항")
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'supplements'
        verbose_name = '영양제'
        verbose_name_plural = '영양제들'
        ordering = ['category', 'name']

    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"


class UserSupplement(models.Model):
    """사용자 영양제 구독"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='supplements')
    supplement = models.ForeignKey(Supplement, on_delete=models.CASCADE)
    
    # 개인 설정
    dosage = models.CharField(max_length=50, help_text="개인 복용량")
    frequency = models.CharField(
        max_length=20,
        choices=[
            ('daily', '매일'),
            ('weekly', '주 몇회'),
            ('as_needed', '필요시'),
        ],
        default='daily'
    )
    
    # 복용 시간 설정
    morning = models.BooleanField(default=False)
    afternoon = models.BooleanField(default=False)
    evening = models.BooleanField(default=False)
    
    # 개인 메모
    personal_notes = models.TextField(blank=True)
    
    is_active = models.BooleanField(default=True)
    started_date = models.DateField(default=timezone.now)
    ended_date = models.DateField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user_supplements'
        verbose_name = '사용자 영양제'
        verbose_name_plural = '사용자 영양제들'
        unique_together = ('user', 'supplement')

    def __str__(self):
        return f"{self.user.nickname} - {self.supplement.name}"


class SupplementLog(models.Model):
    """영양제 복용 기록"""
    user_supplement = models.ForeignKey(UserSupplement, on_delete=models.CASCADE, related_name='logs')
    taken_at = models.DateTimeField(default=timezone.now)
    
    dosage_taken = models.CharField(max_length=50, help_text="실제 복용량")
    time_of_day = models.CharField(
        max_length=20,
        choices=[
            ('morning', '아침'),
            ('afternoon', '오후'),
            ('evening', '저녁'),
            ('night', '밤'),
        ]
    )
    
    notes = models.TextField(blank=True, help_text="복용 시 메모")
    side_effects = models.TextField(blank=True, help_text="부작용 기록")
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'supplement_logs'
        verbose_name = '영양제 복용 기록'
        verbose_name_plural = '영양제 복용 기록들'
        ordering = ['-taken_at']

    def __str__(self):
        return f"{self.user_supplement.supplement.name} - {self.taken_at.strftime('%Y-%m-%d %H:%M')}"