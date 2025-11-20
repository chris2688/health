import sys
import io
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

WP_LOGIN_URL = "https://health9988234.mycafe24.com/wp-login.php"
WP_ADMIN_URL = "https://health9988234.mycafe24.com/wp-admin/"
WP_USER = "health9988234"
WP_PASSWORD = "ssurlf7904!"


def setup_driver():
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    return driver


def wp_login(driver):
    print("=" * 60)
    print("🔐 WordPress 로그인")
    print("=" * 60)
    
    try:
        driver.get(WP_LOGIN_URL)
        time.sleep(2)
        
        user_field = driver.find_element(By.ID, "user_login")
        pass_field = driver.find_element(By.ID, "user_pass")
        user_field.clear()
        user_field.send_keys(WP_USER)
        pass_field.clear()
        pass_field.send_keys(WP_PASSWORD)
        
        login_btn = driver.find_element(By.ID, "wp-submit")
        login_btn.click()
        time.sleep(3)
        
        if "wp-admin" in driver.current_url:
            print("✅ 로그인 성공!")
            return True
        else:
            print("❌ 로그인 실패")
            return False
    except Exception as e:
        print(f"❌ 로그인 중 오류: {e}")
        return False


def set_permalink_to_postname(driver):
    """Permalink를 '게시물 이름'으로 설정"""
    print("\n" + "=" * 60)
    print("⚙️ Permalink를 '게시물 이름'으로 설정")
    print("=" * 60)
    
    try:
        driver.get(f"{WP_ADMIN_URL}options-permalink.php")
        time.sleep(3)
        
        print("\n📝 '게시물 이름' 옵션 찾기 중...")
        
        # "게시물 이름" 라디오 버튼 찾기 (value="/%postname%/")
        try:
            postname_radio = driver.find_element(By.CSS_SELECTOR, "input[type='radio'][value='/%postname%/']")
            
            if not postname_radio.is_selected():
                print("  ✓ '게시물 이름' 선택 중...")
                driver.execute_script("arguments[0].click();", postname_radio)
                time.sleep(1)
            else:
                print("  ℹ️ '게시물 이름'이 이미 선택되어 있습니다")
        except Exception as e:
            print(f"  ⚠️ '게시물 이름' 라디오 버튼을 찾을 수 없습니다: {e}")
            print("  💡 수동으로 설정해주세요:")
            print("     WordPress 관리자 > 설정 > 고유주소 > '게시물 이름' 선택")
            return False
        
        # 저장 버튼 클릭
        try:
            save_button = driver.find_element(By.ID, "submit")
            print("\n💾 설정 저장 중...")
            driver.execute_script("arguments[0].click();", save_button)
            time.sleep(3)
            print("  ✅ 저장 완료!")
            return True
        except Exception as e:
            print(f"  ❌ 저장 버튼 클릭 실패: {e}")
            return False
            
    except Exception as e:
        print(f"❌ Permalink 설정 중 오류: {e}")
        return False


def main():
    print("\n" + "=" * 60)
    print("🚀 WordPress Permalink 설정")
    print("=" * 60)
    
    driver = setup_driver()
    
    try:
        if not wp_login(driver):
            print("\n❌ 로그인 실패. 작업을 중단합니다.")
            return
        
        set_permalink_to_postname(driver)
        
        print("\n" + "=" * 60)
        print("✅ 작업 완료!")
        print("=" * 60)
        print("\n💡 다음 단계:")
        print("   1. 잠시 기다린 후 REST API 테스트:")
        print("      https://health9988234.mycafe24.com/wp-json/wp/v2/posts?per_page=1")
        print("   2. 카테고리 페이지를 새로고침하여 확인하세요")
        print("=" * 60)
        
    finally:
        print("\n⏳ 5초 후 브라우저 종료...")
        time.sleep(5)
        driver.quit()


if __name__ == "__main__":
    main()

