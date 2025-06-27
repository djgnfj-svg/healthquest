from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """확장된 사용자 모델"""
    email = models.EmailField(unique=True)
    nickname = models.CharField(max_length=50, unique=True)
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(
        max_length=10,
        choices=[
            ('male', '남성'),
            ('female', '여성'),
            ('other', '기타'),
        ],
        null=True,
        blank=True
    )
    height = models.FloatField(null=True, blank=True, help_text="키 (cm)")
    weight = models.FloatField(null=True, blank=True, help_text="몸무게 (kg)")
    activity_level = models.CharField(
        max_length=20,
        choices=[
            ('sedentary', '좌식생활'),
            ('light', '가벼운 활동'),
            ('moderate', '보통 활동'),
            ('active', '활발한 활동'),
            ('very_active', '매우 활발한 활동'),
        ],
        default='moderate'
    )
    timezone = models.CharField(max_length=50, default='Asia/Seoul')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'nickname']

    class Meta:
        db_table = 'users'
        verbose_name = '사용자'
        verbose_name_plural = '사용자들'

    def __str__(self):
        return f"{self.nickname} ({self.email})"


class UserProfile(models.Model):
    """사용자 프로필 추가 정보"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(max_length=500, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    notification_enabled = models.BooleanField(default=True)
    email_notification = models.BooleanField(default=True)
    push_notification = models.BooleanField(default=True)
    privacy_level = models.CharField(
        max_length=20,
        choices=[
            ('public', '공개'),
            ('friends', '친구만'),
            ('private', '비공개'),
        ],
        default='friends'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user_profiles'
        verbose_name = '사용자 프로필'
        verbose_name_plural = '사용자 프로필들'

    def __str__(self):
        return f"{self.user.nickname}의 프로필"