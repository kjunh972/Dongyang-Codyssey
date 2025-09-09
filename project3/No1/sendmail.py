import smtplib
import os
import getpass
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders


# Gmail SMTP 메일 발송 클래스
class EmailSender:
    def __init__(self, smtp_server='smtp.gmail.com', smtp_port=587):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.server = None
        
    # SMTP 서버 연결 및 로그인
    def setup_connection(self, sender_email, sender_password):
        try:
            # Gmail SMTP 서버에 연결
            print(f'SMTP 서버 연결 시도: {self.smtp_server}:{self.smtp_port}')
            self.server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            # TLS 암호화 활성화 (보안 연결)
            self.server.starttls()
            print('TLS 암호화 연결 완료')
            
            # 비밀번호 정리 (공백 및 특수문자 처리)
            clean_password = sender_password.strip().replace(' ', '').replace('\xa0', '')
            
            # Gmail 앱 비밀번호로 로그인
            self.server.login(sender_email, clean_password)
            print('SMTP 서버 로그인 성공')
            return True
            
        except smtplib.SMTPAuthenticationError as e:
            print('로그인 실패: 이메일 또는 비밀번호를 확인하세요.')
            print('Gmail의 경우 앱 비밀번호를 사용해야 합니다.')
            print('확인 사항:')
            print('1. Gmail 계정에 2단계 인증이 활성화되어 있는지 확인')
            print('2. 앱 비밀번호가 올바르게 생성되었는지 확인 (16자리)')
            print('3. 일반 Gmail 비밀번호가 아닌 앱 비밀번호를 사용해야 합니다')
            print(f'상세 오류: {e}')
            return False
        except smtplib.SMTPConnectError:
            print(f'SMTP 서버 연결 실패: {self.smtp_server}:{self.smtp_port}')
            return False
        except Exception as e:
            print(f'연결 설정 중 오류 발생: {e}')
            return False
    
    # 이메일 메시지 생성
    def create_message(self, sender_email, recipient_email, subject, body, attachment_path=None):
        try:
            # MIME 멀티파트 메시지 생성
            msg = MIMEMultipart()
            # 메일 헤더 정보 설정
            msg['From'] = sender_email
            msg['To'] = recipient_email
            msg['Subject'] = subject
            
            # 메일 본문 추가
            msg.attach(MIMEText(body, 'plain'))
            
            if attachment_path and os.path.exists(attachment_path):
                self.add_attachment(msg, attachment_path)
                print(f'첨부파일 추가: {attachment_path}')
            
            return msg
            
        except Exception as e:
            print(f'메시지 생성 중 오류 발생: {e}')
            return None
    
    # 첨부파일 추가
    def add_attachment(self, msg, attachment_path):
        try:
            # 첨부파일을 바이너리 모드로 열기
            with open(attachment_path, 'rb') as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
            
            # Base64로 인코딩 (이메일 전송용)
            encoders.encode_base64(part)
            filename = os.path.basename(attachment_path)
            # 첨부파일 헤더 설정
            part.add_header(
                'Content-Disposition',
                f'attachment; filename= {filename}',
            )
            msg.attach(part)
            
        except Exception as e:
            print(f'첨부파일 추가 중 오류 발생: {e}')
    
    # 이메일 전송
    def send_email(self, sender_email, recipient_email, subject, body, attachment_path=None):
        try:
            # 메일 메시지 생성
            msg = self.create_message(sender_email, recipient_email, subject, body, attachment_path)
            if msg is None:
                return False
            
            # MIME 객체를 문자열로 변환
            text = msg.as_string()
            # SMTP 서버를 통해 메일 전송
            self.server.sendmail(sender_email, recipient_email, text)
            print('메일 전송 완료!')
            return True
            
        except smtplib.SMTPRecipientsRefused:
            print('수신자 이메일 주소가 잘못되었습니다.')
            return False
        except smtplib.SMTPDataError as e:
            print(f'메일 데이터 전송 오류: {e}')
            return False
        except Exception as e:
            print(f'메일 전송 중 오류 발생: {e}')
            return False
    
    # SMTP 연결 종료
    def close_connection(self):
        try:
            if self.server:
                self.server.quit()
                print('SMTP 연결 종료')
        except Exception as e:
            print(f'연결 종료 중 오류 발생: {e}')


# 사용자 입력 받기
def get_user_input():
    print('=== Gmail SMTP 메일 발송 프로그램 ===')
    print('Gmail 계정의 앱 비밀번호가 필요합니다.')
    print('Google 계정 > 보안 > 앱 비밀번호에서 설정하세요.\n')
    
    sender_email = input('보내는 사람 Gmail 주소: ').strip()
    sender_password = getpass.getpass('앱 비밀번호 (공백 없이 16자리): ').strip().replace(' ', '')
    recipient_email = input('받는 사람 이메일 주소: ')
    subject = input('메일 제목: ')
    body = input('메일 내용: ')
    
    attachment_choice = input('첨부파일을 추가하시겠습니까? (y/n): ').lower()
    attachment_path = None
    if attachment_choice == 'y':
        attachment_path = input('첨부파일 경로: ')
        if not os.path.exists(attachment_path):
            print('첨부파일을 찾을 수 없습니다. 첨부파일 없이 전송됩니다.')
            attachment_path = None
    
    return sender_email, sender_password, recipient_email, subject, body, attachment_path


# 메인 실행 함수
def main():
    try:
        sender_email, sender_password, recipient_email, subject, body, attachment_path = get_user_input()
        
        email_sender = EmailSender()
        
        if email_sender.setup_connection(sender_email, sender_password):
            success = email_sender.send_email(
                sender_email, 
                recipient_email, 
                subject, 
                body, 
                attachment_path
            )
            
            if success:
                print('메일이 성공적으로 전송되었습니다.')
            else:
                print('메일 전송에 실패했습니다.')
        else:
            print('SMTP 서버 연결에 실패했습니다.')
            
    except KeyboardInterrupt:
        print('\n프로그램이 사용자에 의해 중단되었습니다.')
    except Exception as e:
        print(f'프로그램 실행 중 예상치 못한 오류: {e}')
    finally:
        try:
            email_sender.close_connection()
        except:
            pass


if __name__ == '__main__':
    main()