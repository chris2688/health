import sys
import io
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import re

# UTF-8 인코딩 설정
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

WP_URL = "https://health9988234.mycafe24.com"

def extract_header():
    """WordPress 헤더 HTML 추출"""
    print("=" * 60)
    print("🔍 WordPress 헤더 추출")
    print("=" * 60)
    
    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        print(f"\n🌐 메인 사이트 접속 중...")
        driver.get(WP_URL)
        time.sleep(5)
        
        # 헤더 추출
        print("\n🎨 헤더 요소 찾는 중...")
        
        header_selectors = [
            "header.site-header",
            "header#masthead",
            "header",
            ".site-header",
            "#masthead"
        ]
        
        header_html = None
        for selector in header_selectors:
            try:
                header = driver.find_element(By.CSS_SELECTOR, selector)
                header_html = header.get_attribute('outerHTML')
                print(f"  ✅ 헤더 발견: {selector}")
                break
            except:
                continue
        
        if header_html:
            # CSS 링크 추출
            print("\n🎨 CSS 링크 추출 중...")
            page_source = driver.page_source
            
            # CSS 링크 찾기
            css_links = re.findall(r'<link[^>]*rel=["\']stylesheet["\'][^>]*>', page_source)
            
            print(f"  ✓ CSS 링크 {len(css_links)}개 발견")
            
            # 파일 저장
            with open("wordpress_header.html", "w", encoding="utf-8") as f:
                f.write("<!-- WordPress CSS -->\n")
                for css in css_links[:10]:  # 처음 10개만
                    f.write(css + "\n")
                f.write("\n<!-- WordPress 헤더 -->\n")
                f.write(header_html)
            
            print("\n✅ wordpress_header.html 파일로 저장됨!")
            print(f"   헤더 크기: {len(header_html)} bytes")
            
            # 미리보기
            print("\n📋 헤더 미리보기 (처음 200자):")
            print("-" * 60)
            print(header_html[:200] + "...")
            print("-" * 60)
            
            return header_html
        else:
            print("❌ 헤더를 찾을 수 없습니다")
            return None
        
    except Exception as e:
        print(f"❌ 오류: {e}")
        return None
    finally:
        driver.quit()

if __name__ == "__main__":
    header = extract_header()
    
    if header:
        print("\n" + "=" * 60)
        print("✅ 추출 완료!")
        print("=" * 60)
        print("\n💡 다음 단계:")
        print("   1. wordpress_header.html 파일 확인")
        print("   2. intro.html 상단에 이 헤더 추가")
        print("=" * 60)
    
    print("\n⏳ 5초 후 종료...")
    time.sleep(5)

