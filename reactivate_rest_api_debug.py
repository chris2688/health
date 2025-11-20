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

def reactivate_rest_api_debug():
    """WordPress REST API 재활성화 (디버깅 모드)"""
    print("=" * 60)
    print("🔄 WordPress REST API 재활성화 시작 (디버깅 모드)")
    print("=" * 60)
    
    # Chrome 옵션 설정 (headless 비활성화로 브라우저 표시)
    chrome_options = Options()
    # chrome_options.add_argument('--headless')  # 디버깅을 위해 비활성화
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
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
        time.sleep(3)
        
        # 페이지 소스 일부 출력
        print("\n[DEBUG] 페이지 제목:", driver.title)
        
        # 3. "게시물 이름" 라디오 버튼 찾기 (여러 방법 시도)
        print("\n3️⃣  '게시물 이름' 라디오 버튼 찾기 중...")
        
        postname_radio = None
        selectors = [
            ("CSS", "input[value='/%postname%/']"),
            ("CSS", "label:contains('게시물 이름')"),
            ("XPATH", "//label[contains(text(), '게시물 이름')]/preceding-sibling::input"),
            ("XPATH", "//label[contains(text(), 'Post name')]/preceding-sibling::input"),
            ("CSS", "input[name='selection'][value='/%postname%/']"),
        ]
        
        for selector_type, selector in selectors:
            try:
                print(f"   시도 중: {selector_type} - {selector}")
                if selector_type == "CSS":
                    postname_radio = driver.find_element(By.CSS_SELECTOR, selector)
                elif selector_type == "XPATH":
                    postname_radio = driver.find_element(By.XPATH, selector)
                
                if postname_radio:
                    print(f"   ✅ 라디오 버튼 발견: {selector}")
                    break
            except Exception as e:
                print(f"   ❌ 실패: {e}")
                continue
        
        if not postname_radio:
            # 모든 input 요소 출력
            print("\n[DEBUG] 페이지의 모든 input 요소:")
            inputs = driver.find_elements(By.TAG_NAME, "input")
            for i, inp in enumerate(inputs):
                print(f"   Input {i}: type={inp.get_attribute('type')}, value={inp.get_attribute('value')}, name={inp.get_attribute('name')}")
                if i > 10:  # 처음 10개만
                    break
            
            raise Exception("게시물 이름 라디오 버튼을 찾을 수 없습니다.")
        
        # 4. 라디오 버튼 클릭
        print("\n4️⃣  '게시물 이름' 선택 중...")
        driver.execute_script("arguments[0].click();", postname_radio)
        time.sleep(1)
        print("   ✅ '게시물 이름' 선택 완료")
        
        # 5. 저장 버튼 찾기
        print("\n5️⃣  저장 버튼 찾기 중...")
        save_button = None
        save_selectors = [
            ("ID", "submit"),
            ("NAME", "submit"),
            ("CSS", "input[type='submit']"),
            ("CSS", "button[type='submit']"),
            ("XPATH", "//input[@value='변경사항 저장']"),
            ("XPATH", "//input[@value='Save Changes']"),
        ]
        
        for selector_type, selector in save_selectors:
            try:
                print(f"   시도 중: {selector_type} - {selector}")
                if selector_type == "ID":
                    save_button = driver.find_element(By.ID, selector)
                elif selector_type == "NAME":
                    save_button = driver.find_element(By.NAME, selector)
                elif selector_type == "CSS":
                    save_button = driver.find_element(By.CSS_SELECTOR, selector)
                elif selector_type == "XPATH":
                    save_button = driver.find_element(By.XPATH, selector)
                
                if save_button:
                    print(f"   ✅ 저장 버튼 발견: {selector}")
                    break
            except Exception as e:
                print(f"   ❌ 실패: {e}")
                continue
        
        if not save_button:
            raise Exception("저장 버튼을 찾을 수 없습니다.")
        
        # 6. 저장
        print("\n6️⃣  변경사항 저장 중...")
        save_button.click()
        time.sleep(5)
        print("   ✅ 저장 완료")
        
        # 7. REST API 확인
        print("\n7️⃣  REST API 상태 확인 중...")
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
        
        # 브라우저 유지 (확인용)
        print("\n브라우저를 10초간 유지합니다...")
        time.sleep(10)
        
        return True
        
    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()
        
        if driver:
            print("\n브라우저를 10초간 유지합니다 (오류 확인용)...")
            time.sleep(10)
        
        return False
        
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    reactivate_rest_api_debug()

