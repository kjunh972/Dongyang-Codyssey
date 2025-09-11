import csv
import os
from typing import Dict
from fastapi import FastAPI, APIRouter, HTTPException
import uvicorn


# FastAPI 애플리케이션 인스턴스 생성
app = FastAPI()
# API 라우터 인스턴스 생성
router = APIRouter()

# 할 일 목록을 저장할 전역 리스트
todo_list = []
# CSV 파일 경로 상수
CSV_FILE = 'todos.csv'


#CSV 파일에서 할 일 목록을 불러오는 함수
def load_todos_from_csv():
    global todo_list
    # CSV 파일이 존재하는지 확인
    if os.path.exists(CSV_FILE):
        # UTF-8 인코딩으로 CSV 파일 읽기
        with open(CSV_FILE, 'r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            # 각 행을 딕셔너리 형태로 변환하여 리스트에 저장
            todo_list = [{'content': row[0]} for row in reader if row]

# 할 일 목록을 CSV 파일에 저장하는 함수"""
def save_todos_to_csv():
    # UTF-8 인코딩으로 CSV 파일 쓰기
    with open(CSV_FILE, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # 각 할 일의 내용을 CSV 행으로 저장
        for todo in todo_list:
            writer.writerow([todo['content']])
 
# 할 일 추가 api
@router.post('/todo/add')
async def add_todo(todo_data: Dict) -> Dict:
    # 빈 데이터나 빈 내용 검증
    if not todo_data or 'content' not in todo_data or not todo_data['content'].strip():
        raise HTTPException(status_code=400, detail='빈 값은 입력할 수 없습니다.')
    
    # 새로운 할 일 생성
    new_todo = {'content': todo_data['content']}
    # 전역 리스트에 추가
    todo_list.append(new_todo)
    # CSV 파일에 저장
    save_todos_to_csv()
    
    # 성공 응답 반환
    return {'message': 'TODO가 성공적으로 추가되었습니다.', 'todo': new_todo}

# 할 일 목록 api
@router.get('/todo')
async def retrieve_todo() -> Dict:
    # CSV 파일에서 최신 데이터 로드
    load_todos_from_csv()
    # 할 일 목록 반환
    return {'todos': todo_list}

# 라우터 등록
app.include_router(router)

if __name__ == '__main__':
    load_todos_from_csv()
    uvicorn.run(app, host='0.0.0.0', port=8000)