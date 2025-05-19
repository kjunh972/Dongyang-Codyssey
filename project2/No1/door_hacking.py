import zipfile
import itertools
import string
import time
from datetime import datetime
from multiprocessing import Process, Queue, cpu_count
from queue import Empty
import random


def try_password_range(start_idx, end_idx, zip_path, result_queue, process_id):
    """특정 범위의 비밀번호를 시도하는 프로세스"""
    try:
        zip_file = zipfile.ZipFile(zip_path)
    except:
        result_queue.put(('error', process_id))
        return

    chars = string.ascii_lowercase + string.digits
    total_range = end_idx - start_idx
    
    # 진행상황 업데이트를 위한 시간 체크
    last_update = time.time()
    attempts = 0
    
    # 6자리 조합 생성 및 시도
    for i in range(start_idx, end_idx):
        # 6자리 비밀번호 생성
        current = []
        n = i
        for _ in range(6):
            current.append(chars[n % len(chars)])
            n //= len(chars)
        password = ''.join(current)
        
        attempts += 1
        
        try:
            # 비밀번호 시도
            first_file = zip_file.namelist()[0]
            zip_file.read(first_file, pwd=password.encode())
            
            # 비밀번호를 찾은 경우
            result_queue.put(('success', password, process_id, attempts))
            return
            
        except:
            # 2초마다 진행상황 보고
            if attempts % 1000 == 0:  # 1000번 시도마다 진행상황 체크
                current_time = time.time()
                if current_time - last_update >= 2:
                    progress = (attempts / total_range) * 100
                    result_queue.put(('progress', progress, attempts, process_id))
                    last_update = current_time

    # 실패 보고
    result_queue.put(('done', process_id, attempts))


def unlock_zip():
    """
    ZIP 파일 비밀번호 크래킹 함수
    - 6자리 비밀번호 (소문자 + 숫자)
    - 멀티프로세스 기반의 병렬 처리
    """
    zip_path = './project2/No1/emergency_storage_key.zip'
    
    try:
        with zipfile.ZipFile(zip_path) as zf:
            pass
    except FileNotFoundError:
        print('ZIP 파일을 찾을 수 없습니다.')
        return
    except zipfile.BadZipFile:
        print('유효하지 않은 ZIP 파일입니다.')
        return

    # 시작 시간 기록
    start_time = time.time()
    
    print(f'암호 해제 시작: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    print('\n비밀번호 크래킹 시작...')
    print('패턴: 6자리 숫자/소문자 조합 (36^6 가지)\n')
    
    # 프로세스 수 설정 (최대 8개로 제한)
    num_processes = min(8, cpu_count())
    chars = string.ascii_lowercase + string.digits
    
    # 전체 검색 공간 계산 및 분할
    total_combinations = len(chars) ** 6  # 36^6 가지
    chunk_size = total_combinations // num_processes
    
    print(f'전체 조합 수: {total_combinations:,}개')
    print(f'사용할 프로세스 수: {num_processes}개')
    print(f'프로세스당 시도할 조합 수: {chunk_size:,}개\n')
    
    # 결과 큐 생성
    result_queue = Queue()
    
    # 프로세스 생성 및 시작
    processes = []
    for i in range(num_processes):
        start_idx = i * chunk_size
        end_idx = start_idx + chunk_size if i < num_processes - 1 else total_combinations
        
        p = Process(target=try_password_range, 
                   args=(start_idx, end_idx, zip_path, result_queue, i))
        processes.append(p)
        p.start()
        print(f'프로세스 {i+1} 시작: {start_idx:,} ~ {end_idx:,} 범위 시도 중...')

    # 결과 모니터링
    completed = 0
    found = False
    progress = [0] * num_processes
    total_attempts = [0] * num_processes
    last_print = time.time()

    while completed < num_processes and not found:
        try:
            result = result_queue.get(timeout=0.5)
            
            if result[0] == 'success':
                found = True
                password = result[1]
                attempts = result[3]
                total_time = time.time() - start_time
                
                print(f'\n\n성공! 비밀번호를 찾았습니다!')
                print(f'비밀번호: {password}')
                print(f'총 소요 시간: {total_time:.1f}초')
                print(f'시도한 비밀번호: {attempts:,}개')
                print(f'초당 시도 횟수: {int(attempts/total_time):,}개/초')
                
                # 비밀번호를 파일에 저장
                with open('./project2/No1/password.txt', 'w') as f:
                    f.write(password)
                print(f'비밀번호가 password.txt 파일에 저장되었습니다.')
                
                # 다른 프로세스들 종료
                for p in processes:
                    if p.is_alive():
                        p.terminate()
                
                return password
                
            elif result[0] == 'progress':
                progress[result[3]] = result[1]
                total_attempts[result[3]] = result[2]
                
            elif result[0] == 'done':
                completed += 1
                total_attempts[result[1]] = result[2]
                
            elif result[0] == 'error':
                completed += 1
                
        except Empty:
            # 2초마다 진행상황 출력
            current_time = time.time()
            if current_time - last_print >= 2:
                avg_progress = sum(progress) / num_processes
                total_tried = sum(total_attempts)
                elapsed = current_time - start_time
                attempts_per_sec = int(total_tried / elapsed) if elapsed > 0 else 0
                
                print(f'\r진행률: {avg_progress:.1f}% | '
                      f'시도: {total_tried:,}개 | '
                      f'속도: {attempts_per_sec:,}개/초 | '
                      f'시간: {elapsed:.1f}초', end='', flush=True)
                last_print = current_time

    # 모든 프로세스 종료 확인
    for p in processes:
        if p.is_alive():
            p.terminate()
            p.join(timeout=1)

    if not found:
        print('\n비밀번호를 찾지 못했습니다.')
        print(f'시도한 총 비밀번호: {sum(total_attempts):,}개')
    
    return None


if __name__ == '__main__':
    unlock_zip()
