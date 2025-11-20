import sys
import io
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# UTF-8 인코딩 설정
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# WordPress 정보
WP_URL = "https://health9988234.mycafe24.com"
WP_USERNAME = "health9988234"
WP_PASSWORD = "ssurlf7904!"

def main():
    print("=" * 60)
    print("🔍 CSS 문제 진단")
    print("=" * 60)
    
    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        # 로그인
        print("\n🔐 로그인 중...")
        driver.get(f"{WP_URL}/wp-login.php")
        time.sleep(2)
        
        driver.find_element(By.ID, "user_login").send_keys(WP_USERNAME)
        driver.find_element(By.ID, "user_pass").send_keys(WP_PASSWORD)
        driver.find_element(By.ID, "wp-submit").click()
        time.sleep(3)
        print("✅ 로그인 완료!")
        
        # 메인 페이지 열기
        print("\n🌐 메인 페이지 열기...")
        driver.get(WP_URL)
        time.sleep(5)
        
        # 페이지 소스 분석
        print("\n📊 페이지 구조 분석 중...")
        
        # health-card-container 확인
        try:
            container = driver.find_element(By.CLASS_NAME, "health-card-container")
            print("  ✓ .health-card-container 발견!")
        except:
            print("  ❌ .health-card-container 없음!")
        
        # health-card 확인
        try:
            cards = driver.find_elements(By.CLASS_NAME, "health-card")
            print(f"  ✓ .health-card {len(cards)}개 발견!")
        except:
            print("  ❌ .health-card 없음!")
        
        # CSS 스타일 확인
        try:
            card = driver.find_element(By.CLASS_NAME, "health-card")
            bg_color = driver.execute_script("return window.getComputedStyle(arguments[0]).background;", card)
            print(f"  📌 카드 배경: {bg_color[:100]}...")
            
            if "gradient" in bg_color or "linear" in bg_color:
                print("  ✅ 그라디언트 CSS 적용됨!")
            else:
                print("  ❌ 그라디언트 CSS 미적용!")
        except Exception as e:
            print(f"  ⚠️ 스타일 확인 실패: {e}")
        
        print("\n" + "=" * 60)
        print("💡 브라우저를 확인하세요!")
        print("   F12를 눌러서 개발자 도구를 열고")
        print("   Elements 탭에서 .health-card를 찾아보세요!")
        print("=" * 60)
        
        print("\n⏳ 브라우저를 1분간 유지합니다...")
        print("   확인 후 아무 키나 누르면 종료됩니다...")
        
        # 1분 대기
        for i in range(60, 0, -10):
            print(f"   {i}초 남음...")
            time.sleep(10)
        
    except Exception as e:
        print(f"❌ 오류: {e}")
        time.sleep(10)
    finally:
        try:
            driver.quit()
        except:
            pass
        print("\n✅ 완료")

if __name__ == "__main__":
    main()

