def print_hello():
    '''화성에 인사하는 함수'''
    print('Hello Mars')


def read_and_analyze_log():
    '''로그 파일을 읽고 분석하는 함수'''
    try:
        with open('./No1/mission_computer_main.log', 'r', encoding='utf-8') as file:
            print('=== 로그 파일 내용 ===')
            # 첫 줄(헤더) 건너뛰기
            header = file.readline()
            
            events = []
            for line in file:
                timestamp, event, message = line.strip().split(',')
                print(f'{timestamp} [{event}] {message}')
                events.append((timestamp, event, message))
            
            print('=== 로그 파일 끝 ===')
            
            # 분석 보고서 작성
            with open('./No1/log_analysis.md', 'w', encoding='utf-8') as report:
                report.write('# 화성 기지 사고 분석 보고서\n\n')
                
                # 임무 개요
                report.write('## 1. 임무 개요\n')
                mission_start = events[0]
                mission_end = events[-1]
                report.write(f'- 임무 시작: {mission_start[0]}\n')
                report.write(f'- 임무 종료: {mission_end[0]}\n\n')
                
                # 주요 사건 연대기
                report.write('## 2. 주요 사건 연대기\n')
                key_events = []
                key_words = [
                    'initialization',
                    'liftoff',
                    'touchdown',
                    'oxygen',
                    'explosion'
                ]
                
                for timestamp, event, message in events:
                    if any(word in message.lower() for word in key_words):
                        key_events.append(f'- {timestamp}: {message}')
                report.write('\n'.join(key_events) + '\n\n')
                
                # 사고 분석
                report.write('## 3. 사고 분석\n')
                report.write('### 3.1 사고 발생\n')
                accident_events = []
                for timestamp, event, message in events:
                    if 'oxygen' in message.lower() or 'explosion' in message.lower():
                        accident_events.append(f'- {timestamp}: {message}')
                report.write('\n'.join(accident_events) + '\n\n')
                
    except FileNotFoundError:
        print('Error: 로그 파일을 찾을 수 없습니다.')
    except Exception as e:
        print(f'Error: 파일 처리 중 오류가 발생했습니다 - {str(e)}')

def main():
    '''메인 함수'''
    print_hello()
    read_and_analyze_log()

if __name__ == '__main__':
    main()