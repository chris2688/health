import sys
import io
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
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
# 🎨 메인 카테고리 페이지 HTML (질환별 정보 카테고리)
# ---------------------------------------------------------
MAIN_CATEGORY_HTML = """
<style>
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

/* 페이지 제목과 카테고리 설명 숨기기 */
.entry-title, .page-title, .category-description, .taxonomy-description {
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


def update_main_category(driver):
    """질환별 정보 카테고리를 메인 화면으로 설정"""
    print("📂 '질환별 정보' 카테고리 업데이트 중...\n")
    
    try:
        # 카테고리 목록으로 이동
        driver.get(f"{WP_ADMIN_URL}edit-tags.php?taxonomy=category")
        time.sleep(2)
        
        # "질환별 정보" 카테고리 찾기
        try:
            category_link = driver.find_element(By.XPATH, "//a[contains(@class, 'row-title') and contains(text(), '질환별 정보')]")
            edit_url = category_link.get_attribute('href')
            driver.get(edit_url)
            time.sleep(2)
            print("  ✓ '질환별 정보' 카테고리 편집 페이지 접근")
        except:
            print("  ❌ '질환별 정보' 카테고리를 찾을 수 없습니다")
            return False
        
        # Description 필드에 HTML 주입
        try:
            description_field = driver.find_element(By.ID, "description")
            driver.execute_script("arguments[0].value = arguments[1];", description_field, MAIN_CATEGORY_HTML)
            print("  ✓ HTML 콘텐츠 주입 완료")
            time.sleep(1)
        except Exception as e:
            print(f"  ❌ Description 필드를 찾을 수 없습니다: {e}")
            return False
        
        # 업데이트 버튼 클릭
        try:
            try:
                update_button = driver.find_element(By.ID, "submit")
                driver.execute_script("arguments[0].click();", update_button)
            except:
                try:
                    update_button = driver.find_element(By.CSS_SELECTOR, "input[type='submit'].button-primary")
                    driver.execute_script("arguments[0].click();", update_button)
                except:
                    form = driver.find_element(By.ID, "edittag")
                    driver.execute_script("arguments[0].submit();", form)
            
            time.sleep(2)
            print("  ✅ '질환별 정보' 카테고리 업데이트 완료!")
            return True
        except Exception as e:
            print(f"  ❌ 업데이트 실패: {e}")
            return False
            
    except Exception as e:
        print(f"  ❌ 오류 발생: {e}")
        return False


def set_category_as_homepage(driver):
    """카테고리를 홈페이지로 설정"""
    print("\n⚙️ 홈페이지 설정 업데이트 중...\n")
    
    try:
        driver.get(f"{WP_ADMIN_URL}options-reading.php")
        time.sleep(2)
        
        # "Your latest posts" 라디오 버튼 선택 (카테고리 아카이브가 기본 홈으로)
        try:
            posts_radio = driver.find_element(By.ID, "show_on_front_posts")
            driver.execute_script("arguments[0].click();", posts_radio)
            time.sleep(1)
            print("  ✓ 홈페이지 표시 설정 변경")
        except Exception as e:
            print(f"  ⚠️ 홈페이지 설정 변경 실패: {e}")
        
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
        print(f"  ❌ 오류 발생: {e}")
        return False


def main():
    """메인 실행"""
    print("\n" + "="*60)
    print("🎨 워드프레스 메인 화면 설정")
    print("="*60 + "\n")
    
    driver = setup_driver()
    
    try:
        if not wp_login(driver):
            print("❌ 로그인 실패. 사용자명/비밀번호를 확인하세요.")
            return
        
        if update_main_category(driver):
            print("\n" + "="*60)
            print("✨ 완료!")
            print("="*60)
            print(f"\n🌐 사이트 확인: {WP_BASE_URL}/category/질환별-정보/")
            print("\n💡 팁:")
            print("   - '질환별 정보' 카테고리가 메인 화면 역할을 합니다")
            print("   - 7개의 카테고리 카드가 표시됩니다")
            print("   - 각 카드를 클릭하면 서브카테고리로 이동합니다\n")
        
    finally:
        time.sleep(3)
        driver.quit()


if __name__ == "__main__":
    main()

