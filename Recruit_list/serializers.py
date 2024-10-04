from rest_framework import serializers
from .models import Job

class JobSerializer(serializers.ModelSerializer): #모델 데이터를 JSON으로 변환하기 위해
    class Meta:
        model = Job
        fields = ['id', 'title', 'company', 'location', 'description', 'posted_date']
