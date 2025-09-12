import csv
import os
from typing import Dict
from fastapi import FastAPI, APIRouter, HTTPException
import uvicorn
from model import TodoItem


# FastAPI 애플리케이션 인스턴스 생성
app = FastAPI()
# API 라우터 인스턴스 생성
router = APIRouter()

# 할 일 목록을 저장할 전역 리스트
todo_list = []
# 다음 할 일 ID를 위한 카운터
next_id = 1
# CSV 파일 경로 상수
CSV_FILE = 'todos.csv'


# CSV 파일에서 할 일 목록을 불러오기
def load_todos_from_csv():
    global todo_list, next_id
    todo_list = []
    # CSV 파일이 존재하는지 확인
    if os.path.exists(CSV_FILE):
        # UTF-8 인코딩으로 CSV 파일 읽기
        with open(CSV_FILE, 'r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            # 각 행을 딕셔너리 형태로 변환하여 리스트에 저장
            for i, row in enumerate(reader):
                if row and len(row) >= 2:
                    todo_id = int(row[0]) if row[0].isdigit() else i + 1
                    content = row[1] if len(row) > 1 else row[0]
                    todo_list.append({
                        'id': todo_id,
                        'content': content
                    })
    # 다음 ID 설정
    next_id = max([todo['id'] for todo in todo_list], default=0) + 1

# 할 일 목록을 CSV 파일에 저장
def save_todos_to_csv():
    # UTF-8 인코딩으로 CSV 파일 쓰기
    with open(CSV_FILE, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # 각 할 일의 id, content를 CSV 행으로 저장
        for todo in todo_list:
            writer.writerow([todo['id'], todo['content']])
 
# 할 일을 추가 API 
@router.post('/todo/add')
async def add_todo(todo_data: Dict) -> Dict:
    global next_id
    # 빈 데이터나 빈 내용 검증
    if not todo_data or 'content' not in todo_data or not todo_data['content'].strip():
        raise HTTPException(status_code=400, detail='빈 값은 입력할 수 없습니다.')
    
    # 새로운 할 일 생성
    new_todo = {
        'id': next_id,
        'content': todo_data['content']
    }
    # 리스트에 추가
    todo_list.append(new_todo)
    # 다음 ID 증가
    next_id += 1
    # CSV 파일에 저장
    save_todos_to_csv()
    
    return {'message': 'TODO가 성공적으로 추가되었습니다.'}

# 모든 할 일 목록 조회 API
@router.get('/todo')
async def retrieve_todo() -> Dict:
    # CSV 파일에서 최신 데이터 로드
    load_todos_from_csv()
    # 할 일 목록 반환
    return {'todos': todo_list}


# 특정 ID의 할 일 조회 API
@router.get('/todo/{todo_id}')
async def get_single_todo(todo_id: int) -> Dict:
    # CSV 파일에서 최신 데이터 로드
    load_todos_from_csv()
    
    # 해당 ID의 할 일 찾기
    for todo in todo_list:
        if todo['id'] == todo_id:
            return {'todo': todo}
    
    raise HTTPException(status_code=404, detail='해당 ID의 할 일을 찾을 수 없습니다.')


# 할 일 수정 API 
@router.put('/todo/update/{todo_id}')
async def update_todo(todo_id: int, todo_item: TodoItem) -> Dict:
    # CSV 파일에서 최신 데이터 로드
    load_todos_from_csv()
    
    # 해당 ID의 할 일 찾기
    for i, todo in enumerate(todo_list):
        if todo['id'] == todo_id:
            # 할 일 정보 업데이트
            todo_list[i]['content'] = todo_item.content
            # CSV 파일에 저장
            save_todos_to_csv()
            return {'message': '할 일이 성공적으로 수정되었습니다.'}
    
    # 할 일을 찾지 못한 경우
    raise HTTPException(status_code=404, detail='해당 ID의 할 일을 찾을 수 없습니다.')


# 할 일 삭제 API
@router.delete('/todo/delete/{todo_id}')
async def delete_single_todo(todo_id: int) -> Dict:
    # CSV 파일에서 최신 데이터 로드
    load_todos_from_csv()
    
    # 해당 ID의 할 일 찾기
    for i, todo in enumerate(todo_list):
        if todo['id'] == todo_id:
            # 삭제될 할 일 정보 저장
            deleted_todo = todo_list.pop(i)
            # CSV 파일에 저장
            save_todos_to_csv()
            return {'message': '할 일이 성공적으로 삭제되었습니다.'}
    
    raise HTTPException(status_code=404, detail='해당 ID의 할 일을 찾을 수 없습니다.')

# 라우터 등록
app.include_router(router)

if __name__ == '__main__':
    load_todos_from_csv()
    uvicorn.run(app, host='0.0.0.0', port=8000)