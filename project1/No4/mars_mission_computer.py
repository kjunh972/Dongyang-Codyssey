import time

# No3의 mars_mission_computer.py 파일에서 DummySensor 가져오기
no3_file_path = './project1/No3/mars_mission_computer.py'

# 파일의 내용을 글로벌 네임스페이스에 로드
no3_globals = {}
with open(no3_file_path, 'r') as file:
    exec(file.read(), no3_globals)

# DummySensor 클래스를 글로벌 네임스페이스로 가져오기
DummySensor = no3_globals['DummySensor']


class MissionComputer:
    '''
    화성 기지 미션 컴퓨터 클래스
    '''
    def __init__(self):
        '''
        생성자: 환경 값을 저장할 사전 객체와 더미 센서 초기화
        '''
        self.env_values = {
            'mars_base_internal_temperature': 0,    # 기지 내부 온도
            'mars_base_external_temperature': 0,    # 기지 외부 온도
            'mars_base_internal_humidity': 0,       # 기지 내부 습도
            'mars_base_external_illuminance': 0,    # 기지 외부 광량
            'mars_base_internal_co2': 0,            # 기지 내부 이산화탄소 농도
            'mars_base_internal_oxygen': 0          # 기지 내부 산소 농도
        }
        # No3의 DummySensor 인스턴스화
        self.ds = DummySensor()
    
    def get_sensor_data(self):
        '''
        센서 데이터를 가져와서 출력하는 메소드
        5초마다 센서 값을 갱신하고 출력
        '''
        try:
            while True:
                # 센서 값 갱신
                self.ds.set_env()
                self.env_values = self.ds.get_env()
                
                # JSON 형태로 출력
                print('\n=== 화성 기지 환경 정보 ===')
                print("{")
                for i, (key, value) in enumerate(self.env_values.items()):
                    if i < len(self.env_values) - 1:
                        print(f'  "{key}": {value},')
                    else:
                        print(f'  "{key}": {value}')
                print("}")
                
                # 5초 대기
                time.sleep(5)
        except KeyboardInterrupt:
            print('\n미션 컴퓨터 종료')


def main():
    '''
    메인 함수
    '''
    # 미션 컴퓨터 인스턴스 생성
    RunComputer = MissionComputer()
    
    # 센서 데이터 모니터링 시작
    RunComputer.get_sensor_data()


if __name__ == '__main__':
    main()
