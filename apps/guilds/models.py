from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator


class Guild(models.Model):
    """길드 (4-8명 소규모 팀)"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    motto = models.CharField(max_length=200, blank=True, help_text="길드 모토")
    
    # 길드 설정
    max_members = models.PositiveIntegerField(
        default=6,
        validators=[MinValueValidator(4), MaxValueValidator(8)]
    )
    is_private = models.BooleanField(default=False, help_text="비공개 길드 여부")
    join_code = models.CharField(max_length=10, unique=True, blank=True, null=True)
    
    # 길드 통계
    level = models.PositiveIntegerField(default=1)
    experience_points = models.PositiveIntegerField(default=0)
    total_quests_completed = models.PositiveIntegerField(default=0)
    
    # 길드 외관
    emblem = models.CharField(max_length=50, default='shield')
    color_theme = models.CharField(max_length=7, default='#3B82F6', help_text="HEX 색상 코드")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'guilds'
        verbose_name = '길드'
        verbose_name_plural = '길드들'

    def __str__(self):
        return f"{self.name} (Lv.{self.level})"

    @property
    def member_count(self):
        return self.members.count()

    @property
    def is_full(self):
        return self.member_count >= self.max_members

    def can_join(self, user):
        """사용자가 길드에 가입할 수 있는지 확인"""
        if self.is_full:
            return False, "길드가 가득 찼습니다."
        
        if self.members.filter(user=user).exists():
            return False, "이미 길드에 소속되어 있습니다."
        
        if user.guild_memberships.exclude(status='left').exists():
            return False, "다른 길드에 이미 소속되어 있습니다."
        
        return True, "가입 가능합니다."

    def gain_experience(self, points):
        """길드 경험치 획득 및 레벨업"""
        self.experience_points += points
        
        # 길드 레벨업 계산 (200 * level^1.5)
        required_exp = int(200 * (self.level ** 1.5))
        
        while self.experience_points >= required_exp:
            self.experience_points -= required_exp
            self.level += 1
            required_exp = int(200 * (self.level ** 1.5))
        
        self.save()


class GuildMembership(models.Model):
    """길드 멤버십"""
    guild = models.ForeignKey(Guild, on_delete=models.CASCADE, related_name='members')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='guild_memberships')
    
    role = models.CharField(
        max_length=20,
        choices=[
            ('leader', '길드장'),
            ('officer', '부길드장'),
            ('member', '일반 멤버'),
        ],
        default='member'
    )
    
    status = models.CharField(
        max_length=20,
        choices=[
            ('active', '활성'),
            ('inactive', '비활성'),
            ('left', '탈퇴'),
            ('kicked', '추방'),
        ],
        default='active'
    )
    
    # 멤버 통계
    contributed_experience = models.PositiveIntegerField(default=0)
    quests_completed = models.PositiveIntegerField(default=0)
    
    joined_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'guild_memberships'
        unique_together = ('guild', 'user')
        verbose_name = '길드 멤버십'
        verbose_name_plural = '길드 멤버십들'

    def __str__(self):
        return f"{self.user.nickname} - {self.guild.name} ({self.role})"

    def contribute_experience(self, points):
        """길드에 경험치 기여"""
        self.contributed_experience += points
        self.save()
        
        # 길드 경험치 증가
        self.guild.gain_experience(points)


class GuildQuest(models.Model):
    """길드 공동 퀘스트"""
    guild = models.ForeignKey(Guild, on_delete=models.CASCADE, related_name='guild_quests')
    title = models.CharField(max_length=200)
    description = models.TextField()
    
    # 목표 설정
    target_type = models.CharField(
        max_length=20,
        choices=[
            ('total_quests', '총 퀘스트 완료 수'),
            ('member_participation', '멤버 참여율'),
            ('streak_days', '연속 완료 일수'),
            ('stat_improvement', '스탯 향상'),
        ]
    )
    target_value = models.PositiveIntegerField()
    current_progress = models.PositiveIntegerField(default=0)
    
    # 보상
    reward_guild_experience = models.PositiveIntegerField(default=0)
    reward_member_experience = models.PositiveIntegerField(default=0)
    reward_member_gold = models.PositiveIntegerField(default=0)
    reward_member_gems = models.PositiveIntegerField(default=0)
    
    # 퀘스트 기간
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    
    status = models.CharField(
        max_length=20,
        choices=[
            ('active', '진행 중'),
            ('completed', '완료'),
            ('failed', '실패'),
            ('expired', '만료'),
        ],
        default='active'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'guild_quests'
        verbose_name = '길드 퀘스트'
        verbose_name_plural = '길드 퀘스트들'

    def __str__(self):
        return f"{self.guild.name} - {self.title}"

    @property
    def progress_percentage(self):
        if self.target_value == 0:
            return 0
        return min(100, (self.current_progress / self.target_value) * 100)

    def check_completion(self):
        """퀘스트 완료 확인 및 처리"""
        if self.current_progress >= self.target_value and self.status == 'active':
            self.status = 'completed'
            self.save()
            self._distribute_rewards()

    def _distribute_rewards(self):
        """보상 분배"""
        # 길드 경험치 지급
        if self.reward_guild_experience > 0:
            self.guild.gain_experience(self.reward_guild_experience)
        
        # 멤버 보상 지급
        active_members = self.guild.members.filter(status='active')
        for membership in active_members:
            character = membership.user.character
            
            if self.reward_member_experience > 0:
                character.gain_experience(self.reward_member_experience)
            
            if self.reward_member_gold > 0:
                character.gold += self.reward_member_gold
            
            if self.reward_member_gems > 0:
                character.gems += self.reward_member_gems
            
            character.save()


class GuildMessage(models.Model):
    """길드 메시지 (응원, 격려)"""
    guild = models.ForeignKey(Guild, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='received_guild_messages',
        null=True, 
        blank=True,
        help_text="특정 멤버에게 보내는 메시지, 없으면 전체 메시지"
    )
    
    message_type = models.CharField(
        max_length=20,
        choices=[
            ('general', '일반'),
            ('encouragement', '응원'),
            ('celebration', '축하'),
            ('quest_share', '퀘스트 공유'),
        ],
        default='general'
    )
    
    content = models.TextField(max_length=500)
    related_quest = models.ForeignKey(
        'quests.Quest', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='guild_messages'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'guild_messages'
        verbose_name = '길드 메시지'
        verbose_name_plural = '길드 메시지들'
        ordering = ['-created_at']

    def __str__(self):
        recipient_name = f" to {self.recipient.nickname}" if self.recipient else ""
        return f"{self.sender.nickname}{recipient_name}: {self.content[:50]}..."


class GuildRanking(models.Model):
    """길드 랭킹 (주간/월간)"""
    guild = models.ForeignKey(Guild, on_delete=models.CASCADE)
    ranking_type = models.CharField(
        max_length=20,
        choices=[
            ('weekly', '주간'),
            ('monthly', '월간'),
            ('all_time', '전체'),
        ]
    )
    
    rank_position = models.PositiveIntegerField()
    score = models.PositiveIntegerField(help_text="랭킹 점수")
    
    # 기간
    start_date = models.DateField()
    end_date = models.DateField()
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'guild_rankings'
        unique_together = ('guild', 'ranking_type', 'start_date')
        verbose_name = '길드 랭킹'
        verbose_name_plural = '길드 랭킹들'
        ordering = ['rank_position']

    def __str__(self):
        return f"{self.guild.name} - {self.ranking_type} {self.rank_position}위"