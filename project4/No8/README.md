# 필수과정 4 - 문제8: 질문을 올려봐

## 개요
질문 등록 기능을 추가하여 완전한 질문 시스템을 구현한 프로젝트입니다. QuestionCreate 스키마를 통해 빈 값 검증을 수행하고, POST 메소드로 새로운 질문을 등록할 수 있습니다.

## 파일 구조
```
No8/
├── main.py                              # FastAPI 메인 애플리케이션
├── database.py                          # contextlib 기반 DB 세션 관리
├── models.py                            # Question 모델 정의
├── schemas.py                           # Pydantic 스키마 (QuestionCreate, QuestionResponse)
├── myapi.db                             # SQLite 데이터베이스 파일
├── domain/
│   └── question/
│       └── question_router.py           # 질문 조회 및 등록 라우터
└── README.md                            # 이 파일
```

## API 엔드포인트

### 질문 목록 조회
```bash
GET /api/question/list
```

### 질문 등록
```bash
POST /api/question/create
```

**요청 스키마**:
```json
{
    "subject": "질문 제목",
    "content": "질문 내용"
}
```

**응답 스키마**:
```json
{
    "id": 6,
    "subject": "질문 제목",
    "content": "질문 내용",
    "create_date": "2024-09-16T17:00:00"
}
```

## 실행 방법

### 1. 가상환경 활성화
```bash
cd project4
source venv/bin/activate  
```

### 2. 서버 실행
```bash
cd No8
python main.py
```

서버가 `http://localhost:8000`에서 실행됩니다.

## API 테스트 방법

### curl 명령어를 사용한 질문 등록 테스트
```bash
# 질문 등록
curl -X POST "http://localhost:8000/api/question/create" \
     -H "Content-Type: application/json" \
     -d '{
         "subject": "새로운 질문",
         "content": "이것은 테스트 질문입니다."
     }'

# 질문 목록 조회 
curl -X GET "http://localhost:8000/api/question/list"
```

### 빈 값 검증 테스트
```bash
# 제목이 빈 값인 경우 (에러 발생)
curl -X POST "http://localhost:8000/api/question/create" \
     -H "Content-Type: application/json" \
     -d '{
         "subject": "",
         "content": "내용만 있는 질문"
     }'

# 내용이 빈 값인 경우 (에러 발생)
curl -X POST "http://localhost:8000/api/question/create" \
     -H "Content-Type: application/json" \
     -d '{
         "subject": "제목만 있는 질문",
         "content": ""
     }'
```


### 웹 브라우저 접속
- 메인 페이지: `http://localhost:8000`
- 질문 목록: `http://localhost:8000/api/question/list`
- API 문서: `http://localhost:8000/docs`

## 기술 스택

- **프레임워크**: FastAPI
- **ORM**: SQLAlchemy
- **데이터베이스**: SQLite
- **스키마**: Pydantic (validation 포함)
- **세션 관리**: contextlib
- **의존성 주입**: FastAPI Depends