from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Question
import models

# 데이터베이스 테이블 생성
models.Base.metadata.create_all(bind=engine)

# FastAPI 애플리케이션 인스턴스 생성
app = FastAPI()

# 데이터베이스 세션 
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get('/')
def main():
    return {'message': '게시판 API 서버가 실행 중입니다.'}

# 테이블 생성 확인 API
@app.get('/check/tables')
def check_tables():
    # 테이블 조회
    import sqlite3
    conn = sqlite3.connect('myapi.db')
    cursor = conn.cursor()
    
    # 테이블 목록 조회
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    # question 테이블 스키마 조회
    cursor.execute("PRAGMA table_info(question);")
    question_schema = cursor.fetchall()
    
    conn.close()
    
    return {
        'message': 'SQLite 테이블 생성 확인',
        'tables': [table[0] for table in tables],
        'question_table_schema': [
            {
                'column_id': col[0],
                'name': col[1], 
                'type': col[2],
                'not_null': bool(col[3]),
                'primary_key': bool(col[5])
            }
            for col in question_schema
        ]
    }

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)