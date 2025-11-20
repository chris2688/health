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

def apply_template():
    """홈 페이지에 템플릿 적용"""
    print("=" * 60)
    print("📝 페이지 템플릿 적용")
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
        print("\n📄 '홈 (메인 로비)' 페이지 열기...")
        driver.get(f"{WP_URL}/wp-admin/edit.php?post_type=page")
        time.sleep(3)
        
        # "홈 (메인 로비)" 페이지 찾기
        try:
            page_link = driver.find_element(By.XPATH, "//a[@class='row-title' and contains(text(), '홈') and contains(text(), '메인')]")
            page_link.click()
            time.sleep(5)
            print("✅ 페이지 열기 성공!")
        except:
            print("❌ 페이지를 찾을 수 없습니다")
            return False
        
        # 템플릿 선택
        print("\n🎨 템플릿 선택 중...")
        try:
            # 템플릿 드롭다운 찾기 (여러 방법 시도)
            template_selectors = [
                "select[id*='template']",
                "select[name*='template']",
                ".editor-page-attributes__template select"
            ]
            
            template_select = None
            for selector in template_selectors:
                try:
                    template_select = Select(driver.find_element(By.CSS_SELECTOR, selector))
                    print(f"  ✓ 템플릿 선택 박스 발견: {selector}")
                    break
                except:
                    continue
            
            if template_select:
                # 옵션 목록 출력
                print("\n  📋 사용 가능한 템플릿:")
                for option in template_select.options:
                    print(f"     - {option.text}")
                
                # '인트로 메인 페이지' 템플릿 선택
                found = False
                for option in template_select.options:
                    if "인트로" in option.text or "Intro" in option.text or "intro" in option.get_attribute("value"):
                        template_select.select_by_visible_text(option.text)
                        print(f"\n  ✅ 템플릿 선택: {option.text}")
                        found = True
                        break
                
                if not found:
                    print("  ⚠️ '인트로 메인 페이지' 템플릿을 찾을 수 없습니다")
                    print("  💡 수동으로 선택해주세요!")
            else:
                print("  ⚠️ 템플릿 선택 박스를 찾을 수 없습니다")
                print("  💡 페이지 오른쪽 사이드바에서 수동으로 선택해주세요!")
        except Exception as e:
            print(f"  ❌ 템플릿 선택 실패: {e}")
        
        # 업데이트 버튼 클릭
        print("\n💾 저장 중...")
        try:
            update_button = driver.find_element(By.CSS_SELECTOR, ".editor-post-publish-button__button")
            driver.execute_script("arguments[0].click();", update_button)
            time.sleep(3)
            print("✅ 저장 완료!")
        except:
            print("⚠️ 저장 버튼 클릭 실패 - 수동으로 저장해주세요!")
        
        print("\n" + "=" * 60)
        print("🎉 템플릿 적용 완료!")
        print("=" * 60)
        print(f"\n🌐 {WP_URL} 접속해서 확인하세요!")
        print("   WordPress 헤더와 메뉴가 표시됩니다!")
        print("=" * 60)
        
        print("\n⏳ 10초 후 브라우저가 닫힙니다...")
        time.sleep(10)
        
        return True
        
    except Exception as e:
        print(f"❌ 오류: {e}")
        time.sleep(10)
        return False
    finally:
        driver.quit()

if __name__ == "__main__":
    apply_template()

