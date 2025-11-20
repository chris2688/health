import sys
import io
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

# UTF-8 인코딩 설정
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# ---------------------------------------------------------
# ✅ 설정 변수
# ---------------------------------------------------------
WP_LOGIN_URL = "https://health9988234.mycafe24.com/wp-login.php"
WP_ADMIN_URL = "https://health9988234.mycafe24.com/wp-admin/"
WP_USER = "health9988234"
WP_PASSWORD = "ssurlf7904!"
WP_BASE_URL = "https://health9988234.mycafe24.com"


def setup_driver():
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    return driver


def wp_login(driver):
    print("🔐 WordPress 로그인 중...")
    driver.get(WP_LOGIN_URL)
    time.sleep(2)
    
    try:
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
            print("  ✓ 로그인 성공!\n")
            return True
        return False
    except Exception as e:
        print(f"  ❌ 로그인 실패: {e}")
        return False


def set_homepage_as_front(driver):
    """'홈 (메인 로비)' 페이지를 프론트 페이지로 설정"""
    print("🏠 '홈 (메인 로비)' 페이지를 프론트 페이지로 설정 중...\n")
    
    try:
        driver.get(f"{WP_ADMIN_URL}options-reading.php")
        time.sleep(2)
        
        # 정적 페이지 옵션 선택
        try:
            page_radio = driver.find_element(By.ID, "page_on_front")
            if page_radio:
                # 상위의 라디오 버튼 찾기
                try:
                    static_page_radio = driver.find_element(By.XPATH, "//input[@name='show_on_front'][@value='page']")
                    driver.execute_script("arguments[0].click();", static_page_radio)
                    time.sleep(1)
                    print("  ✓ 정적 페이지 옵션 선택")
                except:
                    print("  ℹ️ 정적 페이지가 이미 선택되어 있습니다")
        except Exception as e:
            print(f"  ⚠️ 라디오 버튼 찾기 실패: {e}")
        
        # 프론트 페이지로 "홈 (메인 로비)" 선택 (ID: 2055)
        try:
            front_page_select = driver.find_element(By.ID, "page_on_front")
            # 옵션 2055 선택
            option_2055 = driver.find_element(By.XPATH, "//select[@id='page_on_front']/option[@value='2055']")
            driver.execute_script("arguments[0].selected = true;", option_2055)
            time.sleep(1)
            print("  ✓ '홈 (메인 로비)' 페이지를 프론트 페이지로 선택")
        except Exception as e:
            print(f"  ⚠️ 프론트 페이지 선택 실패: {e}")
            # 텍스트로 찾기 시도
            try:
                front_page_select = driver.find_element(By.ID, "page_on_front")
                option = driver.find_element(By.XPATH, "//select[@id='page_on_front']/option[contains(text(), '홈')]")
                driver.execute_script("arguments[0].selected = true;", option)
                time.sleep(1)
                print("  ✓ '홈' 페이지를 프론트 페이지로 선택 (텍스트 매칭)")
            except:
                print("  ❌ '홈' 페이지를 찾을 수 없습니다")
        
        # 저장
        try:
            save_btn = driver.find_element(By.ID, "submit")
            driver.execute_script("arguments[0].click();", save_btn)
            time.sleep(2)
            print("  ✅ 설정 저장 완료!\n")
            return True
        except Exception as e:
            print(f"  ⚠️ 저장 실패: {e}\n")
            return False
            
    except Exception as e:
        print(f"  ❌ 프론트 페이지 설정 실패: {e}\n")
        return False


def main():
    print("\n" + "="*60)
    print("🎨 워드프레스 프론트 페이지 설정")
    print("="*60 + "\n")
    
    driver = setup_driver()
    
    try:
        if not wp_login(driver):
            print("❌ 로그인 실패")
            return
        
        if set_homepage_as_front(driver):
            print("="*60)
            print("✨ 완료!")
            print("="*60)
            print(f"\n🌐 사이트 확인: {WP_BASE_URL}")
            print("\n💡 메인 화면에 7개의 카테고리 카드가 표시됩니다!")
            print("   각 카드를 클릭하면 서브카테고리 페이지로 이동합니다.\n")
        else:
            print("\n💡 수동 설정 방법:")
            print("   1. WordPress 관리자 > 설정 > 읽기")
            print("   2. '홈페이지 표시' > '정적 페이지' 선택")
            print("   3. '홈페이지' 드롭다운에서 '홈 (메인 로비)' 선택")
            print("   4. '변경사항 저장' 클릭\n")
        
    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
    finally:
        time.sleep(3)
        driver.quit()


if __name__ == "__main__":
    main()

