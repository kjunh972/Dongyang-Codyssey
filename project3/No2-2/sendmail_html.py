import smtplib
import os
import getpass
import csv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders


# HTML 메일 발송 및 대량 전송 클래스
class HtmlEmailSender:
    def __init__(self, smtp_server='smtp.gmail.com', smtp_port=587):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.server = None
        
    # SMTP 서버 연결 및 로그인
    def setup_connection(self, sender_email, sender_password):
        try:
            print(f'SMTP 서버 연결 시도: {self.smtp_server}:{self.smtp_port}')
            # Gmail SMTP 서버에 연결
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
            print(f'상세 오류: {e}')
            return False
        except smtplib.SMTPConnectError:
            print(f'SMTP 서버 연결 실패: {self.smtp_server}:{self.smtp_port}')
            return False
        except Exception as e:
            print(f'연결 설정 중 오류 발생: {e}')
            return False
    
    # HTML 이메일 메시지 생성
    def create_html_message(self, sender_email, recipient_emails, subject, html_body, attachment_path=None):
        try:
            # MIME 멀티파트 메시지 생성
            msg = MIMEMultipart()
            # 메일 헤더 정보 설정
            msg['From'] = sender_email
            msg['To'] = ', '.join(recipient_emails) if isinstance(recipient_emails, list) else recipient_emails
            msg['Subject'] = subject
            
            # HTML 버전 추가
            html_part = MIMEText(html_body, 'html')
            msg.attach(html_part)
            
            # 첨부파일이 있으면 추가
            if attachment_path and os.path.exists(attachment_path):
                self.add_attachment(msg, attachment_path)
                print(f'첨부파일 추가: {attachment_path}')
            
            return msg
            
        except Exception as e:
            print(f'HTML 메시지 생성 중 오류 발생: {e}')
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
    
    # CSV 파일에서 메일 대상 목록 읽기
    def read_mail_targets(self, csv_file_path):
        try:
            targets = []
            # CSV 파일 읽기
            with open(csv_file_path, 'r', encoding='utf-8') as file:
                csv_reader = csv.reader(file)
                # 헤더 건너뛰기
                next(csv_reader, None)
                
                for row in csv_reader:
                    if len(row) >= 2:  # 이름, 이메일이 모두 있는 경우
                        name = row[0].strip()
                        email = row[1].strip()
                        if name and email:  # 빈 값이 아닌 경우만 추가
                            targets.append({'name': name, 'email': email})
            
            print(f'CSV에서 {len(targets)}명의 대상자를 읽었습니다.')
            return targets
            
        except FileNotFoundError:
            print(f'CSV 파일을 찾을 수 없습니다: {csv_file_path}')
            return []
        except Exception as e:
            print(f'CSV 파일 읽기 중 오류 발생: {e}')
            return []
    
    # 방법 1: 여러 명을 TO에 열거하여 한 번에 전송
    def send_bulk_email_method1(self, sender_email, targets, subject, html_body, attachment_path=None):
        try:
            # 모든 수신자 이메일 주소 추출
            recipient_emails = [target['email'] for target in targets]
            
            # HTML 메시지 생성
            msg = self.create_html_message(sender_email, recipient_emails, subject, html_body, attachment_path)
            if msg is None:
                return False
            
            # MIME 객체를 문자열로 변환
            text = msg.as_string()
            # 모든 수신자에게 한 번에 전송
            self.server.sendmail(sender_email, recipient_emails, text)
            print(f'방법 1: {len(targets)}명에게 한 번에 메일 전송 완료!')
            return True
            
        except Exception as e:
            print(f'방법 1 메일 전송 중 오류 발생: {e}')
            return False
    
    # 방법 2: 한 명씩 개별 전송
    def send_bulk_email_method2(self, sender_email, targets, subject, html_body, attachment_path=None):
        try:
            success_count = 0
            fail_count = 0
            
            for target in targets:
                try:
                    # 개인화된 HTML 메시지 생성
                    personalized_html = html_body.replace('[이름]', target['name'])
                    
                    # 개별 메시지 생성
                    msg = self.create_html_message(sender_email, [target['email']], subject, personalized_html, attachment_path)
                    if msg is None:
                        fail_count += 1
                        continue
                    
                    # MIME 객체를 문자열로 변환
                    text = msg.as_string()
                    # 개별 전송
                    self.server.sendmail(sender_email, [target['email']], text)
                    success_count += 1
                    print(f'{target["name"]} ({target["email"]})에게 전송 완료')
                    
                except Exception as e:
                    print(f'{target["name"]} ({target["email"]}) 전송 실패: {e}')
                    fail_count += 1
            
            print(f'방법 2: 개별 전송 완료 - 성공: {success_count}명, 실패: {fail_count}명')
            return success_count > 0
            
        except Exception as e:
            print(f'방법 2 메일 전송 중 오류 발생: {e}')
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
    print('=== HTML 메일 대량 발송 프로그램 ===\n')
    
    sender_email = input('보내는 사람 이메일 주소: ').strip()
    sender_password = getpass.getpass('비밀번호 : ').strip().replace(' ', '')
    
    csv_file = './project3/No2-2/mail_target_list.csv'
    
    subject = input('메일 제목: ')
    
    print('\n=== HTML 메일 내용 작성 ===')
    print('개별 전송 시 [이름] 부분이 수신자 이름으로 대체됩니다.')
    print('여러 줄 입력 후 "END"를 입력하면 입력 완료')
    print('HTML 메일 내용을 입력하세요:')
    
    html_lines = []
    while True:
        line = input()
        if line.strip().upper() == 'END':
            break
        html_lines.append(line)
    html_body = '\n'.join(html_lines)
    
    plain_body = None
    attachment_path = None
    
    method_choice = input('\n전송 방법 선택 (1: 한번에 전송, 2: 개별 전송, 3: 둘다 테스트): ')
    
    return sender_email, sender_password, csv_file, subject, html_body, attachment_path, method_choice


def main():
    try:
        sender_email, sender_password, csv_file, subject, html_body, attachment_path, method_choice = get_user_input()
        
        email_sender = HtmlEmailSender()
        
        # SMTP 연결 설정
        if not email_sender.setup_connection(sender_email, sender_password):
            print('SMTP 서버 연결에 실패했습니다.')
            return
        
        # CSV에서 대상자 목록 읽기
        targets = email_sender.read_mail_targets(csv_file)
        if not targets:
            print('유효한 메일 대상자가 없습니다.')
            return
        
        # 전송 방법에 따라 실행
        if method_choice == '1':
            print('\n=== 방법 1: 한 번에 전송 ===')
            email_sender.send_bulk_email_method1(sender_email, targets, subject, html_body, attachment_path)
            
        elif method_choice == '2':
            print('\n=== 방법 2: 개별 전송 ===')
            email_sender.send_bulk_email_method2(sender_email, targets, subject, html_body, attachment_path)
            
        elif method_choice == '3':
            print('\n=== 두 방법 모두 테스트 ===')
            print('\n--- 방법 1 테스트 ---')
            email_sender.send_bulk_email_method1(sender_email, targets, subject, html_body, attachment_path)
            print('\n--- 방법 2 테스트 ---')
            email_sender.send_bulk_email_method2(sender_email, targets, subject, html_body, attachment_path)
            
        else:
            print('올바른 방법을 선택해주세요 (1, 2, 또는 3)')
            
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