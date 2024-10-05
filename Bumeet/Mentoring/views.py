from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Matching
from .serializers import *
from django.shortcuts import get_object_or_404
from User.models import CustomUser


class MatchingCreateView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = MatchingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # 매칭 생성
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MatchingUpdateView(APIView):
    def get_object(self, pk):
        return get_object_or_404(Matching, pk=pk)

    def patch(self, request, pk, *args, **kwargs):
        match = self.get_object(pk)

        # 요청 데이터에서 username 추출
        mentee_username = request.data.get('mentee_username')
        mentoring_request = request.data.get('mentoring_request')
        if mentee_username:
            # username으로 멘티 찾기
            mentee = get_object_or_404(CustomUser, username=mentee_username)
            match.mentee = mentee  # 매칭에 멘티 설정
            match.match = mentoring_request

        serializer = MatchingSerializer(match, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# 요청 json 형태
# {
#     "mentee_username": "some_mentee_username",
#     "match": true  // 또는 다른 필드 업데이트
# }

# class MatchingDeleteView(APIView):
#     def get_object(self, pk):
#         return get_object_or_404(Matching, pk=pk)

#     def delete(self, request, pk, *args, **kwargs):
#         match = self.get_object(pk)
        
#         # 삭제 요청하는 사용자의 username 추출
#         request_username = request.data.get('request_username')

#         # 멘토의 username과 요청하는 사용자의 username 비교
#         if match.mento.username == request_username:
#             match.delete()  # 매칭 삭제
#             return Response(status=status.HTTP_204_NO_CONTENT)
        
#         return Response(
#             {"detail": "삭제 권한이 없습니다."}, 
#             status=status.HTTP_403_FORBIDDEN
#         )

class MatchingDeleteView(APIView):
    def get_object(self, pk):
        return get_object_or_404(Matching, pk=pk)

    def delete(self, request, pk, *args, **kwargs):
        match = self.get_object(pk)
        
        # 삭제 요청하는 사용자의 username을 쿼리 매개변수로 추출
        request_username = request.query_params.get('request_username')

        # 멘토의 username과 요청하는 사용자의 username 비교
        if match.mento.username == request_username:
            match.delete()  # 매칭 삭제
            return Response(status=status.HTTP_204_NO_CONTENT)
        
        return Response(
            {"detail": "삭제 권한이 없습니다."}, 
            status=status.HTTP_403_FORBIDDEN
        )

class MatchingListView(APIView):
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
    def post(self, request, matching_id, *args, **kwargs):
        try:
            matching = Matching.objects.get(pk=matching_id)  # 매칭 객체 가져오기
        except Matching.DoesNotExist:
            return Response({"detail": "Matching not found."}, status=status.HTTP_404_NOT_FOUND)

        writer_id = request.data.get('writer')  # 요청에서 작성자 ID를 가져옴
        if not writer_id:
            return Response({"detail": "Writer ID is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            writer = CustomUser.objects.get(pk=writer_id)  # 작성자 객체 가져오기
        except CustomUser.DoesNotExist:
            return Response({"detail": "No CustomUser matches the given writer ID."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = CommentSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save(writer=writer, matching=matching)  # writer와 matching 필드를 설정
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)