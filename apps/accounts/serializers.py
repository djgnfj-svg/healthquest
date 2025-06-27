from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from .models import User, UserProfile


class UserRegistrationSerializer(serializers.ModelSerializer):
    """사용자 회원가입 시리얼라이저"""
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('email', 'username', 'nickname', 'password', 'password_confirm',
                 'birth_date', 'gender', 'height', 'weight', 'activity_level')

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("비밀번호가 일치하지 않습니다.")
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        UserProfile.objects.create(user=user)
        return user


class UserLoginSerializer(serializers.Serializer):
    """사용자 로그인 시리얼라이저"""
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(username=email, password=password)
            if not user:
                raise serializers.ValidationError('이메일 또는 비밀번호가 올바르지 않습니다.')
            if not user.is_active:
                raise serializers.ValidationError('비활성화된 계정입니다.')
            attrs['user'] = user
            return attrs
        else:
            raise serializers.ValidationError('이메일과 비밀번호를 모두 입력해주세요.')


class UserProfileSerializer(serializers.ModelSerializer):
    """사용자 프로필 시리얼라이저"""
    class Meta:
        model = UserProfile
        fields = ('bio', 'avatar', 'notification_enabled', 'email_notification',
                 'push_notification', 'privacy_level')


class UserSerializer(serializers.ModelSerializer):
    """사용자 정보 시리얼라이저"""
    profile = UserProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'nickname', 'birth_date', 'gender',
                 'height', 'weight', 'activity_level', 'date_joined', 'profile')
        read_only_fields = ('id', 'email', 'date_joined')


class UserUpdateSerializer(serializers.ModelSerializer):
    """사용자 정보 수정 시리얼라이저"""
    profile = UserProfileSerializer(required=False)

    class Meta:
        model = User
        fields = ('nickname', 'birth_date', 'gender', 'height', 'weight',
                 'activity_level', 'profile')

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', None)
        
        # User 정보 업데이트
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Profile 정보 업데이트
        if profile_data:
            profile = instance.profile
            for attr, value in profile_data.items():
                setattr(profile, attr, value)
            profile.save()

        return instance