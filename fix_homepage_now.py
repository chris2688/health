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
    print("🔍 WordPress 홈페이지 상태 확인")
    print("=" * 60)
    
    # 크롬 드라이버 설정
    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        # 로그인
        print("\n🔐 WordPress 로그인 중...")
        driver.get(f"{WP_URL}/wp-login.php")
        time.sleep(2)
        
        username_field = driver.find_element(By.ID, "user_login")
        password_field = driver.find_element(By.ID, "user_pass")
        
        username_field.clear()
        username_field.send_keys(WP_USERNAME)
        password_field.clear()
        password_field.send_keys(WP_PASSWORD)
        
        login_button = driver.find_element(By.ID, "wp-submit")
        login_button.click()
        time.sleep(3)
        print("✅ 로그인 완료!")
        
        # 홈 페이지 열기
        print("\n🌐 메인 사이트 확인 중...")
        driver.get(WP_URL)
        time.sleep(5)
        
        print("\n" + "=" * 60)
        print("💬 현재 화면을 확인해주세요!")
        print("   1. 카드가 보이나요?")
        print("   2. 색상이 적용되었나요?")
        print("   3. 어떤 문제가 있나요?")
        print("=" * 60)
        
        # "홈 (메인 로비)" 페이지 편집 화면 열기
        print("\n📝 '홈 (메인 로비)' 페이지 편집 화면 열기...")
        driver.get(f"{WP_URL}/wp-admin/edit.php?post_type=page")
        time.sleep(3)
        
        try:
            page_link = driver.find_element(By.XPATH, "//a[@class='row-title' and contains(text(), '홈') and contains(text(), '메인')]")
            page_link.click()
            time.sleep(5)
            print("✅ 페이지 편집 모드 열림")
            print("\n💡 브라우저에서 직접 수정하실 수 있습니다!")
        except:
            print("❌ 페이지를 찾을 수 없습니다")
        
        print("\n⏳ 수정 후 Enter 키를 누르면 종료됩니다...")
        input()
        
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        time.sleep(10)
    finally:
        driver.quit()
        print("\n✅ 완료")

if __name__ == "__main__":
    main()

