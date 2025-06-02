import pyaudio
import wave
import datetime
import os


class AudioRecorder:
    '''음성을 녹음하고 파일로 저장하는 클래스입니다.'''
    
    def __init__(self):
        self.chunk = 1024
        self.format = pyaudio.paInt16
        self.channels = 1
        self.rate = 44100
        self.records_path = './project2/No7/records'
        self.input_gain = 5.0 
    

    def create_records_folder(self):
        '''records 폴더가 없으면 생성합니다.'''
        if not os.path.exists(self.records_path):
            os.makedirs(self.records_path)
    

    def get_filename(self):
        '''현재 날짜와 시간을 기반으로 파일명을 생성합니다.'''
        now = datetime.datetime.now()
        return now.strftime('%Y%m%d-%H%M%S') + '.wav'
    

    def amplify_audio(self, audio_data):
        '''오디오 데이터의 볼륨을 증폭시킵니다.'''
        # 바이트 데이터를 정수로 변환
        audio_int = int.from_bytes(audio_data, byteorder='little', signed=True)
        # 볼륨 증폭
        amplified = int(audio_int * self.input_gain)
        # 16비트 범위 (-32768 ~ 32767) 내로 제한
        amplified = max(min(amplified, 32767), -32768)
        # 다시 바이트로 변환
        return amplified.to_bytes(2, byteorder='little', signed=True)


    def record(self, duration=5):
        '''
        음성을 녹음하고 파일로 저장합니다.
        
        Args:
            duration (int): 녹음 시간 (초)
        '''
        p = pyaudio.PyAudio()

        # 스트림 열기
        stream = p.open(format=self.format,
                       channels=self.channels,
                       rate=self.rate,
                       input=True,
                       frames_per_buffer=self.chunk)

        print('녹음을 시작합니다...')
        
        frames = []
        
        # 녹음
        for i in range(0, int(self.rate / self.chunk * duration)):
            data = stream.read(self.chunk)
            # 각 청크의 볼륨을 증폭
            amplified_data = b''.join(self.amplify_audio(data[i:i+2]) for i in range(0, len(data), 2))
            frames.append(amplified_data)

        print('녹음이 완료되었습니다.')

        # 스트림 정리
        stream.stop_stream()
        stream.close()
        p.terminate()

        self.create_records_folder()
        filename = self.get_filename()
        filepath = os.path.join(self.records_path, filename)

        wf = wave.open(filepath, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(p.get_sample_size(self.format))
        wf.setframerate(self.rate)
        wf.writeframes(b''.join(frames))
        wf.close()

        print(f'녹음 파일이 저장되었습니다: {filepath}')


if __name__ == '__main__':
    recorder = AudioRecorder()
    recorder.record()
