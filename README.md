# HealthQuest 2.0

건강한 삶을 위한 개인 맞춤형 RPG 건강 관리 웹서비스

## 프로젝트 개요

HealthQuest는 게임 요소를 활용하여 건강 관리를 재미있게 만드는 웹 서비스입니다. 사용자는 자신만의 캐릭터를 성장시키면서 실제 건강 습관을 개선할 수 있습니다.

### 핵심 기능

- **8개 세분화 스탯 시스템**: 체력, 근력, 정신력, 지구력, 심폐, 유연성, 영양, 회복
- **개인 맞춤 퀘스트**: AI 기반 추천으로 사용자에게 최적화된 건강 퀘스트 제공
- **길드 시스템**: 4-8명 소규모 팀으로 함께 도전하고 동기부여
- **실시간 진행 상황 추적**: 연속 완료 기록, 성취도 분석
- **보상 시스템**: 경험치, 골드, 젬, 칭호, 스킨 등 다양한 보상

## 기술 스택

### Backend
- **Django 4.2** + **Django REST Framework**
- **PostgreSQL** (메인 데이터베이스)
- **Redis** (캐싱, 실시간 기능)
- **Celery** (백그라운드 작업)
- **JWT** (인증)

### Frontend
- **React 18** + **TypeScript**
- **Vite** (빌드 도구)
- **Tailwind CSS** (스타일링)
- **Axios** (HTTP 클라이언트)
- **React Router** (라우팅)

### Infrastructure
- **Docker** + **Docker Compose**
- **Python 3.11** + **Node.js 20**

## 빠른 시작

### 1. 요구사항
- Docker 및 Docker Compose
- Node.js 20+ (프론트엔드 로컬 개발 시)
- Python 3.11+ (백엔드 로컬 개발 시)

### 2. 프로젝트 클론 및 실행

```bash
# 프로젝트 클론
git clone <repository-url>
cd healthQuest

# Docker 컨테이너 실행
docker-compose up --build -d

# 원클릭 개발 환경 설정 (추천)
docker-compose exec web python manage.py setup_dev

# 또는 개별 설정:
# docker-compose exec web python manage.py migrate
# docker-compose exec web python manage.py create_admin  
# docker-compose exec web python manage.py create_test_users
# docker-compose exec web python manage.py create_sample_quests
```

### 3. 서비스 접속

- **프론트엔드**: http://localhost:3000
- **API 서버**: http://localhost:8000
- **Django Admin**: http://localhost:8000/admin (admin / admin123)
- **데이터베이스**: localhost:5433
- **Redis**: localhost:6380

### 4. 테스트 계정 (선택사항)

빠른 테스트를 위해 미리 생성된 계정들:

| 이메일 | 비밀번호 | 닉네임 | 특징 |
|--------|----------|--------|------|
| user1@test.com | 1234 | 건강왕 | 활발한 남성 |
| user2@test.com | 1234 | 운동러버 | 매우 활발한 여성 |
| user3@test.com | 1234 | 요가마스터 | 요가 전문 여성 |
| user4@test.com | 1234 | 헬스킹 | 헬스 전문 남성 |
| user5@test.com | 1234 | 다이어터 | 다이어트 중인 여성 |
| user6@test.com | 1234 | 마라토너 | 달리기 전문 남성 |
| user7@test.com | 1234 | 필라테스퀸 | 필라테스 전문 여성 |
| user8@test.com | 1234 | 수영선수 | 수영 전문 남성 |
| user9@test.com | 1234 | 명상러 | 명상 전문가 |
| user10@test.com | 1234 | 초보자 | 운동 초보자 |

**사용법**: 프론트엔드에서 위 이메일과 비밀번호로 바로 로그인하여 테스트할 수 있습니다!

## API 문서

### 인증 API
- `POST /api/auth/register/` - 회원가입
- `POST /api/auth/login/` - 로그인
- `POST /api/auth/logout/` - 로그아웃
- `POST /api/auth/token/refresh/` - 토큰 갱신
- `GET /api/auth/me/` - 현재 사용자 정보
- `PUT /api/auth/profile/` - 프로필 수정

### 캐릭터 API
- `GET /api/characters/` - 캐릭터 정보 조회
- `PUT /api/characters/` - 캐릭터 정보 수정
- `GET /api/characters/stats/` - 스탯 조회
- `GET /api/characters/stats-history/` - 스탯 변화 기록
- `GET /api/characters/achievements/` - 업적 목록

### 퀘스트 API
- `GET /api/quests/` - 퀘스트 목록
- `GET /api/quests/{id}/` - 퀘스트 상세
- `POST /api/quests/{id}/start/` - 퀘스트 시작
- `POST /api/quests/{id}/complete/` - 퀘스트 완료
- `GET /api/quests/daily/` - 오늘의 퀘스트
- `GET /api/quests/streak/` - 연속 완료 기록
- `GET /api/quests/completions/` - 완료 기록

### 길드 API
- `GET /api/guilds/` - 길드 목록
- `POST /api/guilds/create/` - 길드 생성
- `POST /api/guilds/join/` - 길드 가입
- `GET /api/guilds/my/` - 내 길드 정보
- `GET /api/guilds/{id}/members/` - 길드 멤버 목록
- `GET /api/guilds/{id}/quests/` - 길드 퀘스트
- `GET /api/guilds/{id}/messages/` - 길드 메시지

## 테스트

### API 테스트 실행
```bash
# 통합 API 테스트
python3 test_api.py

# Django 테스트
docker-compose exec web python manage.py test
```

### 수동 API 테스트 예시
```bash
# 회원가입
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "username": "testuser",
    "nickname": "테스트유저",
    "password": "testpass123",
    "password_confirm": "testpass123",
    "gender": "male",
    "height": 175,
    "weight": 70,
    "activity_level": "moderate"
  }'

# 로그인
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "testpass123"
  }'

# 캐릭터 정보 조회 (토큰 필요)
curl -X GET http://localhost:8000/api/characters/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## 프로젝트 구조

```
healthQuest/
├── apps/                          # Django 앱들
│   ├── accounts/                  # 사용자 계정 관리
│   ├── characters/                # 캐릭터 및 스탯 관리
│   ├── quests/                    # 퀘스트 시스템
│   └── guilds/                    # 길드 및 소셜 기능
├── healthquest/                   # Django 설정
├── static/                        # 정적 파일
├── docker-compose.yml             # Docker 구성
├── Dockerfile                     # Docker 이미지 정의
├── requirements.txt               # Python 의존성
├── test_api.py                   # API 테스트 스크립트
└── CLAUDE.md                     # 개발 가이드
```

## 게임 시스템

### 캐릭터 성장
- **레벨업**: 퀘스트 완료로 경험치 획득
- **스탯 증가**: 퀘스트 유형에 따른 스탯 향상
- **보상**: 골드, 젬, 칭호, 스킨 획득

### 퀘스트 카테고리
- **Morning**: 기상 후 활동
- **Work**: 업무/학습 시간 활동
- **Evening**: 퇴근 후 활동
- **Night**: 취침 전 활동
- **Weekly**: 주간 장기 목표
- **Challenge**: 월간 특별 도전

### 길드 시스템
- **소규모 팀**: 4-8명으로 구성
- **협력 중심**: 경쟁보다 함께 성장
- **팀 퀘스트**: 공동 목표 달성
- **실시간 소통**: 응원 메시지 교환

## 개발 명령어

```bash
# 컨테이너 상태 확인
docker-compose ps

# 로그 확인
docker-compose logs web
docker-compose logs celery

# Django 관리 명령
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py collectstatic
docker-compose exec web python manage.py shell

# 개발 서버 재시작
docker-compose restart web

# 전체 재빌드
docker-compose down
docker-compose up --build -d
```

## 향후 계획

### Phase 2 (프론트엔드)
- React 18 + TypeScript 웹 앱
- PWA 지원으로 모바일 최적화
- 실시간 대시보드 및 통계

### Phase 3 (AI 개인화)
- 사용자 패턴 분석 기반 퀘스트 추천
- 개인 맞춤 난이도 조절
- 건강 예측 모델링

### Phase 4 (확장 기능)
- 웨어러블 디바이스 연동
- 소셜 기능 강화
- 전문가 상담 연결

## 기여하기

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.

## 문의

프로젝트 관련 문의사항이 있으시면 이슈를 등록해 주세요.

---

**"사용자와 함께 성장하는 살아있는 서비스"**

*건강한 삶을 게임처럼 재미있게, HealthQuest와 함께하세요!*