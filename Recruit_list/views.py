# views.py (in Recruit_list app)
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Job
from .serializers import JobSerializer

def create_job(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        company = request.POST.get('company')
        location = request.POST.get('location')
        description = request.POST.get('description')

        # ORM을 사용하여 데이터 삽입
        new_job = Job(
            title=title,
            company=company,
            location=location,
            description=description
        )
        new_job.save()  # 데이터베이스에 저장

        # 리디렉션 또는 다른 처리
        return render(request, 'success.html', {'job': new_job})

    return render(request, 'create_job.html')




class JobListView(APIView):
    def get(self, request):
        jobs = Job.objects.all()
        serializer = JobSerializer(jobs, many=True)
        return Response(serializer.data)
