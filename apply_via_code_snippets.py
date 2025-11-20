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

WP_LOGIN_URL = "https://health9988234.mycafe24.com/wp-login.php"
WP_ADMIN_URL = "https://health9988234.mycafe24.com/wp-admin/"
WP_USER = "health9988234"
WP_PASSWORD = "ssurlf7904!"
WP_BASE_URL = "https://health9988234.mycafe24.com"

# 완전한 PHP 코드 (functions.php에 추가용)
PHP_CODE = """
// 9988 건강 연구소 메인 화면
add_action('wp_footer', 'health_main_cards_9988');
function health_main_cards_9988() {
    if (is_home() || is_front_page()) {
        ?>
        <script>
        jQuery(document).ready(function($) {
            if ($('body').hasClass('home') || $('body').hasClass('blog')) {
                var mainHTML = '<div class="health-main-wrapper"><div class="health-main-title"><p class="health-main-subtitle">9988 건강 연구소 핵심 가이드</p><h2 class="health-main-heading">중년 건강의 모든 것, 분야별로 찾아보세요</h2></div><div class="health-main-grid"><a href="https://health9988234.mycafe24.com/category/질환별-정보/심혈관-질환/" class="health-main-card" style="--card-color-1:#FF6B6B; --card-color-2:#EE5A6F;"><div class="health-main-card-icon">❤️</div><h3>심혈관 질환</h3><p>고혈압, 심근경색, 동맥경화</p></a><a href="https://health9988234.mycafe24.com/category/질환별-정보/당뇨병/" class="health-main-card" style="--card-color-1:#4ECDC4; --card-color-2:#44A08D;"><div class="health-main-card-icon">💉</div><h3>당뇨병</h3><p>혈당관리, 공복혈당, 합병증</p></a><a href="https://health9988234.mycafe24.com/category/질환별-정보/관절-근골격계-질환/" class="health-main-card" style="--card-color-1:#A18CD1; --card-color-2:#FBC2EB;"><div class="health-main-card-icon">🦴</div><h3>관절/근골격계 질환</h3><p>관절염, 허리디스크, 골다공증</p></a><a href="https://health9988234.mycafe24.com/category/질환별-정보/호르몬-내분비-질환/" class="health-main-card" style="--card-color-1:#FA709A; --card-color-2:#FEE140;"><div class="health-main-card-icon">🌡️</div><h3>호르몬/내분비 질환</h3><p>갱년기, 갑상선, 대사증후군</p></a><a href="https://health9988234.mycafe24.com/category/질환별-정보/정신-건강-신경계/" class="health-main-card" style="--card-color-1:#667eea; --card-color-2:#764ba2;"><div class="health-main-card-icon">🧠</div><h3>정신 건강/신경계</h3><p>우울증, 치매, 수면장애</p></a><a href="https://health9988234.mycafe24.com/category/질환별-정보/소화기-질환/" class="health-main-card" style="--card-color-1:#f093fb; --card-color-2:#f5576c;"><div class="health-main-card-icon">🍽️</div><h3>소화기 질환</h3><p>위염, 지방간, 역류성 식도염</p></a><a href="https://health9988234.mycafe24.com/category/질환별-정보/안과-치과-기타/" class="health-main-card" style="--card-color-1:#4facfe; --card-color-2:#00f2fe;"><div class="health-main-card-icon">👁️</div><h3>안과/치과/기타</h3><p>백내장, 녹내장, 치주질환</p></a></div></div>';
                $('.site-main').prepend(mainHTML);
            }
        });
        </script>
        <?php
    }
}
"""


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
    except:
        return False


def add_via_code_snippets(driver):
    """Code Snippets 플러그인을 통해 코드 추가"""
    print("📝 Code Snippets에 코드 추가 중...\n")
    
    try:
        # Code Snippets 새 스니펫 추가 페이지로 이동
        driver.get(f"{WP_ADMIN_URL}admin.php?page=add-snippet")
        time.sleep(3)
        
        print("  ✓ Code Snippets 페이지 접근")
        
        # 제목 입력
        try:
            title_field = driver.find_element(By.ID, "title")
            title_field.clear()
            title_field.send_keys("9988 건강 연구소 메인 화면")
            print("  ✓ 제목 입력 완료")
            time.sleep(1)
        except:
            print("  ⚠️ 제목 입력 건너뜀")
        
        # 코드 입력
        try:
            # CodeMirror 에디터 찾기
            code_editor = driver.find_element(By.CSS_SELECTOR, ".CodeMirror")
            driver.execute_script("""
                var editor = arguments[0].CodeMirror;
                editor.setValue(arguments[1]);
            """, code_editor, PHP_CODE)
            print("  ✓ PHP 코드 입력 완료")
            time.sleep(2)
        except:
            # 일반 textarea 시도
            try:
                code_field = driver.find_element(By.ID, "snippet_code")
                driver.execute_script("arguments[0].value = arguments[1];", code_field, PHP_CODE)
                print("  ✓ PHP 코드 입력 완료 (textarea)")
                time.sleep(2)
            except Exception as e:
                print(f"  ❌ 코드 입력 실패: {e}")
                return False
        
        # 저장 및 활성화 버튼 클릭
        try:
            # "Save Changes and Activate" 버튼 찾기
            save_activate_btn = driver.find_element(By.NAME, "save_snippet_activate")
            driver.execute_script("arguments[0].click();", save_activate_btn)
            time.sleep(3)
            print("  ✅ 스니펫 저장 및 활성화 완료!")
            return True
        except:
            # 일반 저장 버튼 시도
            try:
                save_btn = driver.find_element(By.NAME, "save_snippet")
                driver.execute_script("arguments[0].click();", save_btn)
                time.sleep(2)
                print("  ✅ 스니펫 저장 완료!")
                
                # 활성화 체크박스
                try:
                    active_checkbox = driver.find_element(By.NAME, "snippet_active")
                    if not active_checkbox.is_selected():
                        driver.execute_script("arguments[0].click();", active_checkbox)
                        time.sleep(1)
                    print("  ✅ 스니펫 활성화 완료!")
                except:
                    print("  ⚠️ 활성화는 수동으로 해주세요")
                
                return True
            except Exception as e:
                print(f"  ❌ 저장 버튼을 찾을 수 없습니다: {e}")
                return False
                
    except Exception as e:
        print(f"  ❌ Code Snippets 접근 실패: {e}")
        print("  💡 Code Snippets 플러그인이 설치되어 있지 않을 수 있습니다")
        return False


def add_to_functions_php(driver):
    """functions.php에 직접 코드 추가"""
    print("\n📝 functions.php에 코드 추가 중...\n")
    
    try:
        # 외모 > 테마 편집기로 이동
        driver.get(f"{WP_ADMIN_URL}theme-editor.php")
        time.sleep(3)
        
        print("  ✓ 테마 편집기 접근")
        
        # functions.php 선택
        try:
            functions_link = driver.find_element(By.XPATH, "//a[contains(@href, 'functions.php')]")
            driver.execute_script("arguments[0].click();", functions_link)
            time.sleep(2)
            print("  ✓ functions.php 파일 열림")
        except:
            print("  ℹ️ functions.php가 이미 선택되어 있습니다")
        
        # 코드 편집기 찾기
        try:
            # textarea 찾기
            editor = driver.find_element(By.ID, "newcontent")
            current_content = driver.execute_script("return arguments[0].value;", editor)
            
            if "9988 건강 연구소" in current_content:
                print("  ℹ️ 코드가 이미 추가되어 있습니다")
                return True
            
            # 맨 끝에 코드 추가
            new_content = current_content.rstrip() + "\n\n" + PHP_CODE
            driver.execute_script("arguments[0].value = arguments[1];", editor, new_content)
            print("  ✓ PHP 코드 입력 완료")
            time.sleep(1)
            
            # 저장
            save_btn = driver.find_element(By.ID, "submit")
            driver.execute_script("arguments[0].click();", save_btn)
            time.sleep(2)
            print("  ✅ functions.php 저장 완료!")
            return True
            
        except Exception as e:
            print(f"  ❌ 편집기 접근 실패: {e}")
            return False
            
    except Exception as e:
        print(f"  ❌ 테마 편집기 접근 실패: {e}")
        return False


def main():
    print("\n" + "="*60)
    print("🎨 워드프레스 메인 화면 자동 적용")
    print("="*60 + "\n")
    
    driver = setup_driver()
    
    try:
        if not wp_login(driver):
            print("❌ 로그인 실패")
            return
        
        # 방법 1: Code Snippets 시도
        print("📌 방법 1: Code Snippets 플러그인 사용\n")
        snippet_success = add_via_code_snippets(driver)
        
        if not snippet_success:
            # 방법 2: functions.php에 직접 추가
            print("\n📌 방법 2: functions.php 직접 수정\n")
            functions_success = add_to_functions_php(driver)
            
            if functions_success:
                snippet_success = True
        
        if snippet_success:
            print("\n" + "="*60)
            print("✨ 완료!")
            print("="*60)
            print(f"\n🌐 사이트 확인: {WP_BASE_URL}")
            print("\n💡 메인 화면에 7개의 카테고리 카드가 표시됩니다!")
            print("   Ctrl+F5로 새로고침하세요.\n")
        else:
            print("\n⚠️ 자동 적용 실패")
            print("\n💡 수동으로 코드를 추가해주세요:")
            print("   화면에 나와있는 방법을 따라하시면 됩니다.\n")
        
    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
    finally:
        time.sleep(3)
        driver.quit()


if __name__ == "__main__":
    main()

