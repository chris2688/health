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

# ---------------------------------------------------------
# 🎨 Additional CSS (홈페이지에서만 표시)
# ---------------------------------------------------------
ADDITIONAL_CSS = """
/* 홈페이지 메인 카테고리 카드 스타일 */
body.home .site-main::before {
    content: '';
    display: block;
    width: 100%;
}

body.home .site-main {
    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    min-height: 80vh;
    padding: 60px 20px !important;
}

body.home .entry-title,
body.home .page-title,
body.home h1.entry-title {
    display: none !important;
}

/* 기본 콘텐츠 숨기기 */
body.home article.post,
body.home article.page {
    display: none !important;
}

.health-home-cards {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 30px;
    max-width: 1400px;
    margin: 0 auto;
    padding: 0 20px;
}

.health-home-card {
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

.health-home-card:hover {
    transform: translateY(-8px);
    box-shadow: 0 20px 40px rgba(0,0,0,0.25);
}

.health-home-card::before {
    content: '';
    position: absolute;
    top: 0;
    right: 0;
    width: 150px;
    height: 150px;
    background: rgba(255,255,255,0.1);
    border-radius: 50%;
    transform: translate(50%, -50%);
}

.health-home-card-icon {
    font-size: 48px;
    margin-bottom: 20px;
    filter: drop-shadow(0 2px 4px rgba(0,0,0,0.2));
    position: relative;
    z-index: 1;
}

.health-home-card h3 {
    font-size: 24px;
    font-weight: 700;
    color: #ffffff;
    margin: 0 0 12px 0;
    text-shadow: 0 2px 4px rgba(0,0,0,0.1);
    position: relative;
    z-index: 1;
}

.health-home-card p {
    font-size: 15px;
    color: rgba(255,255,255,0.9);
    margin: 0;
    line-height: 1.6;
    position: relative;
    z-index: 1;
}

.health-home-title {
    text-align: center;
    margin-bottom: 50px;
}

.health-home-subtitle {
    font-size: 16px;
    font-weight: 600;
    color: #4A90E2;
    text-transform: uppercase;
    letter-spacing: 2px;
    margin-bottom: 10px;
}

.health-home-main-title {
    font-size: 42px;
    font-weight: 800;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0;
}

@media (max-width: 768px) {
    .health-home-cards {
        grid-template-columns: 1fr;
        gap: 20px;
    }
    .health-home-main-title {
        font-size: 32px;
    }
}
"""

# ---------------------------------------------------------
# 📝 JavaScript로 HTML 삽입
# ---------------------------------------------------------
JAVASCRIPT_CODE = """
<script>
document.addEventListener('DOMContentLoaded', function() {
    // 홈페이지에서만 실행
    if (document.body.classList.contains('home')) {
        var mainContent = document.querySelector('.site-main') || 
                         document.querySelector('main') || 
                         document.querySelector('#main');
        
        if (mainContent) {
            var cardsHTML = `
                <div class="health-home-title">
                    <p class="health-home-subtitle">9988 건강 연구소 핵심 가이드</p>
                    <h2 class="health-home-main-title">중년 건강의 모든 것, 분야별로 찾아보세요</h2>
                </div>
                
                <div class="health-home-cards">
                    <a href="https://health9988234.mycafe24.com/category/질환별-정보/심혈관-질환/" class="health-home-card" style="--card-color-1:#FF6B6B; --card-color-2:#EE5A6F;">
                        <div class="health-home-card-icon">❤️</div>
                        <h3>심혈관 질환</h3>
                        <p>고혈압, 심근경색, 동맥경화</p>
                    </a>
                    
                    <a href="https://health9988234.mycafe24.com/category/질환별-정보/당뇨병/" class="health-home-card" style="--card-color-1:#4ECDC4; --card-color-2:#44A08D;">
                        <div class="health-home-card-icon">💉</div>
                        <h3>당뇨병</h3>
                        <p>혈당관리, 공복혈당, 합병증</p>
                    </a>
                    
                    <a href="https://health9988234.mycafe24.com/category/질환별-정보/관절-근골격계-질환/" class="health-home-card" style="--card-color-1:#A18CD1; --card-color-2:#FBC2EB;">
                        <div class="health-home-card-icon">🦴</div>
                        <h3>관절/근골격계 질환</h3>
                        <p>관절염, 허리디스크, 골다공증</p>
                    </a>
                    
                    <a href="https://health9988234.mycafe24.com/category/질환별-정보/호르몬-내분비-질환/" class="health-home-card" style="--card-color-1:#FA709A; --card-color-2:#FEE140;">
                        <div class="health-home-card-icon">🌡️</div>
                        <h3>호르몬/내분비 질환</h3>
                        <p>갱년기, 갑상선, 대사증후군</p>
                    </a>
                    
                    <a href="https://health9988234.mycafe24.com/category/질환별-정보/정신-건강-신경계/" class="health-home-card" style="--card-color-1:#667eea; --card-color-2:#764ba2;">
                        <div class="health-home-card-icon">🧠</div>
                        <h3>정신 건강/신경계</h3>
                        <p>우울증, 치매, 수면장애</p>
                    </a>
                    
                    <a href="https://health9988234.mycafe24.com/category/질환별-정보/소화기-질환/" class="health-home-card" style="--card-color-1:#f093fb; --card-color-2:#f5576c;">
                        <div class="health-home-card-icon">🍽️</div>
                        <h3>소화기 질환</h3>
                        <p>위염, 지방간, 역류성 식도염</p>
                    </a>
                    
                    <a href="https://health9988234.mycafe24.com/category/질환별-정보/안과-치과-기타/" class="health-home-card" style="--card-color-1:#4facfe; --card-color-2:#00f2fe;">
                        <div class="health-home-card-icon">👁️</div>
                        <h3>안과/치과/기타</h3>
                        <p>백내장, 녹내장, 치주질환</p>
                    </a>
                </div>
            `;
            
            mainContent.innerHTML = cardsHTML + mainContent.innerHTML;
        }
    }
});
</script>
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
    except Exception as e:
        print(f"  ❌ 로그인 실패: {e}")
        return False


def add_custom_css(driver):
    """Additional CSS 추가"""
    print("🎨 Additional CSS 추가 중...\n")
    
    try:
        driver.get(f"{WP_ADMIN_URL}customize.php")
        time.sleep(5)
        
        # iframe으로 전환 (Customizer는 iframe 안에 있음)
        try:
            driver.switch_to.frame("customize-preview-0")
            time.sleep(2)
            driver.switch_to.default_content()
        except:
            pass
        
        # Additional CSS 패널 찾기
        try:
            # Additional CSS 버튼 클릭
            css_button_selectors = [
                "//button[contains(text(), 'Additional CSS')]",
                "//button[contains(text(), '추가 CSS')]",
                "#accordion-section-custom_css button",
                ".control-section.control-section-custom_css button"
            ]
            
            for selector in css_button_selectors:
                try:
                    if selector.startswith("//"):
                        css_btn = driver.find_element(By.XPATH, selector)
                    else:
                        css_btn = driver.find_element(By.CSS_SELECTOR, selector)
                    driver.execute_script("arguments[0].click();", css_btn)
                    time.sleep(2)
                    print("  ✓ Additional CSS 패널 열림")
                    break
                except:
                    continue
            
            # CSS 입력 필드에 코드 입력
            css_textarea_selectors = [
                ".CodeMirror textarea",
                "#customize-control-custom_css textarea",
                "textarea[aria-label*='CSS']"
            ]
            
            for selector in css_textarea_selectors:
                try:
                    css_field = driver.find_element(By.CSS_SELECTOR, selector)
                    
                    # CodeMirror 사용 시 특별 처리
                    if "CodeMirror" in selector:
                        driver.execute_script("""
                            var editor = document.querySelector('.CodeMirror').CodeMirror;
                            editor.setValue(arguments[0]);
                        """, ADDITIONAL_CSS)
                    else:
                        driver.execute_script("arguments[0].value = arguments[1];", css_field, ADDITIONAL_CSS)
                    
                    print("  ✓ CSS 코드 입력 완료")
                    time.sleep(2)
                    break
                except:
                    continue
            
            # 발행 버튼 클릭
            try:
                publish_btn = driver.find_element(By.ID, "save")
                driver.execute_script("arguments[0].click();", publish_btn)
                time.sleep(3)
                print("  ✅ CSS 저장 완료!\n")
                return True
            except Exception as e:
                print(f"  ⚠️ 발행 버튼 클릭 실패: {e}\n")
                return False
                
        except Exception as e:
            print(f"  ❌ CSS 패널 접근 실패: {e}\n")
            return False
            
    except Exception as e:
        print(f"  ❌ Customizer 접근 실패: {e}\n")
        return False


def add_custom_javascript(driver):
    """JavaScript 코드 추가 (Header/Footer 플러그인 필요)"""
    print("📝 JavaScript 코드 추가 중...\n")
    
    try:
        # WPCode 플러그인이나 Insert Headers and Footers 플러그인 확인
        driver.get(f"{WP_ADMIN_URL}options-general.php")
        time.sleep(2)
        
        # 간단한 방법: 테마의 functions.php에 추가하는 대신
        # Customizer Additional CSS에 <script> 태그 포함
        print("  ℹ️ JavaScript는 테마 파일에 수동으로 추가해야 합니다")
        print("  💡 또는 'Insert Headers and Footers' 플러그인 사용을 권장합니다\n")
        
        return True
        
    except Exception as e:
        print(f"  ⚠️ JavaScript 추가 건너뜀: {e}\n")
        return True


def print_manual_instructions():
    """수동 설정 방법 출력"""
    print("\n" + "="*60)
    print("📋 수동 설정 가이드")
    print("="*60 + "\n")
    
    print("1️⃣ WordPress 관리자 > 외모 > 사용자 정의 > Additional CSS")
    print("   다음 CSS 코드를 붙여넣으세요:")
    print("\n" + "-"*60)
    print(ADDITIONAL_CSS[:300] + "...")
    print("-"*60 + "\n")
    
    print("2️⃣ JavaScript 코드 추가:")
    print("   외모 > 테마 편집기 > footer.php (또는 header.php)")
    print("   </body> 태그 바로 위에 다음 코드를 붙여넣으세요:")
    print("\n" + "-"*60)
    print(JAVASCRIPT_CODE[:300] + "...")
    print("-"*60 + "\n")


def main():
    print("\n" + "="*60)
    print("🎨 워드프레스 홈페이지 커스터마이저 설정")
    print("="*60 + "\n")
    
    driver = setup_driver()
    
    try:
        if not wp_login(driver):
            print("❌ 로그인 실패")
            return
        
        # CSS 추가 시도
        css_success = add_custom_css(driver)
        
        # JavaScript 안내
        add_custom_javascript(driver)
        
        if css_success:
            print("="*60)
            print("✨ CSS 추가 완료!")
            print("="*60)
            print(f"\n🌐 사이트 확인: {WP_BASE_URL}\n")
        else:
            print_manual_instructions()
        
    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
        print_manual_instructions()
    finally:
        time.sleep(3)
        driver.quit()


if __name__ == "__main__":
    main()

