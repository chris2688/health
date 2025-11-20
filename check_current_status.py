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

def login_and_show_categories(driver):
    """로그인하고 카테고리 목록 확인"""
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
    print("✅ 로그인 완료!\n")
    
    # 카테고리 페이지로 이동
    print("📂 카테고리 목록 확인 중...")
    driver.get(f"{WP_URL}/wp-admin/edit-tags.php?taxonomy=category")
    time.sleep(3)
    
    try:
        # 모든 카테고리 이름 출력
        categories = driver.find_elements(By.CSS_SELECTOR, ".row-title")
        print("\n=== 현재 카테고리 목록 ===")
        for i, cat in enumerate(categories[:20], 1):  # 최대 20개만
            print(f"  {i}. {cat.text}")
        print("=" * 40)
    except Exception as e:
        print(f"❌ 카테고리 목록 읽기 실패: {e}")
    
    # 메인 사이트 열기
    print("\n🌐 메인 사이트 확인 중...")
    driver.get(WP_URL)
    time.sleep(3)
    
    print("\n💡 브라우저가 열려있습니다. 현재 상태를 확인해주세요!")
    print("   - 메인 화면이 어떻게 보이나요?")
    print("   - 카테고리를 클릭하면 서브카테고리가 나타나나요?")
    print("   - 서브카테고리를 클릭하면 글이 2열로 나타나나요?")
    print("\n⏳ 확인 후 아무 키나 누르면 종료됩니다...")
    input()

def main():
    print("=" * 60)
    print("🔍 현재 워드프레스 상태 확인")
    print("=" * 60 + "\n")
    
    # 크롬 드라이버 설정
    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        login_and_show_categories(driver)
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
    finally:
        driver.quit()
        print("\n✅ 브라우저 종료")

if __name__ == "__main__":
    main()

