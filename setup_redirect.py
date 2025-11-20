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

# 리디렉션 코드
REDIRECT_CODE = """<script>
window.location.href = "/intro.html";
</script>

<noscript>
<meta http-equiv="refresh" content="0;url=/intro.html">
</noscript>

<p style="text-align: center; padding: 50px; font-size: 18px;">
페이지를 로드하는 중... <br>
자동으로 이동하지 않으면 <a href="/intro.html" style="color: #667eea; font-weight: bold;">여기를 클릭</a>하세요.
</p>"""

def main():
    print("=" * 60)
    print("🔄 메인 페이지 리디렉션 설정")
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
        
        # 페이지 목록
        print("\n📝 '홈 (메인 로비)' 페이지 열기...")
        driver.get(f"{WP_URL}/wp-admin/edit.php?post_type=page")
        time.sleep(3)
        
        # "홈 (메인 로비)" 페이지 찾기
        try:
            page_link = driver.find_element(By.XPATH, "//a[@class='row-title' and contains(text(), '홈') and contains(text(), '메인')]")
            page_link.click()
            time.sleep(5)
        except:
            print("❌ 페이지를 찾을 수 없습니다")
            return False
        
        # 코드 편집기로 전환
        print("✏️ 코드 편집기로 전환 중...")
        try:
            # 옵션 메뉴
            options_button = driver.find_element(By.CSS_SELECTOR, "button[aria-label='옵션'], button[aria-label='Options']")
            driver.execute_script("arguments[0].click();", options_button)
            time.sleep(1)
            
            # 코드 편집기
            code_editor_button = driver.find_element(By.XPATH, "//button[contains(., '코드 편집기') or contains(., 'Code editor')]")
            driver.execute_script("arguments[0].click();", code_editor_button)
            time.sleep(2)
        except:
            print("⚠️ 코드 편집기 전환 건너뛰기")
        
        # 리디렉션 코드 입력
        print("📝 리디렉션 코드 입력 중...")
        try:
            code_textarea = driver.find_element(By.CSS_SELECTOR, "textarea.editor-post-text-editor")
            driver.execute_script("arguments[0].value = arguments[1];", code_textarea, REDIRECT_CODE)
            driver.execute_script("arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", code_textarea)
            time.sleep(2)
        except:
            print("❌ 코드 입력 실패")
            print("\n💡 수동으로 다음 코드를 붙여넣어주세요:")
            print("-" * 60)
            print(REDIRECT_CODE)
            print("-" * 60)
            return False
        
        # 업데이트
        print("💾 저장 중...")
        try:
            update_btn = driver.find_element(By.CSS_SELECTOR, ".editor-post-publish-button__button")
            driver.execute_script("arguments[0].click();", update_btn)
            time.sleep(3)
            print("✅ 저장 완료!")
        except:
            print("⚠️ 저장 버튼 클릭 실패 - 수동으로 저장해주세요")
        
        print("\n" + "=" * 60)
        print("✅ 설정 완료!")
        print("=" * 60)
        print("\n🌐 테스트:")
        print(f"   {WP_URL} 접속하면 자동으로 intro.html로 이동합니다!")
        print("=" * 60)
        
        print("\n⏳ 10초 후 브라우저가 닫힙니다...")
        time.sleep(10)
        
    except Exception as e:
        print(f"❌ 오류: {e}")
        time.sleep(10)
    finally:
        driver.quit()

if __name__ == "__main__":
    main()

