from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator


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