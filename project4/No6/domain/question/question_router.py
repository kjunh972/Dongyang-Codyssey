# FastAPI 관련 모듈 import
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Question

# APIRouter 인스턴스 생성
router = APIRouter(
    prefix='/api/question'
)

# 데이터베이스 세션 의존성 함수
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 질문 조회 api
@router.get('/list')
def question_list(db: Session = Depends(get_db)):
    # 질문 조회
    question_list = db.query(Question).order_by(Question.create_date.desc()).all()
    return question_list