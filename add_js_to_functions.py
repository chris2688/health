import sys
import io
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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

# PHP 코드 (functions.php에 추가)
PHP_CODE = """

// 9988 건강 연구소 메인 화면
add_action('wp_footer', 'health9988_main_page_script');
function health9988_main_page_script() {
    if (is_home() || is_front_page()) {
        ?>
        <script>
        (function() {
            function waitForJQuery(callback) {
                if (typeof jQuery !== 'undefined') {
                    callback(jQuery);
                } else {
                    setTimeout(function() { waitForJQuery(callback); }, 100);
                }
            }
            
            waitForJQuery(function($) {
                if ($('body').hasClass('home') || $('body').hasClass('blog')) {
                    var mainHTML = '<div class="health-main-wrapper">' +
                        '<div class="health-main-title">' +
                        '<p class="health-main-subtitle">9988 건강 연구소 핵심 가이드</p>' +
                        '<h2 class="health-main-heading">중년 건강의 모든 것, 분야별로 찾아보세요</h2>' +
                        '</div>' +
                        '<div class="health-main-grid">' +
                        '<a href="<?php echo home_url(); ?>/category/질환별-정보/심혈관-질환/" class="health-main-card" style="--card-color-1:#FF6B6B; --card-color-2:#EE5A6F;">' +
                        '<div class="health-main-card-icon">❤️</div>' +
                        '<h3>심혈관 질환</h3>' +
                        '<p>고혈압, 심근경색, 동맥경화</p>' +
                        '</a>' +
                        '<a href="<?php echo home_url(); ?>/category/질환별-정보/당뇨병/" class="health-main-card" style="--card-color-1:#4ECDC4; --card-color-2:#44A08D;">' +
                        '<div class="health-main-card-icon">💉</div>' +
                        '<h3>당뇨병</h3>' +
                        '<p>혈당관리, 공복혈당, 합병증</p>' +
                        '</a>' +
                        '<a href="<?php echo home_url(); ?>/category/질환별-정보/관절-근골격계-질환/" class="health-main-card" style="--card-color-1:#A18CD1; --card-color-2:#FBC2EB;">' +
                        '<div class="health-main-card-icon">🦴</div>' +
                        '<h3>관절/근골격계 질환</h3>' +
                        '<p>관절염, 허리디스크, 골다공증</p>' +
                        '</a>' +
                        '<a href="<?php echo home_url(); ?>/category/질환별-정보/호르몬-내분비-질환/" class="health-main-card" style="--card-color-1:#FA709A; --card-color-2:#FEE140;">' +
                        '<div class="health-main-card-icon">🌡️</div>' +
                        '<h3>호르몬/내분비 질환</h3>' +
                        '<p>갱년기, 갑상선, 대사증후군</p>' +
                        '</a>' +
                        '<a href="<?php echo home_url(); ?>/category/질환별-정보/정신-건강-신경계/" class="health-main-card" style="--card-color-1:#667eea; --card-color-2:#764ba2;">' +
                        '<div class="health-main-card-icon">🧠</div>' +
                        '<h3>정신 건강/신경계</h3>' +
                        '<p>우울증, 치매, 수면장애</p>' +
                        '</a>' +
                        '<a href="<?php echo home_url(); ?>/category/질환별-정보/소화기-질환/" class="health-main-card" style="--card-color-1:#f093fb; --card-color-2:#f5576c;">' +
                        '<div class="health-main-card-icon">🍽️</div>' +
                        '<h3>소화기 질환</h3>' +
                        '<p>위염, 지방간, 역류성 식도염</p>' +
                        '</a>' +
                        '<a href="<?php echo home_url(); ?>/category/질환별-정보/안과-치과-기타/" class="health-main-card" style="--card-color-1:#4facfe; --card-color-2:#00f2fe;">' +
                        '<div class="health-main-card-icon">👁️</div>' +
                        '<h3>안과/치과/기타</h3>' +
                        '<p>백내장, 녹내장, 치주질환</p>' +
                        '</a>' +
                        '</div>' +
                        '</div>';
                    
                    $('.site-main').prepend(mainHTML);
                }
            });
        })();
        </script>
        <?php
    }
}
"""

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

def add_to_functions_php(driver):
    """functions.php에 PHP 코드 추가"""
    print("\n📝 functions.php에 JavaScript 추가 중...")
    
    try:
        # 테마 편집기로 이동
        driver.get(f"{WP_URL}/wp-admin/theme-editor.php")
        time.sleep(3)
        
        # functions.php 파일 찾기 및 클릭
        try:
            # 여러 방법으로 functions.php 링크 찾기
            functions_link = None
            
            # 방법 1: 직접 URL로 이동
            try:
                # 현재 테마 확인
                theme_select = driver.find_element(By.ID, "theme")
                current_theme = theme_select.get_attribute("value")
                print(f"  현재 테마: {current_theme}")
                
                # functions.php로 직접 이동
                driver.get(f"{WP_URL}/wp-admin/theme-editor.php?file=functions.php&theme={current_theme}")
                time.sleep(3)
                print("  ✓ functions.php 페이지 접근")
            except Exception as e:
                print(f"  ⚠️ 테마 선택 실패, 기본 방법 사용: {e}")
                
                # 방법 2: 링크 클릭
                try:
                    functions_link = driver.find_element(By.XPATH, "//a[contains(text(), 'functions.php') or contains(@href, 'functions.php')]")
                    functions_link.click()
                    time.sleep(3)
                    print("  ✓ functions.php 페이지 접근")
                except:
                    print("  ❌ functions.php 링크를 찾을 수 없습니다")
                    return False
        except Exception as e:
            print(f"  ❌ functions.php 접근 실패: {e}")
            return False
        
        # 코드 에디터 찾기
        try:
            code_editor = driver.find_element(By.ID, "newcontent")
            existing_code = code_editor.get_attribute('value')
            
            # 이미 코드가 있는지 확인
            if "health9988_main_page_script" in existing_code:
                print("  ℹ️ 코드가 이미 존재합니다")
                return True
            
            # 코드 추가 (파일 끝에)
            new_code = existing_code.rstrip() + "\n" + PHP_CODE
            
            # 코드 업데이트
            driver.execute_script("arguments[0].value = arguments[1];", code_editor, new_code)
            time.sleep(1)
            print("  ✓ 코드 추가 완료")
            
            # 파일 업데이트 버튼 클릭
            try:
                update_button = driver.find_element(By.ID, "submit")
                update_button.click()
                time.sleep(3)
                print("✅ functions.php 업데이트 완료!")
                return True
            except Exception as e:
                print(f"  ❌ 업데이트 버튼 클릭 실패: {e}")
                # JavaScript로 직접 폼 제출
                try:
                    driver.execute_script("document.getElementById('template').submit();")
                    time.sleep(3)
                    print("✅ functions.php 업데이트 완료! (대체 방법)")
                    return True
                except:
                    print("  ❌ 폼 제출 실패")
                    return False
                
        except Exception as e:
            print(f"  ❌ 코드 편집 실패: {e}")
            return False
            
    except Exception as e:
        print(f"  ❌ 테마 편집기 접근 실패: {e}")
        return False

def main():
    print("=" * 60)
    print("🚀 9988 건강 연구소 메인 화면 JavaScript 추가")
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
        
        # functions.php에 코드 추가
        if add_to_functions_php(driver):
            print("\n" + "=" * 60)
            print("✅ 작업 완료!")
            print("🌐 사이트를 방문해서 Ctrl+F5로 새로고침하세요!")
            print("=" * 60)
        else:
            print("\n" + "=" * 60)
            print("❌ 작업 실패")
            print("=" * 60)
        
        # 5초 대기 후 브라우저 닫기
        time.sleep(5)
        
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()

