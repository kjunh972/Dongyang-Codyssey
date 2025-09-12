# 필수과정 4 - 문제3: 완전히 작동하는 Todo

## 개요
FastAPI를 사용하여 구현한 Todo api입니다. CSV 파일을 데이터베이스로 사용하여 할 일을 관리합니다.

## 파일 구조
```
No3/
├── todo.py          # 메인 FastAPI 애플리케이션
├── model.py         # TodoItem 모델 정의
├── todos.csv        # 데이터 저장 파일
└── README.md        # 리드미
```

## 구현된 기능

### 1. 개별 조회 
- **엔드포인트**: `GET /todo/{todo_id}`
- **함수명**: `get_single_todo()`
- **설명**: 특정 ID의 할 일을 조회합니다.

### 2. 수정 
- **엔드포인트**: `PUT /todo/update/{todo_id}`
- **함수명**: `update_todo()`
- **설명**: 특정 ID의 할 일 내용을 수정합니다.
- **요청 본문**: TodoItem 모델 사용

### 3. 삭제
- **엔드포인트**: `DELETE /todo/delete/{todo_id}`
- **함수명**: `delete_single_todo()`
- **설명**: 특정 ID의 할 일을 삭제합니다.

### 4. 기존 기능
- **추가**: `POST /todo/add`
- **전체 조회**: `GET /todo`

## 데이터 모델

### TodoItem (model.py)
```python
class TodoItem(BaseModel):
    content: str  # 할 일 내용
```

## 실행 방법

1. **서버 실행**:
```bash
cd project4/No3
python todo.py
```

2. **서버 확인**:
서버가 `http://localhost:8000`에서 실행됩니다.

## API 사용 예제

### 할 일 추가
```bash
curl -X POST "http://localhost:8000/todo/add" \
  -H "Content-Type: application/json" \
  -d '{"content": "새로운 할 일"}'
```

### 전체 목록 조회
```bash
curl -X GET "http://localhost:8000/todo"
```

### 개별 조회
```bash
curl -X GET "http://localhost:8000/todo/1"
```

### 수정
```bash
curl -X PUT "http://localhost:8000/todo/update/1" \
  -H "Content-Type: application/json" \
  -d '{"content": "수정된 할 일"}'
```

### 삭제
```bash
curl -X DELETE "http://localhost:8000/todo/delete/1"
```

## 응답 형태

### 성공 응답
```json
{
    "message": "TODO가 성공적으로 추가되었습니다."
}
```

### 조회 응답
```json
{
    "todo": {
        "id": 1,
        "content": "할 일 내용"
    }
}
```

### 오류 응답
```json
{
    "detail": "해당 ID의 할 일을 찾을 수 없습니다."
}
```

## 데이터 저장 방식

CSV 파일(`todos.csv`) 형식:
```
1,첫 번째 할 일
2,두 번째 할 일
3,세 번째 할 일
```

## 기술 스택

- **프레임워크**: FastAPI
- **서버**: uvicorn
- **데이터**: CSV 파일
- **모델**: pydantic BaseModel