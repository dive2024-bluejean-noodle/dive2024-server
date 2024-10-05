from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
import requests
import httpx

class ResponseRentalHousingView(APIView):
    permission_classes = [IsAuthenticated]  # 인증이 필요하다면 주석을 해제하세요.
    
    def get(self, request, pageNo, rows, *args, **kwargs):
        api_key = ''
        url = f'https://apis.data.go.kr/B551922/BMC_SERVICE/HOUSELIST?serviceKey={api_key}&pageNo={pageNo}&numOfRows={rows}'

        # GET 요청 보내기
        response = httpx.get(url, verify=False)

        # 응답 데이터 확인
        if response.status_code == 200:
            print('Success:', response.json())  # JSON 응답일 경우
            return Response({'data': response.json()}, status=200)  # JSON 형태로 응답 반환
        else:
            print('Failed:', response.status_code)
            return Response({'error': 'Failed to fetch data'}, status=response.status_code)  # 오류 응답 반환
