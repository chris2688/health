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

# CSS 코드
CSS_CODE = """
/* 메인 페이지 스타일 */
.entry-title, .page-title, .entry-header {
    display: none !important;
}

.site-main {
    padding: 0 !important;
}

.health-card-container {
    padding: 60px 20px;
    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    min-height: 70vh;
}

.health-cards-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 30px;
    max-width: 1400px;
    margin: 0 auto;
    padding: 0 20px;
}

.health-card {
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

.health-card:hover {
    transform: translateY(-8px);
    box-shadow: 0 20px 40px rgba(0,0,0,0.25);
}

.health-card::before {
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

.health-card-icon {
    font-size: 48px;
    margin-bottom: 20px;
    filter: drop-shadow(0 2px 4px rgba(0,0,0,0.2));
    position: relative;
    z-index: 1;
}

.health-card h3 {
    font-size: 24px;
    font-weight: 700;
    color: #ffffff;
    margin: 0 0 12px 0;
    text-shadow: 0 2px 4px rgba(0,0,0,0.1);
    position: relative;
    z-index: 1;
}

.health-card p {
    font-size: 15px;
    color: rgba(255,255,255,0.9);
    margin: 0;
    line-height: 1.6;
    position: relative;
    z-index: 1;
}

.section-title {
    text-align: center;
    margin-bottom: 20px;
}

.section-title .subtitle {
    font-size: 16px;
    font-weight: 600;
    color: #4A90E2;
    text-transform: uppercase;
    letter-spacing: 2px;
    margin-bottom: 10px;
}

.section-title h2 {
    font-size: 42px;
    font-weight: 800;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0 0 50px 0;
}

@media (max-width: 768px) {
    .health-cards-grid {
        grid-template-columns: 1fr;
        gap: 20px;
    }
    .section-title h2 {
        font-size: 32px;
    }
}
"""

# HTML 코드
HTML_CODE = """<div class="health-card-container">
    <div class="section-title">
        <p class="subtitle">9988 건강 연구소 핵심 가이드</p>
        <h2>중년 건강의 모든 것, 분야별로 찾아보세요</h2>
    </div>
    
    <div class="health-cards-grid">
        <a href="https://health9988234.mycafe24.com/category/질환별-정보/심혈관-질환/" class="health-card" style="--card-color-1:#FF6B6B; --card-color-2:#EE5A6F;">
            <div class="health-card-icon">❤️</div>
            <h3>심혈관 질환</h3>
            <p>고혈압, 심근경색, 동맥경화</p>
        </a>
        
        <a href="https://health9988234.mycafe24.com/category/질환별-정보/당뇨병/" class="health-card" style="--card-color-1:#4ECDC4; --card-color-2:#44A08D;">
            <div class="health-card-icon">💉</div>
            <h3>당뇨병</h3>
            <p>혈당관리, 공복혈당, 합병증</p>
        </a>
        
        <a href="https://health9988234.mycafe24.com/category/질환별-정보/관절-근골격계-질환/" class="health-card" style="--card-color-1:#A18CD1; --card-color-2:#FBC2EB;">
            <div class="health-card-icon">🦴</div>
            <h3>관절/근골격계 질환</h3>
            <p>관절염, 허리디스크, 골다공증</p>
        </a>
        
        <a href="https://health9988234.mycafe24.com/category/질환별-정보/호르몬-내분비-질환/" class="health-card" style="--card-color-1:#FA709A; --card-color-2:#FEE140;">
            <div class="health-card-icon">🌡️</div>
            <h3>호르몬/내분비 질환</h3>
            <p>갱년기, 갑상선, 대사증후군</p>
        </a>
        
        <a href="https://health9988234.mycafe24.com/category/질환별-정보/정신-건강-신경계/" class="health-card" style="--card-color-1:#667eea; --card-color-2:#764ba2;">
            <div class="health-card-icon">🧠</div>
            <h3>정신 건강/신경계</h3>
            <p>우울증, 치매, 수면장애</p>
        </a>
        
        <a href="https://health9988234.mycafe24.com/category/질환별-정보/소화기-질환/" class="health-card" style="--card-color-1:#f093fb; --card-color-2:#f5576c;">
            <div class="health-card-icon">🍽️</div>
            <h3>소화기 질환</h3>
            <p>위염, 지방간, 역류성 식도염</p>
        </a>
        
        <a href="https://health9988234.mycafe24.com/category/질환별-정보/안과-치과-기타/" class="health-card" style="--card-color-1:#4facfe; --card-color-2:#00f2fe;">
            <div class="health-card-icon">👁️</div>
            <h3>안과/치과/기타</h3>
            <p>백내장, 녹내장, 치주질환</p>
        </a>
    </div>
</div>"""

def login(driver):
    """로그인"""
    print("🔐 로그인 중...")
    driver.get(f"{WP_URL}/wp-login.php")
    time.sleep(2)
    
    driver.find_element(By.ID, "user_login").send_keys(WP_USERNAME)
    driver.find_element(By.ID, "user_pass").send_keys(WP_PASSWORD)
    driver.find_element(By.ID, "wp-submit").click()
    time.sleep(3)
    print("✅ 로그인 완료!")

def add_css(driver):
    """Customizer에 CSS 추가"""
    print("\n📝 1단계: CSS 추가 중...")
    
    try:
        driver.get(f"{WP_URL}/wp-admin/customize.php")
        time.sleep(5)
        
        # Additional CSS 찾기
        try:
            css_button = driver.find_element(By.XPATH, "//button[contains(., '추가 CSS') or contains(., 'Additional CSS')]")
            driver.execute_script("arguments[0].click();", css_button)
            time.sleep(3)
        except:
            print("  ⚠️ 추가 CSS 버튼을 찾을 수 없습니다")
            return False
        
        # CSS 입력
        try:
            css_textarea = driver.find_element(By.CSS_SELECTOR, "textarea[id*='css'], textarea.code")
            existing_css = css_textarea.get_attribute('value')
            
            if "health-card-container" not in existing_css:
                new_css = existing_css + "\n\n" + CSS_CODE
                driver.execute_script("arguments[0].value = arguments[1];", css_textarea, new_css)
                driver.execute_script("arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", css_textarea)
                time.sleep(2)
                
                # Publish 버튼
                try:
                    publish_btn = driver.find_element(By.CSS_SELECTOR, "button[id='save']")
                    driver.execute_script("arguments[0].click();", publish_btn)
                    time.sleep(3)
                    print("  ✅ CSS 추가 완료!")
                    return True
                except:
                    print("  ⚠️ Publish 버튼 클릭 실패")
                    return True  # CSS는 입력됨
            else:
                print("  ℹ️ CSS가 이미 존재합니다")
                return True
        except Exception as e:
            print(f"  ❌ CSS 입력 실패: {e}")
            return False
            
    except Exception as e:
        print(f"  ❌ Customizer 접근 실패: {e}")
        return False

def update_page_html(driver):
    """페이지 HTML 업데이트"""
    print("\n📝 2단계: 페이지 HTML 업데이트 중...")
    
    try:
        # 페이지 목록
        driver.get(f"{WP_URL}/wp-admin/edit.php?post_type=page")
        time.sleep(3)
        
        # "홈 (메인 로비)" 페이지 찾기
        try:
            page_link = driver.find_element(By.XPATH, "//a[@class='row-title' and contains(text(), '홈') and contains(text(), '메인')]")
            page_link.click()
            time.sleep(5)
        except:
            print("  ❌ 페이지를 찾을 수 없습니다")
            return False
        
        # 코드 편집기로 전환
        try:
            # 옵션 메뉴 열기
            options_button = driver.find_element(By.CSS_SELECTOR, "button[aria-label='옵션'], button[aria-label='Options']")
            driver.execute_script("arguments[0].click();", options_button)
            time.sleep(1)
            
            # 코드 편집기 선택
            code_editor_button = driver.find_element(By.XPATH, "//button[contains(., '코드 편집기') or contains(., 'Code editor')]")
            driver.execute_script("arguments[0].click();", code_editor_button)
            time.sleep(2)
            print("  ✓ 코드 편집기 모드")
        except:
            print("  ℹ️ 코드 편집기 전환 건너뛰기")
        
        # HTML 코드 입력
        try:
            # 코드 영역 찾기
            code_textarea = driver.find_element(By.CSS_SELECTOR, "textarea.editor-post-text-editor")
            driver.execute_script("arguments[0].value = arguments[1];", code_textarea, HTML_CODE)
            driver.execute_script("arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", code_textarea)
            time.sleep(2)
            print("  ✓ HTML 코드 입력")
        except:
            print("  ❌ 코드 입력 실패")
            return False
        
        # 업데이트 버튼
        try:
            update_btn = driver.find_element(By.CSS_SELECTOR, ".editor-post-publish-button__button")
            driver.execute_script("arguments[0].click();", update_btn)
            time.sleep(3)
            print("  ✅ 페이지 업데이트 완료!")
            return True
        except:
            print("  ⚠️ 업데이트 버튼 클릭 실패 (수동으로 저장 필요)")
            return False
            
    except Exception as e:
        print(f"  ❌ 페이지 업데이트 실패: {e}")
        return False

def main():
    print("=" * 60)
    print("🚀 WordPress 메인 페이지 완전 수정")
    print("=" * 60)
    
    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        login(driver)
        css_ok = add_css(driver)
        html_ok = update_page_html(driver)
        
        print("\n" + "=" * 60)
        if css_ok and html_ok:
            print("✅ 모든 작업 완료!")
            print("🌐 사이트를 방문해서 Ctrl+F5로 새로고침하세요!")
        else:
            print("⚠️ 일부 작업 실패 - 브라우저에서 확인 필요")
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

