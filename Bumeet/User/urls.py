from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    # 유저 등록 및 정보 관련
    path('register/', UserCreateView.as_view(), name='user-register'),
    path('update/', UserUpdateView.as_view(), name='user-update'),  # 자신의 정보 업데이트
    path('delete/', UserDeleteView.as_view(), name='user-delete'),  # 대신 자신의 정보 삭제
    path('detail/', UserDetailView.as_view(), name='user-detail'),  # 자신의 정보 조회
    
    # JWT 토큰 발급 및 갱신
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]