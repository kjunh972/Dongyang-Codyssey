import socket
import threading


class ChatClient:
    def __init__(self, host='localhost', port=12345):
        self.host = host
        self.port = port
        self.nickname = ''  
        self.client = None 
        self.running = False  
    
    # 서버로부터 메시지 수신 
    def receive_messages(self):
        while self.running:
            try:
                message = self.client.recv(1024).decode('utf-8')
                if message == '닉네임을 입력하세요: ':
                    self.client.send(self.nickname.encode('utf-8'))
                else:
                    print(message)
            except:
                print('서버와의 연결이 끊어졌습니다.')
                self.client.close()
                break
    

    # 사용자 입력을 서버로 전송
    def send_messages(self):
        while self.running:
            user_input = input('')
            
            if user_input == '/종료':
                # 종료 명령어 전송
                self.client.send('/종료'.encode('utf-8'))
                self.running = False
                break
            elif user_input.startswith('/귓속말'):
                # 귓속말 명령어 전송
                self.client.send(user_input.encode('utf-8'))
            else:
                # 일반 메시지 전송 (닉네임 포함)
                message = f'{self.nickname}> {user_input}'
                self.client.send(message.encode('utf-8'))
    

    # 클라이언트 시작
    def start_client(self):
        self.nickname = input('닉네임을 입력하세요: ')
        
        try:
            # 서버에 연결
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.connect((self.host, self.port))
            self.running = True
            
            # 메시지 수신용 쓰레드 시작
            receive_thread = threading.Thread(target=self.receive_messages)
            receive_thread.start()
            
            # 메시지 전송용 쓰레드 시작
            send_thread = threading.Thread(target=self.send_messages)
            send_thread.start()
            
            # 쓰레드 종료 대기
            send_thread.join()
            receive_thread.join()
            
        except Exception as e:
            print(f'서버에 연결할 수 없습니다: {e}')
        finally:
            if self.client:
                self.client.close()


if __name__ == '__main__':
    chat_client = ChatClient()
    try:
        chat_client.start_client()
    except KeyboardInterrupt:
        print('\n클라이언트를 종료합니다...')
    except Exception as e:
        print(f'클라이언트 오류: {e}')