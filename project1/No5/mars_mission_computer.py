import time
import platform
import os

# No4의 mars_mission_computer.py 파일에서 DummySensor 가져오기
no4_file_path = './project1/No4/mars_mission_computer.py'

# 파일의 내용을 글로벌 네임스페이스에 로드
no4_globals = {}
with open(no4_file_path, 'r') as file:
    exec(file.read(), no4_globals)

# DummySensor 클래스를 글로벌 네임스페이스로 가져오기
DummySensor = no4_globals['DummySensor']


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
    
    def get_mission_computer_info(self):
        '''
        미션 컴퓨터의 시스템 정보를 가져오는 메소드
        Returns:
            dict: 시스템 정보
        '''
        try:
            system_info = {
                'operating_system': platform.system(),
                'os_version': platform.version(),
                'cpu_type': platform.processor() or platform.machine(),
                'cpu_cores': self._get_cpu_cores(),  # 실제 사용 가능한 CPU 코어 수
                'memory_size': self._get_memory_size()
            }
            
            # JSON 형태로 출력
            print('\n=== 미션 컴퓨터 시스템 정보 ===')
            print("{")
            for i, (key, value) in enumerate(system_info.items()):
                if i < len(system_info) - 1:
                    print(f'  "{key}": "{value}",')
                else:
                    print(f'  "{key}": "{value}"')
            print("}")
            
            return system_info
        except Exception as e:
            print(f'Error: 시스템 정보를 가져오는 중 오류 발생 - {str(e)}')
            return None
    
    def _get_cpu_cores(self):
        '''
        CPU 코어 수를 가져오는 내부 메소드
        Returns:
            int: CPU 코어 수
        '''
        try:
            if platform.system() == 'Darwin':  # macOS
                cmd = 'sysctl -n hw.ncpu'
                return int(os.popen(cmd).read())
            elif platform.system() == 'Linux':
                return len(os.sched_getaffinity(0))
            else:
                return os.cpu_count() or 1
        except:
            return os.cpu_count() or 1

    def _get_memory_size(self):
        '''
        시스템 메모리 크기를 가져오는 내부 메소드
        Returns:
            str: 메모리 크기 (단위: GB)
        '''
        try:
            if platform.system() == 'Darwin':  # macOS
                cmd = 'sysctl -n hw.memsize'
                mem_bytes = int(os.popen(cmd).read().strip())
                return f'{round(mem_bytes / (1024**3), 2)} GB'
            elif platform.system() == 'Linux':
                with open('/proc/meminfo', 'r') as f:
                    mem_kb = int(f.readline().split()[1])
                    return f'{round(mem_kb / (1024**2), 2)} GB'
            else:
                return 'Unknown'
        except:
            return 'Unknown'
    
    def get_mission_computer_load(self):
        '''
        미션 컴퓨터의 실시간 부하를 가져오는 메소드
        Returns:
            dict: CPU와 메모리 사용량
        '''
        try:
            # CPU 사용량 계산 (이전 상태와 비교하여 계산)
            if not hasattr(self, '_last_cpu_times'):
                self._last_cpu_times = self._get_cpu_times()
                time.sleep(0.1)
            
            current_cpu_times = self._get_cpu_times()
            cpu_usage = self._calculate_cpu_percent(self._last_cpu_times, current_cpu_times)
            self._last_cpu_times = current_cpu_times
            
            # 메모리 사용량 계산
            memory_usage = self._get_memory_usage()
            
            load_info = {
                'cpu_usage': f'{cpu_usage:.1f}%',
                'memory_usage': f'{memory_usage:.1f}%'
            }
            
            # JSON 형태로 출력
            print('\n=== 미션 컴퓨터 부하 정보 ===')
            print("{")
            for i, (key, value) in enumerate(load_info.items()):
                if i < len(load_info) - 1:
                    print(f'  "{key}": "{value}",')
                else:
                    print(f'  "{key}": "{value}"')
            print("}")
            
            return load_info
        except Exception as e:
            print(f'Error: 시스템 부하 정보를 가져오는 중 오류 발생 - {str(e)}')
            return None
    
    def _get_cpu_times(self):
        '''
        CPU 사용 시간 정보를 가져오는 내부 메소드
        Returns:
            tuple: (idle_time, total_time)
        '''
        if platform.system() == 'Linux':
            with open('/proc/stat', 'r') as f:
                cpu_times = f.readline().split()[1:]
                idle_time = float(cpu_times[3])
                total_time = sum(float(x) for x in cpu_times)
                return idle_time, total_time
        elif platform.system() == 'Darwin':  # macOS
            cmd = 'top -l 1 -n 0 | grep "CPU usage"'
            output = os.popen(cmd).read()
            if output:
                try:
                    user = float(output.split()[2].rstrip('%'))
                    sys = float(output.split()[4].rstrip('%'))
                    idle = float(output.split()[6].rstrip('%'))
                    return idle, user + sys + idle
                except:
                    pass
        return 0, 100  # 기본값
    
    def _calculate_cpu_percent(self, last_times, current_times):
        '''
        CPU 사용량을 계산하는 내부 메소드
        Args:
            last_times (tuple): 이전 CPU 시간 정보
            current_times (tuple): 현재 CPU 시간 정보
        Returns:
            float: CPU 사용량 (%)
        '''
        last_idle, last_total = last_times
        current_idle, current_total = current_times
        
        idle_delta = current_idle - last_idle
        total_delta = current_total - last_total
        
        if total_delta == 0:
            return 0.0
        
        return 100.0 * (1.0 - idle_delta / total_delta)
    
    def _get_memory_usage(self):
        '''
        메모리 사용량을 계산하는 내부 메소드
        Returns:
            float: 메모리 사용량 (%)
        '''
        if platform.system() == 'Linux':
            with open('/proc/meminfo', 'r') as f:
                lines = f.readlines()
                total = int(lines[0].split()[1])
                available = int(lines[2].split()[1])
                return 100 * (1 - available / total)
        elif platform.system() == 'Darwin':  # macOS
            cmd = 'vm_stat | grep "Pages free:"'
            free = int(os.popen(cmd).read().split()[2].strip('.'))
            cmd = 'vm_stat | grep "Pages active:"'
            active = int(os.popen(cmd).read().split()[2].strip('.'))
            cmd = 'vm_stat | grep "Pages inactive:"'
            inactive = int(os.popen(cmd).read().split()[2].strip('.'))
            total = free + active + inactive
            return 100 * (1 - free / total)
        return 0.0  # 기본값


def main():
    '''
    메인 함수
    '''
    # 미션 컴퓨터 인스턴스 생성
    runComputer = MissionComputer()
    
    # 시스템 정보 출력
    runComputer.get_mission_computer_info()
    
    # 시스템 부하 정보 출력
    runComputer.get_mission_computer_load()
    
    # 센서 데이터 모니터링 시작
    runComputer.get_sensor_data()


if __name__ == '__main__':
    main()
