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

# 메인 페이지 HTML 코드
MAIN_HTML = """<style>
    /* 페이지 타이틀 숨기기 */
    .entry-title, .page-title, .entry-header {
        display: none !important;
    }
    
    /* 메인 콘텐츠 영역 스타일 */
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
</style>

<div class="health-card-container">
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

def update_home_page(driver):
    """홈 (메인 로비) 페이지 수정"""
    print("\n📝 '홈 (메인 로비)' 페이지 수정 중...")
    
    try:
        # 페이지 목록으로 이동
        driver.get(f"{WP_URL}/wp-admin/edit.php?post_type=page")
        time.sleep(3)
        
        # "홈 (메인 로비)" 페이지 찾기
        try:
            page_link = driver.find_element(By.XPATH, "//a[@class='row-title' and contains(text(), '홈') and contains(text(), '메인')]")
            page_link.click()
            time.sleep(4)
            print("  ✓ 페이지 편집 모드 진입")
        except:
            print("  ❌ '홈 (메인 로비)' 페이지를 찾을 수 없습니다")
            return False
        
        # Gutenberg 에디터에서 HTML 블록 찾기 또는 추가
        try:
            # 기존 콘텐츠 모두 삭제하고 새로 시작
            print("  ⏳ 에디터 로딩 대기 중...")
            time.sleep(5)
            
            # Ctrl+A로 전체 선택 후 삭제
            from selenium.webdriver.common.keys import Keys
            from selenium.webdriver.common.action_chains import ActionChains
            
            # 에디터 영역 클릭
            try:
                editor = driver.find_element(By.CSS_SELECTOR, ".editor-styles-wrapper, .block-editor-writing-flow")
                editor.click()
                time.sleep(1)
                
                # 전체 선택 및 삭제
                actions = ActionChains(driver)
                actions.key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).perform()
                time.sleep(1)
                actions.send_keys(Keys.DELETE).perform()
                time.sleep(1)
                print("  ✓ 기존 콘텐츠 삭제")
            except:
                print("  ℹ️ 기존 콘텐츠 삭제 건너뛰기")
            
            # 새 블록 추가 버튼 클릭
            try:
                add_button = driver.find_element(By.CSS_SELECTOR, ".block-editor-inserter__toggle, .edit-post-header-toolbar__inserter-toggle")
                add_button.click()
                time.sleep(2)
                print("  ✓ 블록 추가 버튼 클릭")
            except:
                print("  ⚠️ 블록 추가 버튼을 찾을 수 없습니다")
            
            # "사용자 정의 HTML" 검색
            try:
                search_box = driver.find_element(By.CSS_SELECTOR, "input[placeholder*='검색'], .block-editor-inserter__search input, .components-search-control__input")
                search_box.clear()
                search_box.send_keys("HTML")
                time.sleep(2)
                print("  ✓ HTML 블록 검색")
            except:
                print("  ⚠️ 검색창을 찾을 수 없습니다")
            
            # HTML 블록 선택
            try:
                html_block = driver.find_element(By.XPATH, "//button[contains(., 'Custom HTML') or contains(., '사용자 정의 HTML') or contains(., 'HTML')]")
                driver.execute_script("arguments[0].click();", html_block)
                time.sleep(3)
                print("  ✓ HTML 블록 추가")
            except:
                print("  ❌ HTML 블록을 찾을 수 없습니다")
                return False
            
            # HTML 코드 입력
            try:
                html_textarea = driver.find_element(By.CSS_SELECTOR, "textarea.block-editor-plain-text, .components-textarea-control__input")
                driver.execute_script("arguments[0].value = arguments[1];", html_textarea, MAIN_HTML)
                driver.execute_script("arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", html_textarea)
                time.sleep(2)
                print("  ✅ HTML 코드 입력 완료!")
            except Exception as e:
                print(f"  ❌ HTML 코드 입력 실패: {e}")
                return False
            
            # 업데이트 버튼 클릭
            try:
                update_button = driver.find_element(By.CSS_SELECTOR, ".editor-post-publish-button__button, .editor-post-publish-panel__toggle")
                driver.execute_script("arguments[0].click();", update_button)
                time.sleep(3)
                print("  ✅ 페이지 업데이트 완료!")
                return True
            except Exception as e:
                print(f"  ⚠️ 업데이트 버튼 클릭 실패 (수동으로 저장 필요): {e}")
                return False
                
        except Exception as e:
            print(f"  ❌ 에디터 접근 실패: {e}")
            return False
            
    except Exception as e:
        print(f"  ❌ 오류 발생: {e}")
        return False

def main():
    print("=" * 60)
    print("🏠 '홈 (메인 로비)' 페이지에 메인 카드 추가")
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
        
        # 홈 페이지 수정
        if update_home_page(driver):
            print("\n" + "=" * 60)
            print("✅ 작업 완료!")
            print("🌐 사이트를 방문해서 Ctrl+F5로 새로고침하세요!")
            print("=" * 60)
        else:
            print("\n" + "=" * 60)
            print("❌ 자동 업데이트 실패")
            print("💡 브라우저가 열려있습니다. 수동으로 HTML을 붙여넣어주세요!")
            print("=" * 60)
        
        # 브라우저 유지 (수동 확인 가능)
        print("\n⏳ 30초 후 브라우저가 닫힙니다...")
        time.sleep(30)
        
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        time.sleep(10)
    finally:
        driver.quit()

if __name__ == "__main__":
    main()

