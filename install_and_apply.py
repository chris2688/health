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

FOOTER_CODE = """<!-- 9988 건강 연구소 메인 화면 -->
<script>
jQuery(document).ready(function($) {
    if ($('body').hasClass('home') || $('body').hasClass('blog')) {
        var mainHTML = `
<style>
body.home .site-main,
body.blog .site-main {
    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%) !important;
    padding: 60px 20px !important;
    min-height: 80vh !important;
}
body.home .site-main > *:not(.health-main-wrapper),
body.blog .site-main > *:not(.health-main-wrapper) {
    display: none !important;
}
.health-main-wrapper {
    max-width: 1400px;
    margin: 0 auto;
}
.health-main-title {
    text-align: center;
    margin-bottom: 50px;
}
.health-main-subtitle {
    font-size: 16px;
    font-weight: 600;
    color: #4A90E2;
    text-transform: uppercase;
    letter-spacing: 2px;
    margin-bottom: 10px;
}
.health-main-heading {
    font-size: 42px;
    font-weight: 800;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0;
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
.health-main-card-icon {
    font-size: 48px;
    margin-bottom: 20px;
    filter: drop-shadow(0 2px 4px rgba(0,0,0,0.2));
    position: relative;
    z-index: 1;
}
.health-main-card h3 {
    font-size: 24px;
    font-weight: 700;
    color: #ffffff;
    margin: 0 0 12px 0;
    text-shadow: 0 2px 4px rgba(0,0,0,0.1);
    position: relative;
    z-index: 1;
}
.health-main-card p {
    font-size: 15px;
    color: rgba(255,255,255,0.9);
    margin: 0;
    line-height: 1.6;
    position: relative;
    z-index: 1;
}
@media (max-width: 768px) {
    .health-main-grid {
        grid-template-columns: 1fr;
        gap: 20px;
    }
    .health-main-heading {
        font-size: 32px;
    }
}
</style>
<div class="health-main-wrapper">
    <div class="health-main-title">
        <p class="health-main-subtitle">9988 건강 연구소 핵심 가이드</p>
        <h2 class="health-main-heading">중년 건강의 모든 것, 분야별로 찾아보세요</h2>
    </div>
    <div class="health-main-grid">
        <a href="https://health9988234.mycafe24.com/category/질환별-정보/심혈관-질환/" class="health-main-card" style="--card-color-1:#FF6B6B; --card-color-2:#EE5A6F;">
            <div class="health-main-card-icon">❤️</div>
            <h3>심혈관 질환</h3>
            <p>고혈압, 심근경색, 동맥경화</p>
        </a>
        <a href="https://health9988234.mycafe24.com/category/질환별-정보/당뇨병/" class="health-main-card" style="--card-color-1:#4ECDC4; --card-color-2:#44A08D;">
            <div class="health-main-card-icon">💉</div>
            <h3>당뇨병</h3>
            <p>혈당관리, 공복혈당, 합병증</p>
        </a>
        <a href="https://health9988234.mycafe24.com/category/질환별-정보/관절-근골격계-질환/" class="health-main-card" style="--card-color-1:#A18CD1; --card-color-2:#FBC2EB;">
            <div class="health-main-card-icon">🦴</div>
            <h3>관절/근골격계 질환</h3>
            <p>관절염, 허리디스크, 골다공증</p>
        </a>
        <a href="https://health9988234.mycafe24.com/category/질환별-정보/호르몬-내분비-질환/" class="health-main-card" style="--card-color-1:#FA709A; --card-color-2:#FEE140;">
            <div class="health-main-card-icon">🌡️</div>
            <h3>호르몬/내분비 질환</h3>
            <p>갱년기, 갑상선, 대사증후군</p>
        </a>
        <a href="https://health9988234.mycafe24.com/category/질환별-정보/정신-건강-신경계/" class="health-main-card" style="--card-color-1:#667eea; --card-color-2:#764ba2;">
            <div class="health-main-card-icon">🧠</div>
            <h3>정신 건강/신경계</h3>
            <p>우울증, 치매, 수면장애</p>
        </a>
        <a href="https://health9988234.mycafe24.com/category/질환별-정보/소화기-질환/" class="health-main-card" style="--card-color-1:#f093fb; --card-color-2:#f5576c;">
            <div class="health-main-card-icon">🍽️</div>
            <h3>소화기 질환</h3>
            <p>위염, 지방간, 역류성 식도염</p>
        </a>
        <a href="https://health9988234.mycafe24.com/category/질환별-정보/안과-치과-기타/" class="health-main-card" style="--card-color-1:#4facfe; --card-color-2:#00f2fe;">
            <div class="health-main-card-icon">👁️</div>
            <h3>안과/치과/기타</h3>
            <p>백내장, 녹내장, 치주질환</p>
        </a>
    </div>
</div>
        `;
        $('.site-main').prepend(mainHTML);
    }
});
</script>"""


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


def install_plugin(driver):
    """Insert Headers and Footers 플러그인 설치 시도"""
    print("🔌 플러그인 설치 확인 중...\n")
    
    try:
        driver.get(f"{WP_ADMIN_URL}plugins.php")
        time.sleep(2)
        
        # 플러그인이 이미 설치되어 있는지 확인
        page_source = driver.page_source
        
        if "Insert Headers and Footers" in page_source or "insert-headers-and-footers" in page_source:
            print("  ✓ 플러그인이 이미 설치되어 있습니다\n")
            
            # 활성화 확인
            if "활성화" in page_source or "Activate" in page_source:
                # 활성화 버튼 찾아서 클릭
                try:
                    activate_link = driver.find_element(By.XPATH, "//tr[contains(@data-slug, 'insert-headers-and-footers')]//a[contains(@href, 'action=activate')]")
                    driver.execute_script("arguments[0].click();", activate_link)
                    time.sleep(2)
                    print("  ✓ 플러그인 활성화 완료\n")
                except:
                    pass
            
            return True
        
        print("  ℹ️ 플러그인 설치 중...\n")
        
        # 플러그인 설치 페이지로 이동
        driver.get(f"{WP_ADMIN_URL}plugin-install.php?s=Insert+Headers+and+Footers&tab=search&type=term")
        time.sleep(3)
        
        # 설치 버튼 찾기
        try:
            install_btn = driver.find_element(By.XPATH, "//a[contains(@data-slug, 'insert-headers-and-footers') and contains(@class, 'install-now')]")
            driver.execute_script("arguments[0].click();", install_btn)
            time.sleep(5)
            print("  ✓ 플러그인 설치 완료\n")
            
            # 활성화 버튼 클릭
            try:
                activate_btn = driver.find_element(By.XPATH, "//a[contains(@data-slug, 'insert-headers-and-footers') and contains(@class, 'activate-now')]")
                driver.execute_script("arguments[0].click();", activate_btn)
                time.sleep(2)
                print("  ✓ 플러그인 활성화 완료\n")
            except:
                print("  ⚠️ 자동 활성화 실패, 수동으로 활성화해주세요\n")
            
            return True
        except:
            print("  ⚠️ 자동 설치 실패\n")
            return False
            
    except Exception as e:
        print(f"  ❌ 플러그인 설치 중 오류: {e}\n")
        return False


def add_footer_code(driver):
    """Insert Headers and Footers 플러그인에 코드 추가"""
    print("📝 Footer 코드 추가 중...\n")
    
    try:
        driver.get(f"{WP_ADMIN_URL}options-general.php?page=ihaf_settings")
        time.sleep(3)
        
        # Footer 섹션 textarea 찾기
        try:
            footer_textarea = driver.find_element(By.ID, "ihaf_insert_footer")
            
            # 기존 내용 확인
            current_content = driver.execute_script("return arguments[0].value;", footer_textarea)
            
            if "9988 건강 연구소" in current_content:
                print("  ℹ️ 코드가 이미 추가되어 있습니다\n")
                return True
            
            # 코드 추가
            new_content = current_content + "\n\n" + FOOTER_CODE
            driver.execute_script("arguments[0].value = arguments[1];", footer_textarea, new_content)
            time.sleep(1)
            print("  ✓ 코드 입력 완료")
            
            # 저장 버튼 클릭
            try:
                save_btn = driver.find_element(By.NAME, "submit")
                driver.execute_script("arguments[0].click();", save_btn)
                time.sleep(2)
                print("  ✅ 설정 저장 완료!\n")
                return True
            except:
                print("  ⚠️ 저장 버튼을 찾을 수 없습니다\n")
                return False
                
        except Exception as e:
            print(f"  ❌ Footer textarea를 찾을 수 없습니다: {e}\n")
            return False
            
    except Exception as e:
        print(f"  ❌ 플러그인 설정 페이지 접근 실패: {e}\n")
        return False


def main():
    print("\n" + "="*60)
    print("🎨 워드프레스 메인 화면 자동 설정")
    print("="*60 + "\n")
    
    driver = setup_driver()
    
    try:
        if not wp_login(driver):
            print("❌ 로그인 실패")
            return
        
        # 플러그인 설치
        plugin_installed = install_plugin(driver)
        
        if plugin_installed:
            # Footer 코드 추가
            if add_footer_code(driver):
                print("="*60)
                print("✨ 완료!")
                print("="*60)
                print(f"\n🌐 사이트 확인: {WP_BASE_URL}")
                print("\n💡 메인 화면에 7개의 카테고리 카드가 표시됩니다!")
                print("   Ctrl+F5로 새로고침하세요.\n")
            else:
                print("\n⚠️ 코드 추가 실패")
                print(f"수동으로 추가하려면 '메인화면_코드.txt' 파일을 참조하세요.\n")
        else:
            print("\n⚠️ 플러그인 설치 실패")
            print(f"수동으로 추가하려면 '메인화면_코드.txt' 파일을 참조하세요.\n")
        
    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
    finally:
        time.sleep(3)
        driver.quit()


if __name__ == "__main__":
    main()

