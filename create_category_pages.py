import sys
import io
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException

WP_LOGIN_URL = "https://health9988234.mycafe24.com/wp-login.php"
WP_ADMIN_URL = "https://health9988234.mycafe24.com/wp-admin/"
WP_USER = "health9988234"
WP_PASSWORD = "ssurlf7904!"
WP_BASE_URL = "https://health9988234.mycafe24.com"

# 카테고리 페이지 데이터
CATEGORY_PAGES = {
    "심혈관-질환": {
        "title": "심혈관 질환",
        "icon": "❤️",
        "color1": "#FF6B6B",
        "color2": "#EE5A6F",
        "subcategories": [
            {"name": "— 심혈관 질환", "icon": "🫀", "slug": "심혈관-질환"}
        ]
    },
    "당뇨병": {
        "title": "당뇨병",
        "icon": "💉",
        "color1": "#4ECDC4",
        "color2": "#44A08D",
        "subcategories": [
            {"name": "— 당뇨병", "icon": "💉", "slug": "당뇨병"}
        ]
    },
    "관절-근골격계": {
        "title": "관절/근골격계 질환",
        "icon": "🦴",
        "color1": "#A18CD1",
        "color2": "#FBC2EB",
        "subcategories": [
            {"name": "— 관절/근골격계 질환", "icon": "🦴", "slug": "관절-근골격계-질환"}
        ]
    },
    "호르몬-내분비": {
        "title": "호르몬/내분비 질환",
        "icon": "🌡️",
        "color1": "#FA709A",
        "color2": "#FEE140",
        "subcategories": [
            {"name": "— 호르몬/내분비 질환", "icon": "🌡️", "slug": "호르몬-내분비-질환"}
        ]
    },
    "정신-건강": {
        "title": "정신 건강/신경계",
        "icon": "🧠",
        "color1": "#667eea",
        "color2": "#764ba2",
        "subcategories": [
            {"name": "— 정신 건강/신경계", "icon": "🧠", "slug": "정신-건강-신경계"}
        ]
    },
    "소화기-질환": {
        "title": "소화기 질환",
        "icon": "🍽️",
        "color1": "#f093fb",
        "color2": "#f5576c",
        "subcategories": [
            {"name": "— 소화기 질환", "icon": "🍽️", "slug": "소화기-질환"}
        ]
    },
    "안과-치과": {
        "title": "안과/치과/기타",
        "icon": "👁️",
        "color1": "#4facfe",
        "color2": "#00f2fe",
        "subcategories": [
            {"name": "— 안과/치과/기타", "icon": "👁️", "slug": "안과-치과-기타"}
        ]
    }
}


def generate_page_html(page_slug, page_data):
    subcategory_cards = ""
    for sub in page_data["subcategories"]:
        subcategory_cards += f"""
        <div class="health-card" style="--card-color-1:{page_data['color1']}; --card-color-2:{page_data['color2']};">
            <div class="health-card-icon">{sub['icon']}</div>
            <h3>{sub['name'].replace('— ', '')}</h3>
            <p>관련 글 보기 →</p>
            <a href="{WP_BASE_URL}/category/{sub['slug']}" aria-label="{sub['name']}"></a>
        </div>
        """
    
    html = f"""
<style>
/* 페이지 제목 숨기기 */
.entry-title {{
    display: none !important;
}}
.health-card-container {{
    padding: 60px 20px;
    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    min-height: 60vh;
}}
.health-cards-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 30px;
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
}}
.health-card {{
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
    align-items: center;
    text-align: center;
}}
.health-card:hover {{
    transform: translateY(-8px) scale(1.02);
    box-shadow: 0 20px 40px rgba(0,0,0,0.25);
}}
.health-card::before {{
    content: '';
    position: absolute;
    top: 0;
    right: 0;
    width: 150px;
    height: 150px;
    background: rgba(255,255,255,0.1);
    border-radius: 50%;
    transform: translate(50%, -50%);
}}
.health-card-icon {{
    font-size: 64px;
    margin-bottom: 20px;
    filter: drop-shadow(0 2px 4px rgba(0,0,0,0.2));
}}
.health-card h3 {{
    font-size: 26px;
    font-weight: 700;
    color: #ffffff;
    margin: 0 0 12px 0;
    text-shadow: 0 2px 4px rgba(0,0,0,0.1);
    position: relative;
    z-index: 1;
}}
.health-card p {{
    font-size: 16px;
    color: rgba(255,255,255,0.9);
    margin: 0;
    font-weight: 500;
}}
.health-card a {{
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: 10;
}}
.section-title {{
    text-align: center;
    margin-bottom: 30px;
}}
.section-title .back-link {{
    display: inline-block;
    margin-bottom: 25px;
    padding: 12px 28px;
    background: rgba(255,255,255,0.95);
    border-radius: 50px;
    text-decoration: none;
    color: #667eea;
    font-weight: 600;
    font-size: 15px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    transition: all 0.3s;
}}
.section-title .back-link:hover {{
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(0,0,0,0.15);
    background: #ffffff;
}}
.section-title h2 {{
    font-size: 42px;
    font-weight: 800;
    background: linear-gradient(135deg, {page_data['color1']} 0%, {page_data['color2']} 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0 0 15px 0;
}}
.section-title .main-icon {{
    font-size: 72px;
    margin-bottom: 15px;
    filter: drop-shadow(0 4px 8px rgba(0,0,0,0.1));
}}
.section-title .subtitle {{
    font-size: 18px;
    color: #666;
    font-weight: 500;
}}
@media (max-width: 768px) {{
    .health-cards-grid {{
        grid-template-columns: 1fr;
        gap: 20px;
    }}
    .section-title h2 {{
        font-size: 32px;
    }}
    .section-title .main-icon {{
        font-size: 56px;
    }}
}}
</style>

<div class="health-card-container">
    <div class="section-title">
        <a href="{WP_BASE_URL}" class="back-link">← 홈으로 돌아가기</a>
        <div class="main-icon">{page_data['icon']}</div>
        <h2>{page_data['title']}</h2>
        <p class="subtitle">건강 정보를 확인하세요</p>
    </div>
    
    <div class="health-cards-grid">
        {subcategory_cards}
    </div>
</div>
"""
    return html


def setup_driver():
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    return driver


def wp_login(driver):
    print(f"🔐 WordPress 로그인 시도...")
    driver.get(WP_LOGIN_URL)
    time.sleep(2)
    
    user_field = driver.find_element(By.ID, "user_login")
    pass_field = driver.find_element(By.ID, "user_pass")
    user_field.send_keys(WP_USER)
    pass_field.send_keys(WP_PASSWORD)
    
    login_btn = driver.find_element(By.ID, "wp-submit")
    login_btn.click()
    time.sleep(3)
    
    return "wp-admin" in driver.current_url


def create_page(driver, page_slug, page_data):
    print(f"\n--- 📄 '{page_data['title']}' 페이지 생성 중 ---")
    
    try:
        # 새 페이지 생성 화면으로 이동
        driver.get(f"{WP_ADMIN_URL}post-new.php?post_type=page")
        time.sleep(10)
        print("  ⏳ 페이지 편집기 로딩 중...")
        
        # 제목 입력
        try:
            title_field = driver.find_element(By.ID, "title")
            title_field.send_keys(page_data['title'])
            print(f"  ✓ 제목 입력 완료")
        except:
            print("  ⚠️ Classic Editor 제목 필드 시도...")
        
        # HTML 모드로 전환
        try:
            html_tab = driver.find_element(By.ID, "content-html")
            html_tab.click()
            time.sleep(1)
            content_field = driver.find_element(By.ID, "content")
            print("  ✓ Classic Editor HTML 모드 발견")
        except:
            print("  ❌ HTML 모드로 전환 실패")
            return False
        
        # HTML 콘텐츠 주입
        html_content = generate_page_html(page_slug, page_data)
        driver.execute_script("arguments[0].value = arguments[1];", content_field, html_content)
        print("  ✓ HTML 콘텐츠 주입 완료")
        time.sleep(2)
        
        # 발행
        try:
            publish_button = driver.find_element(By.ID, "publish")
            driver.execute_script("arguments[0].click();", publish_button)
            time.sleep(3)
            print(f"  ✅ '{page_data['title']}' 페이지 생성 완료!")
            return True
        except Exception as e:
            print(f"  ❌ 발행 실패: {e}")
            return False
            
    except Exception as e:
        print(f"  ❌ 오류 발생: {e}")
        return False


def main():
    driver = setup_driver()
    
    if not wp_login(driver):
        print("❌ 로그인 실패")
        driver.quit()
        return
    
    print("✓ 로그인 성공\n")
    
    success_count = 0
    for page_slug, page_data in CATEGORY_PAGES.items():
        if create_page(driver, page_slug, page_data):
            success_count += 1
        time.sleep(3)
    
    print(f"\n✨ 완료! {success_count}/{len(CATEGORY_PAGES)}개 카테고리 페이지 생성됨")
    print(f"\n⚠️ 이제 홈페이지의 카드 링크를 새 페이지로 업데이트해야 합니다.")
    driver.quit()


if __name__ == "__main__":
    main()

