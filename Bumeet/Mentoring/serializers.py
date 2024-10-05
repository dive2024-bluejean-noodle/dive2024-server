from rest_framework import serializers
from .models import Matching, Comment
from django.shortcuts import get_object_or_404
from User.models import CustomUser

class CommentSerializer(serializers.ModelSerializer):
    writer_username = serializers.SerializerMethodField()  # writer의 username을 반환하는 필드 추가

    class Meta:
        model = Comment
        fields = ['writer_username', 'created_at', 'contents']  # writer 대신 writer_username 사용

    def get_writer_username(self, obj):
        return obj.writer.username  # writer의 username 반환

class MatchingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Matching
        fields = '__all__'

class MatchingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Matching
        fields = '__all__'

    def create(self, validated_data):
        mento_user_id = validated_data['mento']  # mento ID
        mento_user = get_object_or_404(CustomUser, username=mento_user_id)

        if not mento_user.mento:
            raise serializers.ValidationError("당신은 멘토 유저가 아닙니다.")

        # 매칭 생성
        match = Matching(
            mento=mento_user,  # 멘토 사용자 객체
            mentee=validated_data.get('mentee', None),  # ID 대신 인스턴스를 넣지 않음
            title=validated_data['title'],
            location=validated_data['location'],
            match=validated_data.get('match', False)
        )
        match.save()
        return match
    
    def update(self, instance, validated_data):
        # 멘티가 아닌 경우에만 업데이트를 허용
        if not instance.mentee:  # 만약 멘티가 없는 경우
            raise serializers.ValidationError("멘티가 아닌 사용자는 신청할 수 없습니다.")

        # validated_data에서 업데이트할 데이터 가져오기
        instance.match = validated_data.get('match', instance.match)
        instance.mentee = validated_data.get('mentee', instance.mentee)

        # 변경된 인스턴스를 저장
        instance.save()
        return instance

class MatchingListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Matching
        fields = '__all__'

class MatchingDetailSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)  # 댓글을 포함하는 필드 추가
    class Meta:
        model = Matching
        fields = ['mento', 'mentee', 'title', 'created_at', 'location', 'match', 'comments']
    
    def get_mento_username(self, obj):
        return obj.mento.username  # 멘토의 사용자 이름 반환
    
    def get_mentee_username(self, obj):
        return obj.mentee.username
