from pydantic import BaseModel

# 할 일 항목을 위한 Pydantic 모델 클래스
class TodoItem(BaseModel):
    content: str