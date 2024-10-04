from django.db import models

class Job(models.Model):
    title = models.CharField(max_length=255)  # 채용 공고 제목
    company = models.CharField(max_length=255)  # 회사 이름
    location = models.CharField(max_length=255)  # 근무 위치
    description = models.TextField()  # 채용 공고 설명
    posted_date = models.DateField(auto_now_add=True)  # 게시일

    def __str__(self):
        return self.title
