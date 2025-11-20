from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# WordPress 관리자 정보
WP_URL = "https://health9988234.mycafe24.com/wp-admin"
WP_USERNAME = "health9988234"
WP_PASSWORD = "ssurlf7904!"

def reactivate_rest_api():
    """WordPress REST API 재활성화"""
    print("=" * 60)
    print("🔄 WordPress REST API 재활성화 시작")
    print("=" * 60)
    
    # Chrome 옵션 설정
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')
    
    driver = None
    try:
        driver = webdriver.Chrome(options=chrome_options)
        wait = WebDriverWait(driver, 20)
        
        # 1. 로그인
        print("\n1️⃣  WordPress 로그인 중...")
        driver.get(WP_URL)
        
        username_field = wait.until(EC.presence_of_element_located((By.ID, "user_login")))
        username_field.send_keys(WP_USERNAME)
        
        password_field = driver.find_element(By.ID, "user_pass")
        password_field.send_keys(WP_PASSWORD)
        
        login_button = driver.find_element(By.ID, "wp-submit")
        login_button.click()
        
        time.sleep(3)
        print("   ✅ 로그인 완료")
        
        # 2. 퍼머링크 설정 페이지로 이동
        print("\n2️⃣  퍼머링크 설정 페이지 접속 중...")
        driver.get("https://health9988234.mycafe24.com/wp-admin/options-permalink.php")
        time.sleep(2)
        
        # 3. "기본" 설정으로 변경
        print("\n3️⃣  퍼머링크를 '기본'으로 설정 중...")
        default_radio = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "input[value='']")
        ))
        driver.execute_script("arguments[0].click();", default_radio)
        time.sleep(1)
        
        # 저장 버튼 찾기 (여러 선택자 시도)
        try:
            save_button = driver.find_element(By.ID, "submit")
        except:
            try:
                save_button = driver.find_element(By.NAME, "submit")
            except:
                save_button = driver.find_element(By.CSS_SELECTOR, "input[type='submit']")
        
        save_button.click()
        time.sleep(3)
        print("   ✅ '기본' 설정 저장 완료")
        
        # 4. "게시물 이름"으로 변경
        print("\n4️⃣  퍼머링크를 '게시물 이름'으로 설정 중...")
        driver.get("https://health9988234.mycafe24.com/wp-admin/options-permalink.php")
        time.sleep(2)
        
        postname_radio = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "input[value='/%postname%/']")
        ))
        driver.execute_script("arguments[0].click();", postname_radio)
        time.sleep(1)
        
        # 저장 버튼 찾기 (여러 선택자 시도)
        try:
            save_button = driver.find_element(By.ID, "submit")
        except:
            try:
                save_button = driver.find_element(By.NAME, "submit")
            except:
                save_button = driver.find_element(By.CSS_SELECTOR, "input[type='submit']")
        
        save_button.click()
        time.sleep(3)
        print("   ✅ '게시물 이름' 설정 저장 완료")
        
        # 5. REST API 확인
        print("\n5️⃣  REST API 상태 확인 중...")
        import requests
        
        api_url = "https://health9988234.mycafe24.com/wp-json/wp/v2/posts"
        response = requests.get(api_url, timeout=10)
        
        if response.status_code == 200:
            posts = response.json()
            print(f"   ✅ REST API 정상 작동 (총 {len(posts)}개 포스트)")
        else:
            print(f"   ⚠️  REST API 상태: {response.status_code}")
        
        print("\n" + "=" * 60)
        print("✅ WordPress REST API 재활성화 완료!")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()
        return False
        
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    reactivate_rest_api()

