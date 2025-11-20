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

def update_category_description(driver):
    """질환별-정보 카테고리 설명에 메인 카드 추가"""
    print("\n📝 질환별-정보 카테고리에 메인 카드 추가 중...")
    
    category_html = """
<style>
    /* 카테고리 설명 영역만 표시 */
    .category-description {
        display: block !important;
    }
    .health-card-container {
        padding: 60px 20px;
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        min-height: 60vh;
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
    /* 카테고리 제목 숨기기 */
    .archive-title {
        display: none;
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
            <a href="https://health9988234.mycafe24.com/category/질환별-정보/심혈관-질환/" aria-label="심혈관 질환"></a>
        </div>
        
        <div class="health-card" style="--card-color-1:#4ECDC4; --card-color-2:#44A08D;">
            <div class="health-card-icon">💉</div>
            <h3>당뇨병</h3>
            <p>혈당관리, 공복혈당, 합병증</p>
            <a href="https://health9988234.mycafe24.com/category/질환별-정보/당뇨병/" aria-label="당뇨병"></a>
        </div>
        
        <div class="health-card" style="--card-color-1:#A18CD1; --card-color-2:#FBC2EB;">
            <div class="health-card-icon">🦴</div>
            <h3>관절/근골격계 질환</h3>
            <p>관절염, 허리디스크, 골다공증</p>
            <a href="https://health9988234.mycafe24.com/category/질환별-정보/관절-근골격계-질환/" aria-label="관절/근골격계 질환"></a>
        </div>
        
        <div class="health-card" style="--card-color-1:#FA709A; --card-color-2:#FEE140;">
            <div class="health-card-icon">🌡️</div>
            <h3>호르몬/내분비 질환</h3>
            <p>갱년기, 갑상선, 대사증후군</p>
            <a href="https://health9988234.mycafe24.com/category/질환별-정보/호르몬-내분비-질환/" aria-label="호르몬/내분비 질환"></a>
        </div>
        
        <div class="health-card" style="--card-color-1:#667eea; --card-color-2:#764ba2;">
            <div class="health-card-icon">🧠</div>
            <h3>정신 건강/신경계</h3>
            <p>우울증, 치매, 수면장애</p>
            <a href="https://health9988234.mycafe24.com/category/질환별-정보/정신-건강-신경계/" aria-label="정신 건강/신경계"></a>
        </div>
        
        <div class="health-card" style="--card-color-1:#f093fb; --card-color-2:#f5576c;">
            <div class="health-card-icon">🍽️</div>
            <h3>소화기 질환</h3>
            <p>위염, 지방간, 역류성 식도염</p>
            <a href="https://health9988234.mycafe24.com/category/질환별-정보/소화기-질환/" aria-label="소화기 질환"></a>
        </div>
        
        <div class="health-card" style="--card-color-1:#4facfe; --card-color-2:#00f2fe;">
            <div class="health-card-icon">👁️</div>
            <h3>안과/치과/기타</h3>
            <p>백내장, 녹내장, 치주질환</p>
            <a href="https://health9988234.mycafe24.com/category/질환별-정보/안과-치과-기타/" aria-label="안과/치과/기타"></a>
        </div>
    </div>
</div>
"""
    
    try:
        # 카테고리 편집 페이지로 이동
        driver.get(f"{WP_URL}/wp-admin/edit-tags.php?taxonomy=category")
        time.sleep(2)
        
        # "질환별-정보" 카테고리 찾기
        try:
            category_link = driver.find_element(By.XPATH, "//a[contains(@class, 'row-title') and contains(text(), '질환별-정보')]")
            edit_url = category_link.get_attribute('href')
            driver.get(edit_url)
            time.sleep(2)
            print("  ✓ 질환별-정보 카테고리 편집 페이지 접근")
        except:
            print("  ❌ 질환별-정보 카테고리를 찾을 수 없습니다")
            return False
        
        # Description 필드에 HTML 주입
        try:
            description_field = driver.find_element(By.ID, "description")
            driver.execute_script("arguments[0].value = arguments[1];", description_field, category_html)
            print("  ✓ HTML 콘텐츠 주입 완료")
            time.sleep(1)
        except Exception as e:
            print(f"  ❌ Description 필드를 찾을 수 없습니다: {e}")
            return False
        
        # 업데이트 버튼 클릭
        try:
            update_button = driver.find_element(By.ID, "submit")
            driver.execute_script("arguments[0].click();", update_button)
            time.sleep(2)
            print("  ✅ 카테고리 업데이트 완료!")
            return True
        except Exception as e:
            print(f"  ❌ 업데이트 실패: {e}")
            return False
            
    except Exception as e:
        print(f"  ❌ 오류 발생: {e}")
        return False

def set_category_as_homepage(driver):
    """질환별-정보 카테고리를 홈페이지로 설정"""
    print("\n🏠 질환별-정보 카테고리를 홈페이지로 설정 중...")
    
    try:
        # 설정 > 읽기 페이지로 이동
        driver.get(f"{WP_URL}/wp-admin/options-reading.php")
        time.sleep(3)
        
        # "최신 글" 라디오 버튼 선택 (블로그 모드)
        try:
            blog_radio = driver.find_element(By.CSS_SELECTOR, "input[value='posts']#page_for_posts")
            if not blog_radio.is_selected():
                driver.execute_script("arguments[0].click();", blog_radio)
                time.sleep(1)
                print("  ✓ '최신 글' 옵션 선택")
        except Exception as e:
            print(f"  ℹ️ 기본 설정 유지")
        
        # 변경사항 저장
        try:
            save_button = driver.find_element(By.ID, "submit")
            save_button.click()
            time.sleep(3)
            print("  ✅ 설정 저장 완료!")
            return True
        except Exception as e:
            print(f"  ❌ 저장 실패: {e}")
            return False
            
    except Exception as e:
        print(f"  ❌ 설정 변경 실패: {e}")
        return False

def main():
    print("=" * 60)
    print("🏠 질환별-정보 카테고리를 메인 페이지로 설정")
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
        
        # 카테고리 설명 업데이트
        update_success = update_category_description(driver)
        
        # 설정 변경
        set_success = set_category_as_homepage(driver)
        
        if update_success:
            print("\n" + "=" * 60)
            print("✅ 작업 완료!")
            print("🌐 이제 다음 URL을 홈페이지로 사용하세요:")
            print(f"   {WP_URL}/category/질환별-정보/")
            print("")
            print("💡 또는 WordPress에서:")
            print("   설정 > 읽기 > 홈페이지 표시 > URL 리디렉션 설정")
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

