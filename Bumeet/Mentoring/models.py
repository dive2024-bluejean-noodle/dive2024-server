from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from User.models import CustomUser

class Matching(models.Model):
    mento = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='mentoring',
        limit_choices_to={'mento': True}  # mento=True인 사용자만 선택 가능
    )
    mentee = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='mentees',
        limit_choices_to={'mento': False},  # mento=False인 사용자만 선택 가능
        null=True,
        blank=True
    )
    title = models.CharField(max_length=100, unique=True, null=False, blank=False)  # 주제
    created_at = models.DateTimeField(auto_now_add=True)  # 업로드 일자
    location = models.CharField(max_length=100, null=False, blank=False)  # 만날 장소
    match = models.BooleanField(default=False)  # 매칭 여부

    def __str__(self):
        return f"{self.mento.username} is mentoring {self.mentee.username if self.mentee else 'No Mentee Yet'}"


class Comment(models.Model):
    matching = models.ForeignKey(Matching, on_delete=models.CASCADE, related_name='comments')  # 댓글이 달릴 매칭(글)
    writer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=False, blank=False, related_name='writer')  # 댓글 작성자
    created_at = models.DateTimeField(auto_now_add=True)  # 댓글 생성 시간
    contents = models.TextField(null=False, blank=False)  # 댓글 내용

    def __str__(self):
        return f"Comment by {self.writer.username} on {self.matching.title}"