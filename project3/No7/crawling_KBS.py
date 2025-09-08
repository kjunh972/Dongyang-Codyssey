from bs4 import BeautifulSoup
import urllib.request
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time


def crawl_with_selenium(url):
    headlines_list = []
    driver = None
    
    try:
        # Chrome 옵션 설정 
        chrome_options = Options()
        chrome_options.add_argument('--headless') 
        
        # WebDriver 설정
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # 페이지 접속 및 렌더링
        driver.get(url)
        time.sleep(3)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        
        # BeautifulSoup으로 파싱
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        # .txt-wrapper .title 구조에서 헤드라인 추출
        txt_titles = soup.select('.txt-wrapper .title')
        
        for title in txt_titles:
            headline = title.get_text(strip=True)
            if headline and len(headline) > 5 and headline not in headlines_list:
                headlines_list.append(headline)
        
    except Exception as e:
        print(f'Selenium 크롤링 오류: {e}')
        return []
    
    finally:
        if driver:
            driver.quit()
    
    return headlines_list


def crawl_kbs_news():
    headlines_list = []
    
    # KBS 뉴스 메인 페이지
    kbs_url = 'http://news.kbs.co.kr'
    try:
        # BeautifulSoup 시도
        html = urllib.request.urlopen(kbs_url)
        soup = BeautifulSoup(html, 'html.parser')
        
        # 구조 기반 추출 시도
        selectors = ['.txt-wrapper .title', 'p.title', '.title', 'h3', 'h2', 'a[title]']
        
        for selector in selectors:
            elements = soup.select(selector)
            for element in elements:
                headline = element.get('title') if element.get('title') else element.get_text(strip=True)
                if headline and len(headline) > 5 and headline not in headlines_list:
                    headlines_list.append(headline)
                
    except Exception as e:
        return []
    
    # BeautifulSoup 실패 시 Selenium 사용 (KBS 메인페이지는 뉴스 목록을 JavaScript로 동적 생성하기 때문에 실패 가능성 있음)
    if len(headlines_list) == 0:
        headlines_list = crawl_with_selenium(kbs_url)
    
    # 헤드라인 출력
    if headlines_list:
        print('\nKBS 뉴스 헤드라인:')
        for i, headline in enumerate(headlines_list, 1):
            print(f'{i}. {headline}')
        print(f'\n총 {len(headlines_list)}개 헤드라인 추출')
    
    return headlines_list


def main():
    news_headlines = crawl_kbs_news()
    return news_headlines


if __name__ == '__main__':
    main()