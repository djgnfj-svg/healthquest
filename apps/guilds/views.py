from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils.crypto import get_random_string
from .models import Guild, GuildMembership, GuildQuest, GuildMessage
from .serializers import (
    GuildSerializer, GuildMembershipSerializer, GuildQuestSerializer,
    GuildMessageSerializer, GuildCreateSerializer, GuildJoinSerializer
)


class GuildListView(generics.ListAPIView):
    """길드 목록 조회"""
    serializer_class = GuildSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # 공개 길드만 표시
        return Guild.objects.filter(is_private=False).order_by('-level', '-experience_points')


class GuildDetailView(generics.RetrieveAPIView):
    """길드 상세 조회"""
    serializer_class = GuildSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Guild.objects.all()


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_guild_view(request):
    """길드 생성"""
    # 이미 길드에 소속되어 있는지 확인
    if GuildMembership.objects.filter(user=request.user, status='active').exists():
        return Response(
            {'error': '이미 길드에 소속되어 있습니다.'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    serializer = GuildCreateSerializer(data=request.data)
    if serializer.is_valid():
        guild = serializer.save()
        
        # 길드 생성자를 길드장으로 설정
        GuildMembership.objects.create(
            guild=guild,
            user=request.user,
            role='leader'
        )
        
        # 비공개 길드인 경우 참가 코드 생성
        if guild.is_private:
            guild.join_code = get_random_string(8).upper()
            guild.save()
        
        return Response({
            'message': '길드가 생성되었습니다.',
            'guild': GuildSerializer(guild).data
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def join_guild_view(request):
    """길드 가입"""
    serializer = GuildJoinSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # 이미 길드에 소속되어 있는지 확인
    if GuildMembership.objects.filter(user=request.user, status='active').exists():
        return Response(
            {'error': '이미 길드에 소속되어 있습니다.'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    guild = None
    
    # 길드 찾기
    if serializer.validated_data.get('join_code'):
        try:
            guild = Guild.objects.get(join_code=serializer.validated_data['join_code'])
        except Guild.DoesNotExist:
            return Response(
                {'error': '잘못된 참가 코드입니다.'},
                status=status.HTTP_404_NOT_FOUND
            )
    elif serializer.validated_data.get('guild_id'):
        guild = get_object_or_404(Guild, id=serializer.validated_data['guild_id'])
        if guild.is_private:
            return Response(
                {'error': '비공개 길드는 참가 코드가 필요합니다.'},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    # 가입 가능 여부 확인
    can_join, message = guild.can_join(request.user)
    if not can_join:
        return Response({'error': message}, status=status.HTTP_400_BAD_REQUEST)
    
    # 길드 가입
    GuildMembership.objects.create(
        guild=guild,
        user=request.user,
        role='member'
    )
    
    return Response({
        'message': '길드에 가입했습니다.',
        'guild': GuildSerializer(guild).data
    })


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def leave_guild_view(request, guild_id):
    """길드 탈퇴"""
    membership = get_object_or_404(
        GuildMembership,
        guild_id=guild_id,
        user=request.user,
        status='active'
    )
    
    if membership.role == 'leader':
        # 길드장이 탈퇴하는 경우 다른 멤버에게 권한 이양
        other_members = GuildMembership.objects.filter(
            guild=membership.guild,
            status='active'
        ).exclude(user=request.user)
        
        if other_members.exists():
            # 부길드장을 길드장으로, 없으면 일반 멤버 중 가장 먼저 가입한 사람
            new_leader = other_members.filter(role='officer').first() or other_members.first()
            new_leader.role = 'leader'
            new_leader.save()
    
    membership.status = 'left'
    membership.save()
    
    return Response({'message': '길드에서 탈퇴했습니다.'})


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def my_guild_view(request):
    """내 길드 조회"""
    try:
        membership = GuildMembership.objects.get(user=request.user, status='active')
        return Response({
            'guild': GuildSerializer(membership.guild).data,
            'membership': GuildMembershipSerializer(membership).data
        })
    except GuildMembership.DoesNotExist:
        return Response({'message': '소속된 길드가 없습니다.'}, status=status.HTTP_404_NOT_FOUND)


class GuildMembersView(generics.ListAPIView):
    """길드 멤버 목록"""
    serializer_class = GuildMembershipSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        guild_id = self.kwargs['guild_id']
        return GuildMembership.objects.filter(
            guild_id=guild_id,
            status='active'
        ).order_by('role', 'joined_at')


class GuildQuestListView(generics.ListCreateAPIView):
    """길드 퀘스트 목록/생성"""
    serializer_class = GuildQuestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        guild_id = self.kwargs['guild_id']
        return GuildQuest.objects.filter(guild_id=guild_id).order_by('-created_at')

    def perform_create(self, serializer):
        guild_id = self.kwargs['guild_id']
        guild = get_object_or_404(Guild, id=guild_id)
        
        # 길드장이나 부길드장만 퀘스트 생성 가능
        membership = get_object_or_404(
            GuildMembership,
            guild=guild,
            user=self.request.user,
            status='active'
        )
        
        if membership.role not in ['leader', 'officer']:
            raise serializers.ValidationError('길드 퀘스트는 길드장이나 부길드장만 생성할 수 있습니다.')
        
        serializer.save(guild=guild)


class GuildMessageListView(generics.ListCreateAPIView):
    """길드 메시지 목록/생성"""
    serializer_class = GuildMessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        guild_id = self.kwargs['guild_id']
        return GuildMessage.objects.filter(guild_id=guild_id).order_by('-created_at')

    def perform_create(self, serializer):
        guild_id = self.kwargs['guild_id']
        guild = get_object_or_404(Guild, id=guild_id)
        
        # 길드 멤버만 메시지 작성 가능
        get_object_or_404(
            GuildMembership,
            guild=guild,
            user=self.request.user,
            status='active'
        )
        
        serializer.save(guild=guild, sender=self.request.user)