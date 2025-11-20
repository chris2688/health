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

# CSS 코드
CUSTOM_CSS = """
/* === 메인 화면 스타일 === */
body.home .site-main, body.blog .site-main { 
    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%) !important; 
    padding: 60px 20px !important; 
    min-height: 80vh !important; 
}

body.home .site-main > *:not(.health-main-wrapper), 
body.blog .site-main > *:not(.health-main-wrapper) { 
    display: none !important; 
}

.health-main-wrapper { max-width: 1400px; margin: 0 auto; }
.health-main-title { text-align: center; margin-bottom: 50px; }
.health-main-subtitle { 
    font-size: 16px; font-weight: 600; color: #4A90E2; 
    text-transform: uppercase; letter-spacing: 2px; margin-bottom: 10px; 
}
.health-main-heading { 
    font-size: 42px; font-weight: 800; 
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; 
    background-clip: text; margin: 0; 
}
.health-main-grid { 
    display: grid; 
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); 
    gap: 30px; 
    padding: 0 20px; 
}
.health-main-card { 
    position: relative; 
    padding: 40px 30px; 
    border-radius: 24px; 
    background: linear-gradient(135deg, var(--card-color-1) 0%, var(--card-color-2) 100%); 
    box-shadow: 0 10px 30px rgba(0,0,0,0.15); 
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1); 
    cursor: pointer; 
    overflow: hidden; 
    min-height: 220px; 
    display: flex; 
    flex-direction: column; 
    justify-content: center; 
    text-decoration: none; 
}
.health-main-card:hover { 
    transform: translateY(-8px); 
    box-shadow: 0 20px 40px rgba(0,0,0,0.25); 
}
.health-main-card::before { 
    content: ''; position: absolute; top: 0; right: 0; 
    width: 150px; height: 150px; 
    background: rgba(255,255,255,0.1); 
    border-radius: 50%; 
    transform: translate(50%, -50%); 
}
.health-main-card-icon { 
    font-size: 48px; margin-bottom: 20px; 
    filter: drop-shadow(0 2px 4px rgba(0,0,0,0.2)); 
    position: relative; z-index: 1; 
}
.health-main-card h3 { 
    font-size: 24px; font-weight: 700; color: #ffffff; 
    margin: 0 0 12px 0; text-shadow: 0 2px 4px rgba(0,0,0,0.1); 
    position: relative; z-index: 1; 
}
.health-main-card p { 
    font-size: 15px; color: rgba(255,255,255,0.9); 
    margin: 0; line-height: 1.6; 
    position: relative; z-index: 1; 
}
@media (max-width: 768px) { 
    .health-main-grid { grid-template-columns: 1fr; gap: 20px; } 
    .health-main-heading { font-size: 32px; } 
}
"""

# JavaScript 코드
CUSTOM_JS = """
<script>
(function() {
    // jQuery가 로드될 때까지 기다림
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
                '<a href="https://health9988234.mycafe24.com/category/질환별-정보/심혈관-질환/" class="health-main-card" style="--card-color-1:#FF6B6B; --card-color-2:#EE5A6F;">' +
                '<div class="health-main-card-icon">❤️</div>' +
                '<h3>심혈관 질환</h3>' +
                '<p>고혈압, 심근경색, 동맥경화</p>' +
                '</a>' +
                '<a href="https://health9988234.mycafe24.com/category/질환별-정보/당뇨병/" class="health-main-card" style="--card-color-1:#4ECDC4; --card-color-2:#44A08D;">' +
                '<div class="health-main-card-icon">💉</div>' +
                '<h3>당뇨병</h3>' +
                '<p>혈당관리, 공복혈당, 합병증</p>' +
                '</a>' +
                '<a href="https://health9988234.mycafe24.com/category/질환별-정보/관절-근골격계-질환/" class="health-main-card" style="--card-color-1:#A18CD1; --card-color-2:#FBC2EB;">' +
                '<div class="health-main-card-icon">🦴</div>' +
                '<h3>관절/근골격계 질환</h3>' +
                '<p>관절염, 허리디스크, 골다공증</p>' +
                '</a>' +
                '<a href="https://health9988234.mycafe24.com/category/질환별-정보/호르몬-내분비-질환/" class="health-main-card" style="--card-color-1:#FA709A; --card-color-2:#FEE140;">' +
                '<div class="health-main-card-icon">🌡️</div>' +
                '<h3>호르몬/내분비 질환</h3>' +
                '<p>갱년기, 갑상선, 대사증후군</p>' +
                '</a>' +
                '<a href="https://health9988234.mycafe24.com/category/질환별-정보/정신-건강-신경계/" class="health-main-card" style="--card-color-1:#667eea; --card-color-2:#764ba2;">' +
                '<div class="health-main-card-icon">🧠</div>' +
                '<h3>정신 건강/신경계</h3>' +
                '<p>우울증, 치매, 수면장애</p>' +
                '</a>' +
                '<a href="https://health9988234.mycafe24.com/category/질환별-정보/소화기-질환/" class="health-main-card" style="--card-color-1:#f093fb; --card-color-2:#f5576c;">' +
                '<div class="health-main-card-icon">🍽️</div>' +
                '<h3>소화기 질환</h3>' +
                '<p>위염, 지방간, 역류성 식도염</p>' +
                '</a>' +
                '<a href="https://health9988234.mycafe24.com/category/질환별-정보/안과-치과-기타/" class="health-main-card" style="--card-color-1:#4facfe; --card-color-2:#00f2fe;">' +
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

def add_custom_css(driver):
    """Customizer를 통해 CSS 추가"""
    print("\n📝 메인 화면 CSS 추가 중...")
    
    try:
        # Customizer 열기
        driver.get(f"{WP_URL}/wp-admin/customize.php")
        time.sleep(5)
        
        # iframe으로 전환할 필요가 있을 수 있음
        try:
            # "Additional CSS" 버튼 찾기 (여러 가능한 선택자 시도)
            additional_css_button = None
            selectors = [
                "//button[contains(., '추가 CSS')]",
                "//button[contains(., 'Additional CSS')]",
                "//li[@id='accordion-section-custom_css']",
                "//*[contains(text(), '추가 CSS')]",
                "//*[contains(text(), 'Additional CSS')]"
            ]
            
            for selector in selectors:
                try:
                    additional_css_button = driver.find_element(By.XPATH, selector)
                    if additional_css_button:
                        break
                except:
                    continue
            
            if additional_css_button:
                driver.execute_script("arguments[0].scrollIntoView(true);", additional_css_button)
                time.sleep(1)
                driver.execute_script("arguments[0].click();", additional_css_button)
                time.sleep(3)
                
                # CSS 입력 필드 찾기
                css_textarea = None
                css_selectors = [
                    "//textarea[@id='custom_css']",
                    "//textarea[contains(@class, 'code')]",
                    "//textarea[contains(@id, 'css')]"
                ]
                
                for selector in css_selectors:
                    try:
                        css_textarea = driver.find_element(By.XPATH, selector)
                        if css_textarea:
                            break
                    except:
                        continue
                
                if css_textarea:
                    # 기존 CSS 가져오기
                    existing_css = css_textarea.get_attribute('value')
                    
                    # 새 CSS 추가 (중복 방지)
                    if "health-main-wrapper" not in existing_css:
                        new_css = existing_css + "\n\n" + CUSTOM_CSS
                        driver.execute_script("arguments[0].value = arguments[1];", css_textarea, new_css)
                        
                        # 변경사항 트리거
                        driver.execute_script("arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", css_textarea)
                        time.sleep(2)
                        
                        # Publish 버튼 찾기
                        publish_selectors = [
                            "//button[@id='save']",
                            "//button[contains(., '게시')]",
                            "//button[contains(., 'Publish')]",
                            "//input[@id='save']"
                        ]
                        
                        for selector in publish_selectors:
                            try:
                                publish_button = driver.find_element(By.XPATH, selector)
                                if publish_button and publish_button.is_displayed():
                                    driver.execute_script("arguments[0].click();", publish_button)
                                    time.sleep(3)
                                    print("✅ CSS 추가 완료!")
                                    return True
                            except:
                                continue
                        
                        print("⚠️ Publish 버튼을 찾을 수 없지만 CSS는 입력됨")
                        return True
                    else:
                        print("ℹ️ CSS가 이미 존재합니다")
                        return True
                else:
                    print("❌ CSS 입력 필드를 찾을 수 없습니다")
                    return False
            else:
                print("❌ Additional CSS 버튼을 찾을 수 없습니다")
                return False
                
        except Exception as e:
            print(f"❌ CSS 추가 실패: {e}")
            return False
            
    except Exception as e:
        print(f"❌ Customizer 접근 실패: {e}")
        return False

def add_footer_js(driver):
    """footer.php에 JavaScript 추가"""
    print("\n📝 메인 화면 JavaScript 추가 중...")
    
    try:
        # 테마 편집기 열기
        driver.get(f"{WP_URL}/wp-admin/theme-editor.php")
        time.sleep(3)
        
        # footer.php 찾기
        try:
            footer_link = driver.find_element(By.XPATH, "//a[contains(@href, 'footer.php')]")
            footer_link.click()
            time.sleep(3)
        except:
            print("❌ footer.php 링크를 찾을 수 없습니다")
            return False
        
        # 코드 에디터 찾기
        try:
            code_editor = driver.find_element(By.ID, "newcontent")
            existing_code = code_editor.get_attribute('value')
            
            # </body> 태그 찾기
            if "</body>" in existing_code and "health-main-wrapper" not in existing_code:
                # JavaScript를 </body> 앞에 삽입
                new_code = existing_code.replace("</body>", CUSTOM_JS + "\n</body>")
                
                # 코드 업데이트
                driver.execute_script("arguments[0].value = arguments[1];", code_editor, new_code)
                time.sleep(1)
                
                # 파일 업데이트 버튼 클릭
                update_button = driver.find_element(By.ID, "submit")
                update_button.click()
                time.sleep(3)
                
                print("✅ JavaScript 추가 완료!")
                return True
            elif "health-main-wrapper" in existing_code:
                print("ℹ️ JavaScript가 이미 존재합니다")
                return True
            else:
                print("❌ </body> 태그를 찾을 수 없습니다")
                return False
                
        except Exception as e:
            print(f"❌ 코드 편집 실패: {e}")
            return False
            
    except Exception as e:
        print(f"❌ 테마 편집기 접근 실패: {e}")
        return False

def main():
    print("=" * 60)
    print("🚀 9988 건강 연구소 메인 화면 자동 설치")
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
        
        # CSS 추가
        css_success = add_custom_css(driver)
        
        # JavaScript 추가
        js_success = add_footer_js(driver)
        
        print("\n" + "=" * 60)
        if css_success and js_success:
            print("✅ 모든 작업 완료!")
            print("🌐 사이트를 방문해서 Ctrl+F5로 새로고침하세요!")
        elif css_success:
            print("⚠️ CSS는 추가되었지만 JavaScript 추가 실패")
            print("💡 수동으로 footer.php에 JavaScript를 추가해주세요")
        else:
            print("❌ 작업 실패 - 수동으로 진행해주세요")
        print("=" * 60)
        
        # 5초 대기 후 브라우저 닫기
        time.sleep(5)
        
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()

