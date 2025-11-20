import sys
import io
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

# UTF-8 인코딩 설정
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# WordPress 정보
WP_LOGIN_URL = "https://health9988234.mycafe24.com/wp-login.php"
WP_ADMIN_URL = "https://health9988234.mycafe24.com/wp-admin/"
WP_USER = "health9988234"
WP_PASSWORD = "ssurlf7904!"
WP_BASE_URL = "https://health9988234.mycafe24.com"


def setup_driver():
    """WebDriver 설정"""
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    return driver


def wp_login(driver):
    """WordPress 로그인"""
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


def fix_permalink_settings(driver):
    """Permalink 설정 확인 및 수정"""
    print("\n" + "=" * 60)
    print("⚙️ Permalink 설정 확인")
    print("=" * 60)
    
    try:
        # Permalink 설정 페이지로 이동
        driver.get(f"{WP_ADMIN_URL}options-permalink.php")
        time.sleep(3)
        
        print("\n📝 현재 Permalink 설정 확인 중...")
        
        # "일반 설정" 라디오 버튼 찾기
        try:
            # 여러 방법으로 찾기 시도
            common_radio = None
            
            # 방법 1: ID로 찾기
            try:
                common_radio = driver.find_element(By.ID, "permalink_structure_0")
            except:
                pass
            
            # 방법 2: value로 찾기
            if not common_radio:
                try:
                    common_radio = driver.find_element(By.CSS_SELECTOR, "input[type='radio'][value='']")
                except:
                    pass
            
            # 방법 3: XPath로 찾기
            if not common_radio:
                try:
                    common_radio = driver.find_element(By.XPATH, "//input[@type='radio' and @value='']")
                except:
                    pass
            
            if common_radio:
                # 이미 선택되어 있는지 확인
                if not common_radio.is_selected():
                    print("  ✓ '일반 설정' 선택 중...")
                    driver.execute_script("arguments[0].click();", common_radio)
                    time.sleep(1)
                else:
                    print("  ℹ️ '일반 설정'이 이미 선택되어 있습니다")
            else:
                print("  ⚠️ '일반 설정' 라디오 버튼을 찾을 수 없습니다")
        except Exception as e:
            print(f"  ⚠️ 라디오 버튼 찾기 실패: {e}")
        
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


def check_rest_api(driver):
    """REST API 작동 확인"""
    print("\n" + "=" * 60)
    print("🔍 REST API 작동 확인")
    print("=" * 60)
    
    try:
        # 브라우저에서 REST API 엔드포인트 테스트
        test_url = f"{WP_BASE_URL}/wp-json/wp/v2/posts?per_page=1"
        print(f"\n📡 테스트 URL: {test_url}")
        
        driver.get(test_url)
        time.sleep(2)
        
        page_source = driver.page_source
        
        # JSON 응답인지 확인
        if "title" in page_source or "rendered" in page_source or page_source.strip().startswith("["):
            print("  ✅ REST API가 정상 작동합니다!")
            return True
        elif "404" in page_source or "Not Found" in page_source:
            print("  ❌ REST API가 404를 반환합니다")
            print("  💡 Permalink 설정을 다시 확인하세요")
            return False
        else:
            print("  ⚠️ REST API 응답을 확인할 수 없습니다")
            print(f"  응답 내용: {page_source[:200]}")
            return False
            
    except Exception as e:
        print(f"❌ REST API 확인 중 오류: {e}")
        return False


def add_rest_api_support_via_htaccess():
    """.htaccess 파일에 REST API 지원 추가"""
    print("\n" + "=" * 60)
    print("📝 .htaccess 파일에 REST API 지원 추가")
    print("=" * 60)
    
    htaccess_content = """# WordPress REST API 지원
<IfModule mod_rewrite.c>
RewriteEngine On
RewriteBase /
RewriteRule ^index\\.php$ - [L]
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteRule . /index.php [L]
</IfModule>

# REST API CORS 헤더 (필요한 경우)
<IfModule mod_headers.c>
    Header set Access-Control-Allow-Origin "*"
    Header set Access-Control-Allow-Methods "GET, POST, OPTIONS"
    Header set Access-Control-Allow-Headers "Content-Type"
</IfModule>
"""
    
    try:
        with open(".htaccess", "r", encoding="utf-8") as f:
            current_content = f.read()
        
        # 이미 REST API 관련 내용이 있는지 확인
        if "wp-json" in current_content or "REST API" in current_content:
            print("  ℹ️ .htaccess에 이미 REST API 관련 설정이 있습니다")
            return False
        
        # 기존 내용에 추가
        new_content = current_content + "\n\n" + htaccess_content
        
        with open(".htaccess", "w", encoding="utf-8") as f:
            f.write(new_content)
        
        print("  ✅ .htaccess 파일 업데이트 완료!")
        print("  💡 이 파일을 FTP로 업로드해야 합니다")
        return True
        
    except FileNotFoundError:
        # .htaccess 파일이 없으면 새로 생성
        with open(".htaccess", "w", encoding="utf-8") as f:
            f.write(htaccess_content)
        print("  ✅ .htaccess 파일 생성 완료!")
        print("  💡 이 파일을 FTP로 업로드해야 합니다")
        return True
    except Exception as e:
        print(f"  ❌ .htaccess 파일 처리 중 오류: {e}")
        return False


def main():
    """메인 실행"""
    print("\n" + "=" * 60)
    print("🚀 WordPress REST API 활성화")
    print("=" * 60)
    
    driver = setup_driver()
    
    try:
        # 1. 로그인
        if not wp_login(driver):
            print("\n❌ 로그인 실패. 작업을 중단합니다.")
            return
        
        # 2. Permalink 설정 확인 및 수정
        fix_permalink_settings(driver)
        
        # 3. REST API 작동 확인
        check_rest_api(driver)
        
        # 4. .htaccess 파일 업데이트
        add_rest_api_support_via_htaccess()
        
        print("\n" + "=" * 60)
        print("✅ 작업 완료!")
        print("=" * 60)
        print("\n💡 다음 단계:")
        print("   1. .htaccess 파일을 FTP로 업로드하세요")
        print("   2. 브라우저에서 REST API 테스트:")
        print(f"      {WP_BASE_URL}/wp-json/wp/v2/posts?per_page=1")
        print("   3. 카테고리 페이지를 새로고침하여 확인하세요")
        print("=" * 60)
        
    finally:
        print("\n⏳ 5초 후 브라우저 종료...")
        time.sleep(5)
        driver.quit()


if __name__ == "__main__":
    main()

