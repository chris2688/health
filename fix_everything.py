import sys
import io
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select
import time

# UTF-8 인코딩 설정
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# WordPress 정보
WP_URL = "https://health9988234.mycafe24.com"
WP_USERNAME = "health9988234"
WP_PASSWORD = "ssurlf7904!"

def login_to_wordpress(driver):
    """WordPress 로그인"""
    print("🔐 WordPress 로그인 중...")
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

def check_current_status(driver):
    """현재 상태 확인"""
    print("\n🔍 현재 상태 확인 중...")
    
    # 페이지 목록 확인
    driver.get(f"{WP_URL}/wp-admin/edit.php?post_type=page")
    time.sleep(3)
    
    try:
        pages = driver.find_elements(By.CSS_SELECTOR, ".row-title")
        print("\n=== 현재 페이지 목록 ===")
        for i, page in enumerate(pages[:10], 1):
            print(f"  {i}. {page.text}")
        print("=" * 40)
    except:
        print("  페이지 목록을 가져올 수 없습니다")
    
    # 설정 확인
    driver.get(f"{WP_URL}/wp-admin/options-reading.php")
    time.sleep(2)
    
    try:
        # 현재 홈페이지 설정 확인
        homepage_select = Select(driver.find_element(By.ID, "page_on_front"))
        current_homepage = homepage_select.first_selected_option.text
        print(f"\n현재 홈페이지: {current_homepage}")
    except:
        print("\n현재 홈페이지: 최신 글")
    
    # 메인 사이트 확인
    print("\n🌐 메인 사이트 열기...")
    driver.get(WP_URL)
    time.sleep(3)
    
    print("\n💡 브라우저에서 현재 상태를 확인해주세요!")
    print("   무엇이 문제인가요?")
    print("   1. 메인 화면이 비어있나요?")
    print("   2. 카드가 나타나지 않나요?")
    print("   3. 레이아웃이 깨져있나요?")
    print("\n⏳ 30초 후 자동으로 수정을 시도합니다...")
    time.sleep(30)

def main():
    print("=" * 60)
    print("🔧 WordPress 상태 확인 및 수정")
    print("=" * 60)
    
    # 크롬 드라이버 설정
    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        # 로그인
        login_to_wordpress(driver)
        
        # 상태 확인
        check_current_status(driver)
        
        print("\n" + "=" * 60)
        print("💬 어떤 문제가 있는지 알려주세요!")
        print("=" * 60)
        
        # 브라우저 유지
        print("\n⏳ 확인 후 아무 키나 누르면 종료됩니다...")
        input()
        
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        print("\n⏳ 10초 후 종료됩니다...")
        time.sleep(10)
    finally:
        driver.quit()

if __name__ == "__main__":
    main()

