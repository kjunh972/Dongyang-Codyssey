# 필수과정 4 - 문제7: 또 다시 알 수 없는 오류

## 개요
contextlib을 이용한 의존성 주입과 Pydantic 스키마를 활용하여 데이터베이스 세션 관리를 개선한 프로젝트입니다. 데이터베이스 연결과 종료를 자동으로 관리하여 리소스 누수를 방지합니다.

## 파일 구조
```
No7/
├── main.py                              # FastAPI 메인 애플리케이션
├── database.py                          # contextlib 기반 DB 세션 관리
├── models.py                            # Question 모델 정의
├── schemas.py                           # Pydantic 응답 스키마
├── myapi.db                             # SQLite 데이터베이스 파일
├── domain/
│   └── question/
│       └── question_router.py           # 개선된 질문 라우터
├── frontend/                            # 프론트엔드 디렉토리
└── README.md                            # 이 파일
```

## 개선사항

### 1. contextlib을 이용한 데이터베이스 세션 관리 (database.py)
```python
from contextlib import contextmanager

@contextmanager
def get_db_context():
    db = SessionLocal()
    try:
        print('데이터베이스 연결 시작')
        yield db
    finally:
        print('데이터베이스 연결 종료')
        db.close()

# Depends를 위한 데이터베이스 세션 함수
def get_db():
    db = SessionLocal()
    try:
        print('데이터베이스 연결 시작')
        yield db
    finally:
        print('데이터베이스 연결 종료')
        db.close()
```

### 2. Pydantic 스키마 정의 (schemas.py)
```python
from pydantic import BaseModel
from datetime import datetime

class QuestionResponse(BaseModel):
    id: int
    subject: str
    content: str
    create_date: datetime

    class Config:
        from_attributes = True
```

### 3. 개선된 질문 라우터 (question_router.py)
```python
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from schemas import QuestionResponse
from typing import List

@router.get('/list', response_model=List[QuestionResponse])
def question_list(db: Session = Depends(get_db)):
    question_list = db.query(Question).order_by(Question.create_date.desc()).all()
    return question_list
```

## API 엔드포인트

### 질문 목록 조회
```bash
GET /api/question/list
```

**응답 스키마**:
```json
[
    {
        "id": 1,
        "subject": "질문 제목",
        "content": "질문 내용",
        "create_date": "2024-09-16T12:00:00"
    }
]
```

## 실행 방법

### 1. 가상환경 활성화
```bash
cd project4
source venv/bin/activate  
```

### 2. 서버 실행
```bash
cd No7
python main.py
```

서버가 `http://localhost:8000`에서 실행됩니다.

## API 테스트 방법

### curl 명령어 사용
```bash
# 질문 목록 조회 (콘솔에서 DB 연결/종료 메시지 확인)
curl -X GET "http://localhost:8000/api/question/list"

# 메인 페이지
curl -X GET "http://localhost:8000/"
```

### 데이터베이스 연결 확인
API 호출 시 서버 콘솔에서 다음 메시지를 확인할 수 있습니다:
```
데이터베이스 연결 시작
데이터베이스 연결 종료
```

### 웹 브라우저 접속
- 메인 페이지: `http://localhost:8000`
- 질문 목록: `http://localhost:8000/api/question/list`
- API 문서: `http://localhost:8000/docs`

- **개선**: 콘솔 로그로 명확한 상태 확인

## 기술 스택

- **프레임워크**: FastAPI
- **ORM**: SQLAlchemy
- **데이터베이스**: SQLite
- **스키마**: Pydantic
- **세션 관리**: contextlib
- **의존성 주입**: FastAPI Depends