from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
import os

LANGUAGE_CHOICES = [
    ('Korean', 'Korean'),
    ('English', 'English'),
    ('Japanese', 'Japanese'),
    ('Chinese', 'Chinese'),
]

NATIONALITY_CHOICES = [
    ('Korea', 'Korea'),
    ('USA', 'USA'),
    ('Japan', 'Japan'),
    ('China', 'China'),
]

SEX_CHOICES = [
    ('Male', 'Male'),
    ('Female', 'Female'),
]

def user_directory_path(instance, filename):
    # 인스턴스에서 사용자 이름을 가져옵니다.
    username = instance.username
    # 파일 경로를 생성합니다.
    return os.path.join('photos', username, filename)

class CustomUser(AbstractUser):
    visa_number = models.CharField(max_length=9, null=False, blank=False) # 비자넘버는 보통 9자리
    age = models.IntegerField(
        validators=[MinValueValidator(18), MaxValueValidator(100)],
        null=False, blank=False
    )
    sex = models.CharField(max_length=6, choices=SEX_CHOICES, default='Male')
    mento = models.BooleanField(default=False)  # 멘토 여부
    local = models.CharField(max_length=30, null=True, blank=True)  # 지역 여부
    id_photo = models.ImageField(upload_to=user_directory_path, null=True, blank=True)  # 프로필 사진
    language = models.CharField(max_length=20, choices=LANGUAGE_CHOICES, default='Korean')
    nationality = models.CharField(max_length=30, choices=NATIONALITY_CHOICES, default='Korea')

    def __str__(self):
        return self.username

