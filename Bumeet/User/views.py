from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import CustomUser
from .serializers import UserSerializer
from django.shortcuts import get_object_or_404

# login
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated

# 유저 생성
class UserCreateView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()  # 사용자 생성
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            # 에러를 분류하여 응답
            error_response = {}
            for field, errors in serializer.errors.items():
                error_response[field] = errors  # 각 필드의 에러를 딕셔너리에 추가
            
            return Response(error_response, status=status.HTTP_400_BAD_REQUEST)

# 유저 정보 업데이트
class UserUpdateView(APIView):
    permission_classes = [IsAuthenticated]  # 인증된 사용자만 접근 가능

    def patch(self, request, *args, **kwargs):
        user = request.user  # 현재 로그인된 사용자 정보 가져오기
        serializer = UserSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            # 에러를 세분화하여 응답
            error_response = {}
            for field, errors in serializer.errors.items():
                error_response[field] = errors
            
            return Response(error_response, status=status.HTTP_400_BAD_REQUEST)

# 유저 삭제(deactive)
class UserDeleteView(APIView):
    permission_classes = [IsAuthenticated]  # 인증된 사용자만 접근 가능

    def delete(self, request, *args, **kwargs):
        user = request.user  # 현재 로그인된 사용자 정보 가져오기

        if not user.is_active:
            return Response({'error': '사용자는 이미 비활성화되어 있습니다.'}, status=status.HTTP_400_BAD_REQUEST)

        user.is_active = False  # Soft delete를 위해 active 상태를 비활성화
        user.save()
        return Response(status=status.HTTP_200_OK)


class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]  # 인증된 사용자만 접근 가능

    def get(self, request, *args, **kwargs):
        user = request.user  # 현재 로그인된 사용자 정보 가져오기
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)