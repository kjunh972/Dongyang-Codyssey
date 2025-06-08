import os
import csv
import speech_recognition as sr
from datetime import datetime


class SpeechToText:
    '''음성을 텍스트로 변환하고 CSV 파일로 저장하는 클래스입니다.'''
    
    def __init__(self):
        '''SpeechToText 클래스의 초기화 메서드입니다.'''
        self.records_path = './project2/No7/records'
        self.recognizer = sr.Recognizer()
    
    def get_audio_files(self):
        '''records 폴더에서 WAV 파일 목록을 가져옵니다.'''
        if not os.path.exists(self.records_path):
            print(f'Error: {self.records_path} 폴더가 존재하지 않습니다.')
            return []
            
        return [f for f in os.listdir(self.records_path) if f.endswith('.wav')]
    
    def convert_to_text(self, audio_file):
        '''음성 파일을 텍스트로 변환합니다.'''
        file_path = os.path.join(self.records_path, audio_file)
        
        try:
            with sr.AudioFile(file_path) as source:
                # 오디오 파일 로드
                audio = self.recognizer.record(source)
                # 음성을 텍스트로 변환 (한국어 설정)
                text = self.recognizer.recognize_google(audio, language='ko-KR')
                return text
        except sr.UnknownValueError:
            print(f'음성을 인식할 수 없습니다: {audio_file}')
            return ''
        except sr.RequestError as e:
            print(f'Google Speech Recognition 서비스 에러: {e}')
            return ''
    
    def save_to_csv(self, audio_file, text):
        '''변환된 텍스트를 CSV 파일로 저장합니다.'''
        # CSV 파일명 생성 (WAV 확장자를 CSV로 변경)
        csv_file = os.path.join(self.records_path, 
                               os.path.splitext(audio_file)[0] + '.csv')
        
        # 현재 시간을 기록
        timestamp = datetime.now().strftime('%H:%M:%S')
        
        # CSV 파일 작성
        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['시간', '인식된 텍스트'])
            writer.writerow([timestamp, text])
            
        print(f'CSV 파일이 저장되었습니다: {csv_file}')
    
    def process_all_files(self):
        '''모든 음성 파일을 처리합니다.'''
        audio_files = self.get_audio_files()
        
        if not audio_files:
            print('처리할 음성 파일이 없습니다.')
            return
            
        print(f'발견된 음성 파일: {len(audio_files)}개')
        
        for audio_file in audio_files:
            print(f'\n파일 처리 중: {audio_file}')
            text = self.convert_to_text(audio_file)
            
            if text:
                print(f'인식된 텍스트: {text}')
                self.save_to_csv(audio_file, text)
            else:
                print('텍스트 변환 실패')


if __name__ == '__main__':
    stt = SpeechToText()
    stt.process_all_files()
