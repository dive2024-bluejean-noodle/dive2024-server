# DIVE2024 Server

# API Documentation
## API 정리

### 계정 생성

- **Method**: POST
- **Endpoint**: /User/register/
- **Response**: 계정정보
- **JSON Example**:
    ```json
    {
        "first_name": "Bu",
        "last_name": "Meet",
        "username": "seoul",
        "password": "seoul",
        "email": "seoul@test.com",
        "local": null,
        "id_photo": null,
        "language": "Japanese",
        "nationality": "Korea",
        "is_active": true,
        "visa_number": "000000003",
        "mento": true,
        "age": 54,
        "sex": "Male"
    }
    ```

### 로그인

- **Method**: POST
- **Endpoint**: User/api/token/
- **Response**: 엑세스, 리프래쉬 토큰
- **JSON Example**:
    ```json
    {
        "username": "seoul",
        "password": "seoul"
    }
    ```

### 정보 조회

- **Method**: GET
- **Endpoint**: User/detail/
- **Response**: 계정정보
- **JSON Example (Header)**:
    ```json
    {
        "Authorization": "Bearer <access token>"
    }
    ```

### 정보 업데이트

- **Method**: PATCH
- **Endpoint**: User/update/
- **Response**: 계정정보
- **JSON Example**:
    ```json
    {
        // Header
        "Authorization": "Bearer <access token>"
    }
    // Body
    {
        "username": "new_username",
        "email": "new_email@example.com",
        "local": "new_local",
        "id_photo": "new_id_photo_url_or_path",
        "language": "new_language",
        "mento": true,
        "password": "new_password"  // 비밀번호를 업데이트할 경우 포함
    }
    // 필요한 업데이트만 보내면 됨
    ```

### 멘토링 생성

- **Method**: POST
- **Endpoint**: Mentoring/create/
- **Response**: 매칭 정보
- **JSON Example**:
    ```json
    {
        // Header
        "Authorization": "Bearer <access token>"
    }
    // Body
    {
        "title": "테스트용",
        "location": "테스트용",
        "match": false
    }
    ```

### 멘토링 목록

- **Method**: GET
- **Endpoint**: Mentoring/list/
- **Response**: 멘토링 목록
- **JSON Example**:
    ```json
    {
        // Header
        "Authorization": "Bearer <access token>"
    }
    ```

### 멘토링 상세

- **Method**: GET
- **Endpoint**: Mentoring/match/<int:pk>
- **Response**: 멘토링 상세 정보
- **JSON Example**:
    ```json
    {
        // Header
        "Authorization": "Bearer <access token>"
    }
    ```

### 멘토링 신청

- **Method**: PATCH
- **Endpoint**: Mentoring/application/<int:pk>
- **Response**: 멘토링 정보
- **JSON Example**:
    ```json
    {
        // Header
        "Authorization": "Bearer <access token>"
    }
    // Body
    {
        "mentoring_request": true
    }
    ```

### 멘토링 삭제

- **Method**: DELETE
- **Endpoint**: Mentoring/delete/<int:pk>
- **Response**: NULL
- **JSON Example**:
    ```json
    {
        // Header
        "Authorization": "Bearer <access token>"
    }
    ```

### 멘토링 글에 댓글 남기기

- **Method**: POST
- **Endpoint**: Mentoring/match/<int:pk>/comment/
- **Response**: 댓글 정보
- **JSON Example**:
    ```json
    {
        // Header
        "Authorization": "Bearer <access token>"
    }
    // Body
    {
        "contents": "Test comment."
    }
    ```

### 챗봇

- **Method**: POST
- **Endpoint**: chat/query/
- **Response**:
    ```json
    {
        "results": {
            "generate": {
                "question": "부산역 음식점을 추천해줘",
                "generation": "부산역 근처 맛집으로는 던킨도넛과 영동밀면영동국밥이 추천됩니다. 던킨도넛은 부산역광장 근처에 위치하고, 영동밀면영동국밥은 부산역에서 시원한 밀면과 돼지국밥을 즐길 수 있는 곳입니다. 도보 이동 가능한 거리에 위치한 본전돼지국밥도 인기있는 음식점 중 하나입니다.",
                "documents": [
                    [
                        [
                            "id",
                            null
                        ],
                        [
                            "metadata",
                            {}
                        ],
                        [
                            "page_content",
                            "부산역 근처에 위치한 맛집 10곳을 추천해드립니다. 부산여행의 시작점인 부산역에서 여행의 시작과 끝에 방문하기에 좋은 곳들로 선정하였습니다. 돼지국밥, 밀면 맛집, 노포맛집, 어묵 맛집 등 다양한 메뉴의 맛집들을 소개해드립니다. 더불어 열차시간에 쫓기지 않도록 도보 이동가능한 거리의 ...\n부산은 해안도시로서 신선한 해산물과 풍부한 한국 전통 음식을 맛볼 수 있는 곳입니다. 특히 부산역 주변에는 맛있는 음식점들이 많이 있어서 많은 이들이 그들만의 추천 맛집을 찾고 있습니다. 오늘은 부산역 주변에서 인기있는 베스트10 맛집을 소개하려고 합니다. 각 음식점의 특징과 맛을 ...\n부산역광장 근처 맛집. 부산 동구 중앙대로 200 (우) 48760. 부산역광장에 대한 리뷰 보기. 던킨도너츠. 부산에 있는 음식점 5,286곳 중 694위. 10건의 리뷰. 중앙대로 206. 부산역광장에서 0.1 km. \" 던킨도넛 \" 2018/06/11.\n2 영동밀면영동국밥 두번째 부산역 근처 추천맛집은 영동밀면영동국밥입니다. 시원한 부산식 밀면과 뜨끈한 돼지국밥은 부산 여행의 시작과 끝을 알리는 부산 대표음식인데 한 곳에서 두 가지 다 맛볼 수 있는 곳으로서 냉면과 돼지국밥 맛은 현지인들에게도 검증을 받은 찐 로컬맛집 입니다.\n부산역 관광안내센터에 대한 리뷰 보기. 본전돼지국밥. 부산에 있는 음식점 5,284곳 중 14위. 143건의 리뷰. 동구 초량3동 1200-6번지. 부산역 관광안내센터에서 0.2 km. \" 접근성 좋은 돼지국밥 \" 2021/12/06. \" 창렬함의 끝 \" 2020/01/11. 음식: 아시아 요리, 한국, 수프."
                        ],
                        [
                            "type",
                            "Document"
                        ]
                    ]
                ]
            }
        }
    }
    ```

- **JSON Example**:
    ```json
    {
        // Body
        "question": "내용"
    }
    ```

### 임대주택 데이터

- **Method**: GET
- **Endpoint**: RentalHousing/rental_api/<int:num>/<int:num>/
- **Response Example**:
    ```json
    {
        "data": {
            "response": {
                "header": {
                    "resultCode": "00",
                    "resultMsg": "SUCCESS (조회 성공)"
                },
                "body": {
                    "pageNo": 1,
                    "dataType": "JSON",
                    "totalCount": "366",
                    "numOfRows": 1,
                    "items": {
                        "item": [
                            {
                                "MGMT_NM": "개금2영구임대아파트",
                                "CNT": "990",
                                "GB": "영구임대",
                                "LOCATE": "부산광역시 부산진구 백양관문로77번길 145  (개금동, 개금2지구 도개공영구임대아파트)"
                            }
                        ]
                    }
                }
            }
        }
    }
    ```

### 일자리 리스트

- **Method**: GET
- **Endpoint**: JobList/joblist/
- **Response**:
    ```json
    [
        {
            "title": "I'd like to invite someone who wants to work as a foreign student",
            "company": "씨플랜(C-Plan)",
            "ended_date": "2024-10-24"
        },
        {
            "title": "Recruitment of contract workers (Korean Language and Culture Education Center)",
            "company": "Pusan National University of Foreign Studies",
            "ended_date": "2024-10-11"
        }
    ]
    ```

### 특정 일자리 조회

- **Method**: GET
- **Endpoint**: JobList/job/1
- **Response**:
    ```json
    {
        "id": 1,
        "title": "I'd like to invite someone who wants to work as a foreign student",
        "company": "씨플랜(C-Plan)",
        "location": "411 Suyeong-ro, Suyeong-gu, Busan",
        "description": "Our company conducts employment education and cultural exchange meetings for foreign students, and helps foreigners adapt to Korea.",
        "ended_date": "2024-10-24"
    }
    ```

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

  ---