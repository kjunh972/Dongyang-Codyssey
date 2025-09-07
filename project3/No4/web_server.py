import http.server
import socketserver
import datetime
import os

class CustomHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        client_ip = self.client_address[0]
        
        print(f'접속 시간: {current_time}')
        print(f'접속한 클라이언트의 IP address: {client_ip}')
        print('-' * 50)
        
        # HTTP 200 OK 응답 헤더 전송
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        
        # index.html 파일 읽기 및 전송
        try:
            with open('index.html', 'r', encoding='utf-8') as file:
                html_content = file.read()
            self.wfile.write(html_content.encode('utf-8'))
        except FileNotFoundError:
            error_message = '<h1>404 - index.html 파일을 찾을 수 없습니다.</h1>'
            self.wfile.write(error_message.encode('utf-8'))


def start_web_server():
    port = 8080
    
    # 현재 디렉토리에서 서버 실행
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    with socketserver.TCPServer(('', port), CustomHTTPRequestHandler) as httpd:
        print(f'웹서버가 포트 {port}에서 실행 중입니다...')
        print(f'브라우저에서 http://localhost:{port} 로 접속하세요.')
        print('서버를 종료하려면 Ctrl+C를 누르세요.')
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print('\n웹서버를 종료합니다...')


if __name__ == '__main__':
    start_web_server()