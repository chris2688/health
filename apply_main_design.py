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

# 워드프레스 footer.php에 추가할 코드 (메인 화면 카드 표시)
FOOTER_INJECTION_CODE = """
<!-- 9988 건강 연구소 메인 화면 카드 -->
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
        <a href="${WP_BASE_URL}/category/질환별-정보/심혈관-질환/" class="health-main-card" style="--card-color-1:#FF6B6B; --card-color-2:#EE5A6F;">
            <div class="health-main-card-icon">❤️</div>
            <h3>심혈관 질환</h3>
            <p>고혈압, 심근경색, 동맥경화</p>
        </a>
        
        <a href="${WP_BASE_URL}/category/질환별-정보/당뇨병/" class="health-main-card" style="--card-color-1:#4ECDC4; --card-color-2:#44A08D;">
            <div class="health-main-card-icon">💉</div>
            <h3>당뇨병</h3>
            <p>혈당관리, 공복혈당, 합병증</p>
        </a>
        
        <a href="${WP_BASE_URL}/category/질환별-정보/관절-근골격계-질환/" class="health-main-card" style="--card-color-1:#A18CD1; --card-color-2:#FBC2EB;">
            <div class="health-main-card-icon">🦴</div>
            <h3>관절/근골격계 질환</h3>
            <p>관절염, 허리디스크, 골다공증</p>
        </a>
        
        <a href="${WP_BASE_URL}/category/질환별-정보/호르몬-내분비-질환/" class="health-main-card" style="--card-color-1:#FA709A; --card-color-2:#FEE140;">
            <div class="health-main-card-icon">🌡️</div>
            <h3>호르몬/내분비 질환</h3>
            <p>갱년기, 갑상선, 대사증후군</p>
        </a>
        
        <a href="${WP_BASE_URL}/category/질환별-정보/정신-건강-신경계/" class="health-main-card" style="--card-color-1:#667eea; --card-color-2:#764ba2;">
            <div class="health-main-card-icon">🧠</div>
            <h3>정신 건강/신경계</h3>
            <p>우울증, 치매, 수면장애</p>
        </a>
        
        <a href="${WP_BASE_URL}/category/질환별-정보/소화기-질환/" class="health-main-card" style="--card-color-1:#f093fb; --card-color-2:#f5576c;">
            <div class="health-main-card-icon">🍽️</div>
            <h3>소화기 질환</h3>
            <p>위염, 지방간, 역류성 식도염</p>
        </a>
        
        <a href="${WP_BASE_URL}/category/질환별-정보/안과-치과-기타/" class="health-main-card" style="--card-color-1:#4facfe; --card-color-2:#00f2fe;">
            <div class="health-main-card-icon">👁️</div>
            <h3>안과/치과/기타</h3>
            <p>백내장, 녹내장, 치주질환</p>
        </a>
    </div>
</div>
        `;
        
        mainHTML = mainHTML.replace(/\$\{WP_BASE_URL\}/g, '<?php echo home_url(); ?>');
        $('.site-main').prepend(mainHTML);
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


def inject_footer_code(driver):
    """테마의 footer.php에 코드 주입"""
    print("📝 테마 footer.php 수정 중...\n")
    
    try:
        # 테마 편집기로 이동
        driver.get(f"{WP_ADMIN_URL}theme-editor.php?file=footer.php")
        time.sleep(3)
        
        # 코드 편집기 찾기
        try:
            # 여러 가능한 편집기 ID 시도
            editor = None
            for editor_id in ["newcontent", "content"]:
                try:
                    editor = driver.find_element(By.ID, editor_id)
                    break
                except:
                    continue
            
            if not editor:
                print("  ❌ 편집기를 찾을 수 없습니다")
                return False
            
            current_content = driver.execute_script("return arguments[0].value;", editor)
            
            # 이미 코드가 있는지 확인
            if "9988 건강 연구소 메인 화면" in current_content:
                print("  ℹ️ 메인 화면 코드가 이미 추가되어 있습니다")
                return True
            
            # </body> 태그 바로 위에 코드 삽입
            if "</body>" in current_content:
                new_content = current_content.replace("</body>", FOOTER_INJECTION_CODE + "\n</body>")
            else:
                # </body> 태그가 없으면 맨 끝에 추가
                new_content = current_content + "\n" + FOOTER_INJECTION_CODE
            
            driver.execute_script("arguments[0].value = arguments[1];", editor, new_content)
            print("  ✓ 코드 추가 완료")
            time.sleep(1)
            
            # 저장 버튼 클릭
            try:
                save_btn = driver.find_element(By.ID, "submit")
                driver.execute_script("arguments[0].click();", save_btn)
                time.sleep(2)
                print("  ✅ footer.php 저장 완료!\n")
                return True
            except Exception as e:
                print(f"  ⚠️ 저장 버튼 클릭 실패: {e}")
                return False
                
        except Exception as e:
            print(f"  ❌ 편집기 접근 실패: {e}")
            return False
            
    except Exception as e:
        print(f"  ❌ 테마 편집기 접근 실패: {e}")
        print(f"     오류 상세: {str(e)}")
        return False


def main():
    print("\n" + "="*60)
    print("🎨 워드프레스 메인 화면 디자인 적용")
    print("="*60 + "\n")
    
    driver = setup_driver()
    
    try:
        if not wp_login(driver):
            print("❌ 로그인 실패")
            return
        
        if inject_footer_code(driver):
            print("="*60)
            print("✨ 완료!")
            print("="*60)
            print(f"\n🌐 사이트 확인: {WP_BASE_URL}")
            print("\n💡 메인 화면에 7개의 카테고리 카드가 index.html처럼 표시됩니다!")
            print("   Ctrl+F5로 새로고침하세요.\n")
        else:
            print("\n❌ 자동 적용 실패")
            print("\n💡 수동 적용 방법:")
            print("   1. WordPress 관리자 > 외모 > 테마 편집기")
            print("   2. footer.php 파일 선택")
            print("   3. </body> 태그 바로 위에 다음 코드 붙여넣기:")
            print("      (homepage_code.html 파일 참조)\n")
        
    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
    finally:
        time.sleep(3)
        driver.quit()


if __name__ == "__main__":
    main()

