import sys
import io
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException, TimeoutException

# ---------------------------------------------------------
# ✅ 설정 변수 (로그인 정보 및 워드프레스 주소)
# ---------------------------------------------------------
WP_LOGIN_URL = "https://health9988234.mycafe24.com/wp-login.php"
WP_ADMIN_URL = "https://health9988234.mycafe24.com/wp-admin/"
WP_USER = "health9988234"
WP_PASSWORD = "ssurlf7904!" 

# ---------------------------------------------------------
# 🎨 메인 페이지에 주입할 HTML 블록 코드 (7개 질환별 카드)
# ---------------------------------------------------------
HOMEPAGE_BLOCK_HTML = """
<style>
/* 페이지 제목 숨기기 */
.page-id-2055 .entry-title,
.page-id-2055 h1.entry-title {
    display: none !important;
}
.health-card-container {
    padding: 60px 20px;
    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
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
.health-card a {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: 100;
    text-indent: -9999px;
    overflow: hidden;
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
        <div class="health-card" style="--card-color-1:#FF6B6B; --card-color-2:#EE5A6F;">
            <div class="health-card-icon">❤️</div>
            <h3>심혈관 질환</h3>
            <p>고혈압, 심근경색, 동맥경화</p>
            <a href="[WP_URL]/category/질환별-정보/심혈관-질환/" aria-label="심혈관 질환"></a>
        </div>
        
        <div class="health-card" style="--card-color-1:#4ECDC4; --card-color-2:#44A08D;">
            <div class="health-card-icon">💉</div>
            <h3>당뇨병</h3>
            <p>혈당관리, 공복혈당, 합병증</p>
            <a href="[WP_URL]/category/질환별-정보/당뇨병/" aria-label="당뇨병"></a>
        </div>
        
        <div class="health-card" style="--card-color-1:#A18CD1; --card-color-2:#FBC2EB;">
            <div class="health-card-icon">🦴</div>
            <h3>관절/근골격계 질환</h3>
            <p>관절염, 허리디스크, 골다공증</p>
            <a href="[WP_URL]/category/질환별-정보/관절-근골격계-질환/" aria-label="관절/근골격계 질환"></a>
        </div>
        
        <div class="health-card" style="--card-color-1:#FA709A; --card-color-2:#FEE140;">
            <div class="health-card-icon">🌡️</div>
            <h3>호르몬/내분비 질환</h3>
            <p>갱년기, 갑상선, 대사증후군</p>
            <a href="[WP_URL]/category/질환별-정보/호르몬-내분비-질환/" aria-label="호르몬/내분비 질환"></a>
        </div>
        
        <div class="health-card" style="--card-color-1:#667eea; --card-color-2:#764ba2;">
            <div class="health-card-icon">🧠</div>
            <h3>정신 건강/신경계</h3>
            <p>우울증, 치매, 수면장애</p>
            <a href="[WP_URL]/category/질환별-정보/정신-건강-신경계/" aria-label="정신 건강/신경계"></a>
        </div>
        
        <div class="health-card" style="--card-color-1:#f093fb; --card-color-2:#f5576c;">
            <div class="health-card-icon">🍽️</div>
            <h3>소화기 질환</h3>
            <p>위염, 지방간, 역류성 식도염</p>
            <a href="[WP_URL]/category/질환별-정보/소화기-질환/" aria-label="소화기 질환"></a>
        </div>
        
        <div class="health-card" style="--card-color-1:#4facfe; --card-color-2:#00f2fe;">
            <div class="health-card-icon">👁️</div>
            <h3>안과/치과/기타</h3>
            <p>백내장, 녹내장, 치주질환</p>
            <a href="[WP_URL]/category/질환별-정보/안과-치과-기타/" aria-label="안과/치과/기타"></a>
        </div>
    </div>
</div>
"""

# ---------------------------------------------------------
# ✅ Step 1: Python Script (Inject the Blocks)
# ---------------------------------------------------------

def setup_driver():
    """Chrome WebDriver 설정"""
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    return driver


def wp_login(driver):
    """WordPress 로그인"""
    print(f"🔐 WordPress 로그인 시도: {WP_LOGIN_URL}")
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
        else:
            return False
    except Exception as e:
        print(f"  ❌ 로그인 중 오류: {e}")
        return False


def inject_homepage_cards(driver):
    print("\n--- 🎨 홈 페이지 카드 자동 삽입 시작 ---")
    
    # 1. '홈 (메인 로비)' 페이지 ID 찾기
    try:
        driver.get(WP_ADMIN_URL + "edit.php?post_type=page")
        page_row = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//a[contains(text(), '홈 (메인 로비)')]"))
        )
        page_id = page_row.get_attribute("href").split('post=')[1].split('&')[0]
        edit_url = f"{WP_ADMIN_URL}post.php?post={page_id}&action=edit"
        print(f"  ✓ '홈 (메인 로비)' 페이지 ID 획득: {page_id}")
    except Exception as e:
        print(f"  ❌ '홈 (메인 로비)' 페이지를 찾을 수 없습니다. 페이지를 만들어 발행했는지 확인하세요.")
        return

    # 2. 페이지 편집 화면으로 이동
    driver.get(edit_url)
    print("  ⏳ 페이지 편집기 로딩 중...")
    time.sleep(10)  # 편집기 로딩 충분히 대기
    print("  ✓ 편집기 로딩 완료")

    # 3. Content Injector (코드 에디터 강제 주입)
    try:
        # 1. '코드 편집기' 버튼 클릭 (Code Editor or HTML Mode)
        # CSS selector for the Code Editor button in Gutenberg's top bar
        print("  📝 코드 에디터로 전환 및 코드 주입 중...")
        time.sleep(3)  # 추가 안정화 대기
        
        # 다양한 셀렉터 시도
        code_editor_button = None
        selectors = [
            "button[aria-label*='코드 편집기']",
            "button[aria-label*='Code editor']",
            ".editor-post-text-editor",  # 직접 텍스트 에디터 버튼
            "button.components-button[aria-label*='editor']"
        ]
        
        for selector in selectors:
            try:
                code_editor_button = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                )
                print(f"  ✓ 코드 에디터 버튼 발견: {selector}")
                break
            except:
                continue
        
        if not code_editor_button:
            # 키보드 단축키 사용 시도 (Ctrl+Shift+Alt+M)
            print("  ⌨️ 키보드 단축키로 코드 에디터 전환 시도...")
            from selenium.webdriver.common.keys import Keys
            from selenium.webdriver.common.action_chains import ActionChains
            actions = ActionChains(driver)
            actions.key_down(Keys.CONTROL).key_down(Keys.SHIFT).key_down(Keys.ALT).send_keys('m').key_up(Keys.ALT).key_up(Keys.SHIFT).key_up(Keys.CONTROL).perform()
            time.sleep(2)
        else:
            code_editor_button.click()
            time.sleep(2) 

        # 2. 코드 입력창 찾기 (Gutenberg code editor textarea or Classic Editor)
        code_editor_textarea = None
        
        # Gutenberg 코드 에디터 시도
        try:
            code_editor_textarea = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, "editor-post-text-editor"))
            )
            print("  ✓ Gutenberg 코드 에디터 발견")
        except:
            pass
        
        # Classic Editor 시도 (TinyMCE)
        if not code_editor_textarea:
            try:
                # Classic Editor의 HTML 탭 클릭
                html_tab = driver.find_element(By.ID, "content-html")
                html_tab.click()
                time.sleep(1)
                code_editor_textarea = driver.find_element(By.ID, "content")
                print("  ✓ Classic Editor HTML 모드 발견")
            except:
                pass
        
        if not code_editor_textarea:
            raise Exception("코드 에디터를 찾을 수 없습니다.")
        
        # 3. 코드 주입 (Replace existing content)
        wp_base_url = WP_ADMIN_URL.replace("/wp-admin/", "")
        final_block_code = HOMEPAGE_BLOCK_HTML.replace("[WP_URL]", wp_base_url.rstrip('/'))

        # JavaScript로 직접 값 설정 (이모지 문제 해결)
        driver.execute_script("arguments[0].value = arguments[1];", code_editor_textarea, final_block_code)
        
        time.sleep(3) # 저장 전 대기
        
    except Exception as e:
        print(f"  ❌ 코드 에디터 주입 실패: {e}")
        return

    # 4. 페이지 발행 (Publish)
    try:
        print("  🚀 페이지 발행 중...")
        
        # Classic Editor 발행 버튼 시도
        publish_button = None
        try:
            publish_button = driver.find_element(By.ID, "publish")
            print("  ✓ Classic Editor 발행 버튼 발견")
        except:
            pass
        
        # Gutenberg 발행 버튼 시도
        if not publish_button:
            try:
                publish_button = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, ".editor-post-publish-button"))
                )
                print("  ✓ Gutenberg 발행 버튼 발견")
            except:
                pass
        
        if publish_button:
            # JavaScript로 직접 클릭 (가려진 요소 문제 해결)
            driver.execute_script("arguments[0].click();", publish_button)
            time.sleep(3) 
            
            # Gutenberg의 경우 최종 확인 버튼 클릭
            try:
                confirm_publish = driver.find_element(By.CSS_SELECTOR, ".editor-post-publish-button__button")
                confirm_publish.click()
                time.sleep(2)
            except:
                pass
            
            print("  ✅ 홈 페이지 디자인 및 발행 완료! 웹사이트에서 확인하세요.")
        else:
            print("  ⚠️ 발행 버튼을 찾을 수 없습니다. 수동으로 발행해주세요.")
        
    except Exception as e:
        print(f"  ❌ 발행 실패: {e}")


# ---------------------------------------------------------
# ✅ Step 3: Main Execution
# ---------------------------------------------------------

def main():
    driver = setup_driver()
    if not wp_login(driver):
        print("❌ 로그인 실패. 사용자명/비밀번호를 확인하세요.")
        return

    # 1. 홈 페이지 빌드
    inject_homepage_cards(driver)

    driver.quit()

if __name__ == "__main__":
    main()