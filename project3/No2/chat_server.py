import socket
import threading


class ChatServer:
    def __init__(self, host='localhost', port=12345):
        self.host = host
        self.port = port
        self.clients = []
        self.nicknames = []
        
    def broadcast(self, message, sender_client=None):
        # 모든 클라이언트에게 메시지 전송
        for client in self.clients:
            if client != sender_client:
                try:
                    client.send(message)
                except:
                    self.remove_client(client)
    
    # 특정 사용자에게 귓속말 전송
    def send_private_message(self, sender_nickname, target_nickname, message):
        try:
            # 받는 사람 찾기
            target_index = self.nicknames.index(target_nickname)
            target_client = self.clients[target_index]
            
            # 보내는 사람 찾기
            sender_index = self.nicknames.index(sender_nickname)
            sender_client = self.clients[sender_index]
            
            # 받는 사람에게 귓속말 전송
            private_msg = f'[귓속말] {sender_nickname}> {message}'.encode('utf-8')
            target_client.send(private_msg)
            
            # 보낸 사람에게 확인 메시지
            confirm_msg = f'[귓속말 전송완료] {target_nickname}님에게: {message}'.encode('utf-8')
            sender_client.send(confirm_msg)
            
        except ValueError:
            # 받는 사람을 찾을 수 없을 때
            sender_index = self.nicknames.index(sender_nickname)
            sender_client = self.clients[sender_index]
            error_msg = f'사용자 "{target_nickname}"을 찾을 수 없습니다.'.encode('utf-8')
            sender_client.send(error_msg)
    
    # 클라이언트 연결 해제 및 퇴장 메시지 전송
    def remove_client(self, client):
        if client in self.clients:
            index = self.clients.index(client)
            self.clients.remove(client)
            nickname = self.nicknames[index]
            self.nicknames.remove(nickname)
            self.broadcast(f'{nickname}님이 퇴장하셨습니다.'.encode('utf-8'))
            client.close()
    
    # 각 클라이언트 메시지 처리 
    def handle_client(self, client):
        while True:
            try:
                # 클라이언트로부터 메시지 수신
                message = client.recv(1024).decode('utf-8').strip()
                
                if message == '/종료':
                    self.remove_client(client)
                    break
                elif message.startswith('/귓속말'):
                    # 귓속말 명령어 처리
                    parts = message.split(' ', 2) 
                    if len(parts) >= 3:
                        target_nickname = parts[1]
                        private_message = parts[2]
                        sender_index = self.clients.index(client)
                        sender_nickname = self.nicknames[sender_index]
                        print(f'{sender_nickname}이 {target_nickname}에게 귓속말: {private_message}')
                        self.send_private_message(sender_nickname, target_nickname, private_message)
                    else:
                        print(f'잘못된 귓속말 형식: {parts}')
                        client.send('사용법: /귓속말 <닉네임> <메시지>'.encode('utf-8'))
                else:
                    # 일반 메시지 전체 전송
                    self.broadcast(message.encode('utf-8'), client)
                    
            except:
                self.remove_client(client)
                break
    
    # 서버 시작 및 클라이언트 연결 대기
    def start_server(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # TCP 소켓 생성
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # 포트 재사용 설정
        server.bind((self.host, self.port))  # 주소와 포트에 바인딩
        server.listen()  # 연결 대기 상태
        
        print(f'서버가 {self.host}:{self.port}에서 실행 중입니다...')
        
        while True:
            # 새 클라이언트 연결 수락
            client, address = server.accept()
            print(f'클라이언트 {str(address)}가 연결되었습니다.')
            
            # 닉네임 입력 받기
            client.send('닉네임을 입력하세요: '.encode('utf-8'))
            nickname = client.recv(1024).decode('utf-8')
            
            # 닉네임 중복 체크
            if nickname in self.nicknames:
                client.send('이미 사용 중인 닉네임입니다. 다시 시도해주세요.'.encode('utf-8'))
                client.close()
                continue
            
            # 클라이언트 정보 저장
            self.nicknames.append(nickname)
            self.clients.append(client)
            
            print(f'{nickname}님이 채팅방에 입장했습니다.')
            # 입장 메시지 전체 전송
            self.broadcast(f'{nickname}님이 입장하셨습니다.'.encode('utf-8'))
            client.send('채팅방에 입장했습니다!'.encode('utf-8'))
            
            # 각 클라이언트마다 별도 쓰레드 생성
            thread = threading.Thread(target=self.handle_client, args=(client,))
            thread.start()


if __name__ == '__main__':
    chat_server = ChatServer()
    try:
        chat_server.start_server()
    except KeyboardInterrupt:
        print('\n서버를 종료합니다...')
    except Exception as e:
        print(f'서버 오류: {e}')