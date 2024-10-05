# DIVE2024 Server

# API Documentation

## 설치 패키지

- **Django**: 5.0
- **Django REST Framework**: 3.15.2
- **Pillow**: 10.4.0  ← 이미지 업로드를 위한 패키지

## 계정 생성 - `/User/create/`

**요청 본문 예시:**

```json
{
  "first_name": "Bu",
  "last_name": "Meet",
  "username": "busan",
  "password": "busan",
  "email": "busan@test.com",
  "local": null,
  "id_photo": null,
  "language": "Korean",
  "nationality": "Korea",
  "is_active": true,
  "visa_number": "000000003",
  "mento": true, // 한국인은 true 
  "age": 54,
  "sex": "Male"
}
```

## 계정 정보 업데이트 - `/User/update/<str:username>/`

**요청 본문 예시:**

```json
{
  "username": "new_username",
  "email": "new_email@example.com",
  "local": "new_local",
  "id_photo": "new_id_photo_url_or_path",
  "language": "new_language",
  "mento": true,
  "password": "new_password"  // 비밀번호를 업데이트할 경우 포함
}

// 필요한 업데이트만 보내면 됩니다.
```

## 로그인 - `/User/login/`

**요청 본문 예시:**

```json
{
  "username": "test",
  "password": "test"
}
```

## 멘토 멘티

### Mentoring 생성 - `/Mentoring/create/` (POST)

**요청 본문 예시:**

```json
{
  "mento": 1,
  "title": "멘토링 주제 인데스와",
  "location": "부산역",
  "match": false
}
```

### Mentoring 신청 - `/Mentoring/application/<int:pk>/` (PATCH)

**요청 본문 예시:**

```json
{
  "mentee_username": "hmm",
  "mentoring_request": true
}
```

### Mentoring 목록 - `/Mentoring/list/` (GET)

### Mentoring 정보 - `/Mentoring/match/<int:pk>/` (GET)

### 게시글 댓글 작성 - `/match/<int:matching_id>/comment/` (POST)

**요청 본문 예시:**

```json
{
  "contents": "This is comment.",
  "writer": 1 // 사용자 pk
}
```
```

위 내용을 `README.md` 파일에 추가하시면 됩니다!

## 사용 기술
- Django REST Framework
- Python
---

## 설치 방법
1. 이 레포지토리를 클론합니다.
   ```bash
   git clone <repository-url>
   ```
2. 필요한 패키지를 설치합니다.
   ```bash
   pip install -r requirements.txt
   ```
3. 데이터베이스를 설정하고 마이그레이션을 수행합니다.
   ```bash
   python manage.py migrate
   ```
4. 서버를 실행합니다.
   ```bash
   python manage.py runserver
   ```