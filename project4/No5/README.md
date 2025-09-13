# 필수과정 4 - 문제5: 데이터베이스를 또...

## 개요
SQLAlchemy ORM과 Alembic을 활용한 게시판 시스템의 데이터베이스 구축 프로젝트입니다. 메모리 기반 리스트에서 SQLite 데이터베이스로 영구 저장소를 변경했습니다.

## 파일 구조
```
No5/
├── main.py                    # FastAPI 메인 애플리케이션
├── database.py               # 데이터베이스 설정 및 연결
├── models.py                 # Question 모델 정의
├── domain/
│   └── question/            # 질문 도메인 디렉토리
├── frontend/                # 프론트엔드 디렉토리
├── alembic/                 # Alembic 마이그레이션 관리
│   ├── versions/            # 마이그레이션 파일들
│   └── env.py              # Alembic 환경 설정
├── alembic.ini             # Alembic 설정 파일
├── myapi.db                # SQLite 데이터베이스 파일
└── README.md               # 이 파일
```

## 데이터 모델

### Question 모델 (models.py)
```python
class Question(Base):
    __tablename__ = 'question'
    
    id = Column(Integer, primary_key=True)           # 질문 고유번호
    subject = Column(String, nullable=False)         # 질문 제목
    content = Column(Text, nullable=False)           # 질문 내용
    create_date = Column(DateTime, nullable=False)   # 질문 작성일시
```

## 구현된 기능

### 1. 데이터베이스 설정 (database.py)
- SQLite 데이터베이스 연결
- SQLAlchemy ORM 설정
- 세션 관리 (autocommit=False)

### 2. FastAPI 애플리케이션 (main.py)
- 기본 API 엔드포인트
- 데이터베이스 세션 의존성 주입
- 질문 목록 조회 API

### 3. Alembic 마이그레이션
- 데이터베이스 스키마 버전 관리
- Question 테이블 생성 마이그레이션

## 실행 방법

### 1. 의존성 설치
```bash
pip install fastapi uvicorn sqlalchemy alembic
```

### 2. 서버 실행
```bash
cd project4/No5
python main.py
```

서버가 `http://localhost:8000`에서 실행됩니다.

## API 엔드포인트

### 메인 페이지
```bash
curl -X GET "http://localhost:8000/"
```

### 질문 목록 조회
```bash
curl -X GET "http://localhost:8000/question/list"
```

## 데이터베이스 관리

### 테이블 확인
```bash
# 모든 테이블 목록
sqlite3 myapi.db ".tables"

# Question 테이블 스키마
sqlite3 myapi.db ".schema question"

# 모든 스키마 확인
sqlite3 myapi.db ".schema"
```

### 데이터 조회
```bash
# Question 테이블 데이터 조회
sqlite3 myapi.db "SELECT * FROM question;"

# 레코드 개수 확인
sqlite3 myapi.db "SELECT COUNT(*) FROM question;"
```

## 기술 스택

- **프레임워크**: FastAPI
- **ORM**: SQLAlchemy
- **데이터베이스**: SQLite
- **마이그레이션**: Alembic
- **서버**: uvicorn