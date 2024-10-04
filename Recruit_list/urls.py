from django.urls import path
from .views import JobListView

urlpatterns = [ #API 엔드포인트 설정
    path('jobs/', JobListView.as_view(), name='job-list'),
]
