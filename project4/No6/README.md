# 필수과정 4 - 문제6: 질문 기능을 추가해보자

## 파일 구조
```
No6/
├── main.py                           # FastAPI 메인 애플리케이션
├── database.py                       # 데이터베이스 설정 및 연결
├── models.py                         # Question 모델 정의
├── myapi.db                         # SQLite 데이터베이스 파일
├── domain/
│   └── question/
│       └── question_router.py        # 질문 관련 라우터
└── frontend/                        # 프론트엔드 디렉토리
```

## 핵심 기능

### 1. APIRouter를 이용한 모듈화 (question_router.py)
```python
router = APIRouter(prefix='/api/question')

@router.get('/list')
def question_list(db: Session = Depends(get_db)):
    question_list = db.query(Question).order_by(Question.create_date.desc()).all()
    return question_list
```

### 2. 라우터 등록 (main.py)
```python
from domain.question import question_router
app.include_router(question_router.router)
```

## API

### 질문 목록 조회
```bash
GET /api/question/list
```
**응답 예시**:
```json
[
    {
        "id": 1,
        "subject": "화성에서의 연구 결과는?",
        "content": "현재까지의 연구 결과를 알려주세요.",
        "create_date": "2024-09-13T12:00:00"
    }
]
```

## 실행 방법

### 1. 가상환경 활성화
```bash
cd project4
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 2. 서버 실행
```bash
cd No6
python main.py
```

서버가 `http://localhost:8000`에서 실행됩니다.

## API 테스트 방법

### curl 명령어 사용
```bash
# 메인 페이지
curl -X GET "http://localhost:8000/"

# 질문 목록 조회
curl -X GET "http://localhost:8000/api/question/list"
```

### 웹 브라우저 접속
- 질문 목록: `http://localhost:8000/api/question/list`
- API 문서: `http://localhost:8000/docs`

## 기술 스택

- **프레임워크**: FastAPI
- **ORM**: SQLAlchemy
- **데이터베이스**: SQLite
- **라우팅**: APIRouter
- **서버**: uvicorn