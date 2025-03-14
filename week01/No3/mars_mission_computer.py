import random


class DummySensor:
    '''
    화성 기지의 환경 센서를 시뮬레이션하는 더미 센서 클래스
    '''
    def __init__(self):
        '''
        생성자: 환경 값을 저장할 사전 객체 초기화
        '''
        self.env_values = {
            'mars_base_internal_temperature': 0,    # 기지 내부 온도 (18~30도)
            'mars_base_external_temperature': 0,    # 기지 외부 온도 (0~21도)
            'mars_base_internal_humidity': 0,       # 기지 내부 습도 (50~60%)
            'mars_base_external_illuminance': 0,    # 기지 외부 광량 (500~715 W/m2)
            'mars_base_internal_co2': 0,            # 기지 내부 이산화탄소 농도 (0.02~0.1%)
            'mars_base_internal_oxygen': 0          # 기지 내부 산소 농도 (4~7%)
        }
    
    def set_env(self):
        '''
        랜덤으로 환경 값을 생성하여 설정하는 메소드
        '''
        self.env_values['mars_base_internal_temperature'] = round(random.uniform(18, 30), 2)
        self.env_values['mars_base_external_temperature'] = round(random.uniform(0, 21), 2)
        self.env_values['mars_base_internal_humidity'] = round(random.uniform(50, 60), 2)
        self.env_values['mars_base_external_illuminance'] = round(random.uniform(500, 715), 2)
        self.env_values['mars_base_internal_co2'] = round(random.uniform(0.02, 0.1), 3)
        self.env_values['mars_base_internal_oxygen'] = round(random.uniform(4, 7), 2)
    
    def get_env(self):
        '''
        현재 환경 값을 반환하는 메소드
        Returns:
            dict: 환경 값 사전
        '''
        return self.env_values


def main():
    '''
    메인 함수
    '''
    # DummySensor 인스턴스 생성
    ds = DummySensor()
    
    # 환경 값 설정
    ds.set_env()
    
    # 환경 값 출력
    env_data = ds.get_env()
    print('=== 화성 기지 환경 정보 ===')
    for key, value in env_data.items():
        # 키 이름을 일반적인 형태로 변환
        name = key.replace('mars_base_', '').replace('_', ' ').title()
        print('{0}: {1}'.format(name, value))


if __name__ == '__main__':
    main()
