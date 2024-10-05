from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Matching
from .serializers import *
from django.shortcuts import get_object_or_404
from User.models import CustomUser
from rest_framework.permissions import IsAuthenticated


class MatchingCreateView(APIView):
    permission_classes = [IsAuthenticated]  # 인증된 사용자만 접근 가능

    def post(self, request, *args, **kwargs):
        # 요청 데이터에 인증된 사용자 정보 추가
        data = request.data.copy()  # request.data는 불변이므로 복사
        data['mento'] = request.user.id  # 현재 인증된 사용자의 ID를 멘토로 설정

        serializer = MatchingSerializer(data=data)
        if serializer.is_valid():
            serializer.save()  # 매칭 생성
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MatchingUpdateView(APIView):
    permission_classes = [IsAuthenticated]  # 인증된 사용자만 접근 가능

    def get_object(self, pk):
        return get_object_or_404(Matching, pk=pk)

    def patch(self, request, pk, *args, **kwargs):
        match = self.get_object(pk)

        # 인증된 사용자를 멘티로 설정
        mentee = request.user
        match.mentee = mentee  # 매칭에 멘티 설정

        # 요청 데이터에서 멘토링 요청 추출
        mentoring_request = request.data.get('mentoring_request')
        if mentoring_request:
            match.match = mentoring_request

        serializer = MatchingSerializer(match, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MatchingDeleteView(APIView):
    permission_classes = [IsAuthenticated]  # 인증된 사용자만 접근 가능

    def get_object(self, pk):
        return get_object_or_404(Matching, pk=pk)

    def delete(self, request, pk, *args, **kwargs):
        match = self.get_object(pk)
        
        # 삭제 요청하는 사용자의 ID를 추출
        request_user = request.user  # JWT 인증을 통해 얻은 사용자 객체
        
        # 멘토 또는 멘티가 요청한 사용자와 일치하는지 확인
        if match.mento == request_user or (match.mentee and match.mentee == request_user):
            match.delete()  # 매칭 삭제
            return Response(status=status.HTTP_204_NO_CONTENT)
        
        return Response(
            {"detail": "삭제 권한이 없습니다."}, 
            status=status.HTTP_403_FORBIDDEN
        )

class MatchingListView(APIView):
    permission_classes = [IsAuthenticated]  # 인증된 사용자만 접근 가능

    def get(self, request, *args, **kwargs):
        matching = Matching.objects.all()
        serializer = MatchingListSerializer(matching, many=True)

        # 각 매칭 객체에 멘토와 멘티의 사용자 이름 추가
        for index, match in enumerate(matching):
            serializer.data[index]['mento_username'] = match.mento.username  # 멘토 사용자 이름 추가
            serializer.data[index]['mento_language'] = match.mento.language
            serializer.data[index]['mentee_username'] = match.mentee.username if match.mentee else None  # 멘티 사용자 이름 추가, 멘티가 없는 경우 None
            serializer.data[index]['mentee_language'] = match.mentee.language if  match.mentee else None

        return Response(serializer.data)

class MatchingDetailView(APIView):
    def get(self, request, pk, *args, **kwargs):
        matching = Matching.objects.get(pk=pk)
        serializer = MatchingDetailSerializer(matching)

        # 멘토의 사용자 이름 추가
        response_data = serializer.data
        response_data['mento_username'] = matching.mento.username  # 멘토 사용자 이름 추가
        response_data['mento_language'] = matching.mento.language
        response_data['mentee_username'] = matching.mentee.username if matching.mentee else None
        response_data['mentee_language'] = matching.mentee.language if matching.mentee else None
        return Response(response_data)


class CommentCreateView(APIView):
    permission_classes = [IsAuthenticated]  # 인증된 사용자만 접근 가능

    def post(self, request, matching_id, *args, **kwargs):
        try:
            matching = Matching.objects.get(pk=matching_id)  # 매칭 객체 가져오기
        except Matching.DoesNotExist:
            return Response({"detail": "Matching not found."}, status=status.HTTP_404_NOT_FOUND)
        
        # 현재 인증된 사용자를 writer로 설정
        writer = request.user  

        serializer = CommentSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save(writer=writer, matching=matching)  # writer와 matching 필드를 설정
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)