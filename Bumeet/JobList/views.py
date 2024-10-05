from django.shortcuts import render
import pandas as pd
import os
from .models import Job
from datetime import datetime
from django.conf import settings  # BASE_DIR 사용을 위해 필요
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .serializers import *

# Create your views here.
class JobDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, *args, **kwargs):
        # 데이터가 없으면 404 에러 반환
        obj = get_object_or_404(Job, pk=pk)
        serializer = JobDetailSerializer(obj)
        
        return Response(serializer.data, status=200)

class JobListView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        try:
            objs = Job.objects.all()
            serializer = JobListSerializer(objs, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': e}, status=status.HTTP_404_NOT_FOUND)

def input_data():
    # BASE_DIR 기준으로 파일 경로 설정
    csv_file_path = os.path.join(settings.BASE_DIR, 'JobList', 'csv_data', 'DIVE2024_DATA.csv')
    
    # CSV 파일 읽기
    data = pd.read_csv(csv_file_path, encoding='utf-8')
    
    # 데이터 삽입
    for index, row in data.iterrows():
        # 날짜 변환 (예: "YYYY.MM.DD" 형식에서 DateField로)
        if pd.notna(row['posted_date']):
            posted_date = datetime.strptime(row['posted_date'], '%Y.%m.%d').date()
        else:
            posted_date = None
        
        Job.objects.create(
            title=row['title'],
            company=row['company'],
            location=row['location'],
            description=row['description'],
            ended_date=posted_date
        )