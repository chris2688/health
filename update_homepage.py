import sys
import io
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

# UTF-8 인코딩 설정 (Windows 콘솔 지원)
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
# 🎨 홈페이지 HTML 블록
# ---------------------------------------------------------
HOMEPAGE_HTML = """
<style>
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

/* 페이지 제목 숨기기 */
.entry-title, .page-title {
    display: none !important;
}

.health-card-container {
    padding: 60px 20px;
    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    min-height: 80vh;
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
        <a href="{base_url}/category/질환별-정보/심혈관-질환/" class="health-card" style="--card-color-1:#FF6B6B; --card-color-2:#EE5A6F;">
            <div class="health-card-icon">❤️</div>
            <h3>심혈관 질환</h3>
            <p>고혈압, 심근경색, 동맥경화</p>
        </a>
        
        <a href="{base_url}/category/질환별-정보/당뇨병/" class="health-card" style="--card-color-1:#4ECDC4; --card-color-2:#44A08D;">
            <div class="health-card-icon">💉</div>
            <h3>당뇨병</h3>
            <p>혈당관리, 공복혈당, 합병증</p>
        </a>
        
        <a href="{base_url}/category/질환별-정보/관절-근골격계-질환/" class="health-card" style="--card-color-1:#A18CD1; --card-color-2:#FBC2EB;">
            <div class="health-card-icon">🦴</div>
            <h3>관절/근골격계 질환</h3>
            <p>관절염, 허리디스크, 골다공증</p>
        </a>
        
        <a href="{base_url}/category/질환별-정보/호르몬-내분비-질환/" class="health-card" style="--card-color-1:#FA709A; --card-color-2:#FEE140;">
            <div class="health-card-icon">🌡️</div>
            <h3>호르몬/내분비 질환</h3>
            <p>갱년기, 갑상선, 대사증후군</p>
        </a>
        
        <a href="{base_url}/category/질환별-정보/정신-건강-신경계/" class="health-card" style="--card-color-1:#667eea; --card-color-2:#764ba2;">
            <div class="health-card-icon">🧠</div>
            <h3>정신 건강/신경계</h3>
            <p>우울증, 치매, 수면장애</p>
        </a>
        
        <a href="{base_url}/category/질환별-정보/소화기-질환/" class="health-card" style="--card-color-1:#f093fb; --card-color-2:#f5576c;">
            <div class="health-card-icon">🍽️</div>
            <h3>소화기 질환</h3>
            <p>위염, 지방간, 역류성 식도염</p>
        </a>
        
        <a href="{base_url}/category/질환별-정보/안과-치과-기타/" class="health-card" style="--card-color-1:#4facfe; --card-color-2:#00f2fe;">
            <div class="health-card-icon">👁️</div>
            <h3>안과/치과/기타</h3>
            <p>백내장, 녹내장, 치주질환</p>
        </a>
    </div>
</div>
""".replace("{base_url}", WP_BASE_URL)


def setup_driver():
    """브라우저 드라이버 설정"""
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


def create_homepage(driver):
    """홈페이지 생성 또는 업데이트"""
    print("🏠 홈페이지 설정 중...\n")
    
    try:
        # 페이지 목록으로 이동
        driver.get(f"{WP_ADMIN_URL}edit.php?post_type=page")
        time.sleep(2)
        
        # "홈" 페이지가 있는지 확인
        try:
            home_page_link = driver.find_element(By.XPATH, "//a[contains(@class, 'row-title') and contains(text(), '홈')]")
            edit_url = home_page_link.get_attribute('href')
            driver.get(edit_url)
            time.sleep(2)
            print("  ✓ 기존 '홈' 페이지 발견, 편집 모드로 진입")
        except:
            print("  ℹ️ '홈' 페이지가 없습니다. 새로 생성합니다...")
            driver.get(f"{WP_ADMIN_URL}post-new.php?post_type=page")
            time.sleep(2)
            
            # 페이지 제목 입력
            try:
                title_field = driver.find_element(By.CSS_SELECTOR, ".editor-post-title__input, #post-title-0")
                title_field.clear()
                title_field.send_keys("홈")
                time.sleep(1)
                print("  ✓ 페이지 제목 입력 완료")
            except Exception as e:
                print(f"  ⚠️ 제목 입력 실패 (계속 진행): {e}")
        
        # 블록 에디터에서 HTML 블록 추가
        try:
            # + 버튼 클릭하여 블록 추가
            try:
                add_block_btn = driver.find_element(By.CSS_SELECTOR, ".block-editor-inserter__toggle")
                driver.execute_script("arguments[0].click();", add_block_btn)
                time.sleep(1)
            except:
                pass
            
            # HTML 블록 검색
            try:
                search_box = driver.find_element(By.CSS_SELECTOR, ".block-editor-inserter__search-input")
                search_box.send_keys("HTML")
                time.sleep(1)
                
                # HTML 블록 선택
                html_block = driver.find_element(By.XPATH, "//button[contains(@class, 'block-editor-block-types-list__item') and .//span[contains(text(), 'Custom HTML')]]")
                driver.execute_script("arguments[0].click();", html_block)
                time.sleep(1)
                print("  ✓ HTML 블록 추가 완료")
            except:
                print("  ⚠️ 블록 검색 방식 실패, 직접 HTML 편집기 전환 시도")
        except Exception as e:
            print(f"  ⚠️ 블록 추가 중 오류 (계속 진행): {e}")
        
        # HTML 에디터로 전환 (코드 편집기)
        try:
            # 더보기 메뉴 클릭
            more_menu = driver.find_element(By.CSS_SELECTOR, "button[aria-label='더 보기']")
            driver.execute_script("arguments[0].click();", more_menu)
            time.sleep(1)
            
            # 코드 편집기 버튼 클릭
            code_editor = driver.find_element(By.XPATH, "//button[contains(., '코드 편집기') or contains(., 'Code editor')]")
            driver.execute_script("arguments[0].click();", code_editor)
            time.sleep(1)
            print("  ✓ 코드 편집기 모드 전환")
            
            # HTML 입력
            editor = driver.find_element(By.CSS_SELECTOR, ".editor-post-text-editor")
            driver.execute_script("arguments[0].value = arguments[1];", editor, HOMEPAGE_HTML)
            time.sleep(1)
            print("  ✓ HTML 콘텐츠 주입 완료")
        except Exception as e:
            print(f"  ❌ HTML 편집 실패: {e}")
            return False
        
        # 페이지 발행
        try:
            # 발행 버튼 찾기
            try:
                publish_btn = driver.find_element(By.CSS_SELECTOR, ".editor-post-publish-panel__toggle")
                driver.execute_script("arguments[0].click();", publish_btn)
                time.sleep(1)
                
                # 최종 발행 확인 버튼
                final_publish = driver.find_element(By.CSS_SELECTOR, ".editor-post-publish-button")
                driver.execute_script("arguments[0].click();", final_publish)
            except:
                # 업데이트 버튼 (기존 페이지 수정 시)
                update_btn = driver.find_element(By.CSS_SELECTOR, ".editor-post-publish-button__button")
                driver.execute_script("arguments[0].click();", update_btn)
            
            time.sleep(2)
            print("  ✅ 페이지 발행/업데이트 완료!")
        except Exception as e:
            print(f"  ⚠️ 발행 버튼 클릭 실패 (수동으로 저장해주세요): {e}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ 홈페이지 생성 중 오류: {e}")
        return False


def set_homepage_as_front(driver):
    """홈페이지를 프론트 페이지로 설정"""
    print("\n⚙️ 홈페이지를 프론트 페이지로 설정 중...\n")
    
    try:
        driver.get(f"{WP_ADMIN_URL}options-reading.php")
        time.sleep(2)
        
        # "정적 페이지" 라디오 버튼 선택
        try:
            static_radio = driver.find_element(By.ID, "page_on_front_radio")
            driver.execute_script("arguments[0].click();", static_radio)
            time.sleep(1)
            print("  ✓ 정적 페이지 옵션 선택")
        except:
            print("  ⚠️ 정적 페이지 옵션 선택 실패")
        
        # 프론트 페이지로 "홈" 선택
        try:
            front_page_select = driver.find_element(By.ID, "page_on_front")
            # "홈" 페이지 찾기
            home_option = driver.find_element(By.XPATH, "//select[@id='page_on_front']/option[contains(text(), '홈')]")
            driver.execute_script("arguments[0].selected = true;", home_option)
            time.sleep(1)
            print("  ✓ 프론트 페이지로 '홈' 선택")
        except Exception as e:
            print(f"  ⚠️ 프론트 페이지 선택 실패: {e}")
        
        # 변경사항 저장
        try:
            save_btn = driver.find_element(By.ID, "submit")
            driver.execute_script("arguments[0].click();", save_btn)
            time.sleep(2)
            print("  ✅ 설정 저장 완료!")
        except Exception as e:
            print(f"  ⚠️ 설정 저장 실패: {e}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ 프론트 페이지 설정 중 오류: {e}")
        return False


def main():
    """메인 실행"""
    print("\n" + "="*60)
    print("🎨 워드프레스 홈페이지 자동 생성")
    print("="*60 + "\n")
    
    driver = setup_driver()
    
    try:
        if not wp_login(driver):
            print("❌ 로그인 실패. 사용자명/비밀번호를 확인하세요.")
            return
        
        if create_homepage(driver):
            print("\n" + "="*60)
            set_homepage_as_front(driver)
            
            print("\n" + "="*60)
            print("✨ 모든 작업 완료!")
            print("="*60)
            print(f"\n🌐 사이트 확인: {WP_BASE_URL}")
            print("\n📌 수동 작업이 필요한 경우:")
            print("   1. WordPress 관리자 > 설정 > 읽기")
            print("   2. '홈페이지 표시' > '정적 페이지' 선택")
            print("   3. '홈페이지' 드롭다운에서 '홈' 선택")
            print("   4. '변경사항 저장' 클릭\n")
        
    finally:
        time.sleep(3)
        driver.quit()


if __name__ == "__main__":
    main()

