from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time


class NaverCrawler:
    def __init__(self):
        self.driver = None
        self.before_login_content = []
        self.after_login_content = []

    def setup_driver(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        options.add_experimental_option('useAutomationExtension', False)
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)
        self.driver.execute_script('Object.defineProperty(navigator, "webdriver", {get: () => undefined})')
        
    def navigate_to_naver(self):
        print('네이버 메인페이지로 이동합니다.')
        self.driver.get('https://www.naver.com')
        time.sleep(3)
        
    def crawl_before_login(self):
        print('로그인 전 콘텐츠를 크롤링합니다...')
        try:
            # 주요 서비스 메뉴
            services = self.driver.find_elements(By.CSS_SELECTOR, '.shortcut_list .service_name')
            for service in services:
                text = service.text.strip()
                if text:
                    self.before_login_content.append(f'서비스: {text}')
            
            # 우상단 영역 버튼들
            top_buttons = [
                ('#topAsideButton', '확장 영역'),
                ('#topTalkArea .btn_talk', '톡'),
                ('#topNotiArea .btn_notify', '알림'),
                ('#topShoppingArea .link_shopping', '장바구니')
            ]
            
            for selector, name in top_buttons:
                try:
                    element = self.driver.find_element(By.CSS_SELECTOR, selector)
                    self.before_login_content.append(f'상단메뉴: {name}')
                except:
                    continue
                    
        except Exception as e:
            print(f'로그인 전 크롤링 중 오류: {e}')
    
            
    def navigate_to_login_page(self):
        print('로그인 페이지로 이동합니다.')
        self.driver.get('https://nid.naver.com/nidlogin.login?mode=form&url=https://www.naver.com/')
        time.sleep(3)
        
    def wait_for_manual_login(self):
        print('브라우저에서 직접 로그인해주세요.')
        input('로그인 완료 후 엔터 키를 누르세요...')
        return True
    
    
    
    def crawl_after_login(self):
        try:
            print('로그인 후 콘텐츠 크롤링을 시작합니다...')
            self.driver.get('https://www.naver.com')
            time.sleep(5)
            
            print('로그인된 상태에서 콘텐츠 검색 중...')
            
            # 주요 서비스 메뉴
            services = self.driver.find_elements(By.CSS_SELECTOR, '.shortcut_list .service_name')
            for service in services:
                text = service.text.strip()
                if text:
                    self.after_login_content.append(f'서비스: {text}')
            
            # 사용자 정보 영역
            try:
                user_name = self.driver.find_element(By.CSS_SELECTOR, '.MyView-module__nickname___fcxwI')
                if user_name:
                    self.after_login_content.append(f'사용자: {user_name.text.strip()}님')
            except:
                pass
            
            # MY 서비스 메뉴
            try:
                my_services = self.driver.find_elements(By.CSS_SELECTOR, '.MyView-module__menu_list___UzzwA .MyView-module__item_text___VTQQM')
                for service in my_services:
                    text = service.text.strip()
                    if text:
                        try:
                            parent = service.find_element(By.XPATH, '..')
                            count_elem = parent.find_element(By.CSS_SELECTOR, '.MyView-module__item_num___eHxDY')
                            count = count_elem.text.strip()
                            if count:
                                self.after_login_content.append(f'MY서비스: {text} ({count})')
                            else:
                                self.after_login_content.append(f'MY서비스: {text}')
                        except:
                            self.after_login_content.append(f'MY서비스: {text}')
            except:
                pass
            
            # 알림 개수
            try:
                alarm_count = self.driver.find_element(By.CSS_SELECTOR, '.alarm_count')
                if alarm_count:
                    count = alarm_count.text.strip()
                    self.after_login_content.append(f'상단메뉴: 알림 ({count}개)')
            except:
                pass
            
            # 우상단 영역 버튼들
            top_buttons = [
                ('#topAsideButton', '확장 영역'),
                ('#topTalkArea .btn_talk', '톡'),
                ('#topNotiArea .btn_notify', '알림'),
                ('#topShoppingArea .link_shopping', '장바구니')
            ]
            
            for selector, name in top_buttons:
                try:
                    element = self.driver.find_element(By.CSS_SELECTOR, selector)
                    if 'alarm_count' not in selector:  # 알림 개수는 위에서 따로 처리
                        self.after_login_content.append(f'상단메뉴: {name}')
                except:
                    continue
                        
        except Exception as e:
            print(f'로그인 후 크롤링 중 오류 발생: {e}')
    
    def print_comparison(self):
        print('=== 로그인 전 콘텐츠 ===')
        if self.before_login_content:
            # 카테고리별로 정렬해서 출력
            services = [c for c in self.before_login_content if c.startswith('서비스:')]
            menus = [c for c in self.before_login_content if c.startswith('상단메뉴:')]
            
            for i, content in enumerate(services + menus, 1):
                print(f'{i}. {content}')
        else:
            print('로그인 전 콘텐츠를 찾을 수 없습니다.')
        
        print('\n=== 로그인 후 콘텐츠 ===')
        if self.after_login_content:
            # 카테고리별로 정렬해서 출력
            services = [c for c in self.after_login_content if c.startswith('서비스:')]
            users = [c for c in self.after_login_content if c.startswith('사용자:')]
            my_services = [c for c in self.after_login_content if c.startswith('MY서비스:')]
            menus = [c for c in self.after_login_content if c.startswith('상단메뉴:')]
            
            for i, content in enumerate(services + users + my_services + menus, 1):
                print(f'{i}. {content}')
        else:
            print('로그인 후 콘텐츠를 찾을 수 없습니다.')
            
        print('\n=== 로그인 전/후 차이점 ===')
        login_only_content = []
        
        for content in self.after_login_content:
            if content not in self.before_login_content:
                login_only_content.append(content)
        
        if login_only_content:
            # 콘텐츠 정렬
            users = [c for c in login_only_content if c.startswith('사용자:')]
            my_services = [c for c in login_only_content if c.startswith('MY서비스:')]
            others = [c for c in login_only_content if not c.startswith('사용자:') and not c.startswith('MY서비스:')]
            
            for i, content in enumerate(users + my_services + others, 1):
                print(f'{i}. {content}')
        else:
            print('로그인 전후 차이를 찾을 수 없습니다.')
    
    def close_driver(self):
        if self.driver:
            self.driver.quit()


def main():
    crawler = NaverCrawler()
    
    try:
        print('네이버 크롤링을 시작합니다...')
        crawler.setup_driver()
        
        # 1단계: 로그인 전 크롤링
        print('로그인 전 콘텐츠 크롤링')
        crawler.navigate_to_naver()
        crawler.crawl_before_login()
        
        # 2단계: 로그인 페이지로 이동 및 수동 로그인
        crawler.navigate_to_login_page()
        crawler.wait_for_manual_login()
        
        # 3단계: 로그인 후 크롤링
        print('\n로그인 후 콘텐츠 크롤링')
        crawler.crawl_after_login()
        
        # 4단계: 결과 비교 출력
        crawler.print_comparison()
        
    except Exception as e:
        print(f'프로그램 실행 중 오류 발생: {e}')
    
    finally:
        crawler.close_driver()


if __name__ == '__main__':
    main()