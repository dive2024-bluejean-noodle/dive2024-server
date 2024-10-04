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

# 유저 생성
class UserCreateView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # 사용자 생성
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 유저 정보 업데이트
class UserUpdateView(APIView):
    def get_object(self, username):
        return get_object_or_404(CustomUser, username=username)

    def patch(self, request, username, *args, **kwargs):
        user = self.get_object(username)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 유저 삭제(deactive)
class UserDeleteView(APIView):
    def get_object(self, username):
        return get_object_or_404(CustomUser, username=username)

    def patch(self, request, username, *args, **kwargs):
        user = self.get_object(username)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserDetailView(APIView):
    def get_object(self, username):
        return get_object_or_404(CustomUser, username=username)

    def get(self, request, username, *args, **kwargs):
        user = self.get_object(username)
        serializer = UserSerializer(user)
        return Response(serializer.data)

class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')  # 사용자 이름
        password = request.data.get('password')   # 비밀번호

        user = authenticate(username=username, password=password)  # 사용자 인증

        if user is not None:
            return Response({'message': '로그인 성공!'}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': '아이디 또는 비밀번호가 올바르지 않습니다.'}, status=status.HTTP_401_UNAUTHORIZED)