from rest_framework import serializers
from .models import Job


class JobDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = '__all__'

class JobListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ['title', 'company', 'ended_date']