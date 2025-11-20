import sys
import io
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

# ---------------------------------------------------------
# ✅ 설정 변수
# ---------------------------------------------------------
WP_LOGIN_URL = "https://health9988234.mycafe24.com/wp-login.php"
WP_ADMIN_URL = "https://health9988234.mycafe24.com/wp-admin/"
WP_USER = "health9988234"
WP_PASSWORD = "ssurlf7904!"
WP_BASE_URL = "https://health9988234.mycafe24.com"

# ---------------------------------------------------------
# 📂 카테고리 구조 정의 (정확한 서브카테고리)
# ---------------------------------------------------------
CATEGORY_STRUCTURE = {
    "— 심혈관 질환": {
        "icon": "❤️",
        "color1": "#FF6B6B",
        "color2": "#EE5A6F",
        "subcategories": [
            {"name": "고혈압", "icon": "🩺", "color1": "#FF6B6B", "color2": "#EE5A6F"},
            {"name": "고지혈증(콜레스테롤)", "icon": "💊", "color1": "#4ECDC4", "color2": "#44A08D"},
            {"name": "협심증/심근경색", "icon": "💔", "color1": "#A18CD1", "color2": "#FBC2EB"},
            {"name": "동맥경화", "icon": "🫀", "color1": "#FA709A", "color2": "#FEE140"},
            {"name": "뇌졸중", "icon": "🧠", "color1": "#667eea", "color2": "#764ba2"}
        ]
    },
    "— 당뇨병": {
        "icon": "💉",
        "color1": "#4ECDC4",
        "color2": "#44A08D",
        "subcategories": [
            {"name": "당뇨", "icon": "💉", "color1": "#4ECDC4", "color2": "#44A08D"},
            {"name": "공복혈당장애", "icon": "📊", "color1": "#FA709A", "color2": "#FEE140"},
            {"name": "당뇨병 합병증 (망막,신장 등)", "icon": "⚠️", "color1": "#667eea", "color2": "#764ba2"}
        ]
    },
    "— 관절/근골격계 질환": {
        "icon": "🦴",
        "color1": "#A18CD1",
        "color2": "#FBC2EB",
        "subcategories": [
            {"name": "퇴행성 관절염", "icon": "🦵", "color1": "#A18CD1", "color2": "#FBC2EB"},
            {"name": "허리디스크/목디스크", "icon": "🧘", "color1": "#FA709A", "color2": "#FEE140"},
            {"name": "골다공증", "icon": "🦴", "color1": "#667eea", "color2": "#764ba2"},
            {"name": "오십견(유착성 관절낭염)", "icon": "💪", "color1": "#f093fb", "color2": "#f5576c"}
        ]
    },
    "— 호르몬/내분비 질환": {
        "icon": "🌡️",
        "color1": "#FA709A",
        "color2": "#FEE140",
        "subcategories": [
            {"name": "갑상선 기능 저하/항진", "icon": "🦋", "color1": "#FA709A", "color2": "#FEE140"},
            {"name": "갱년기 증후군", "icon": "🌸", "color1": "#667eea", "color2": "#764ba2"},
            {"name": "대사증후군", "icon": "⚖️", "color1": "#4ECDC4", "color2": "#44A08D"}
        ]
    },
    "— 정신 건강/신경계": {
        "icon": "🧠",
        "color1": "#667eea",
        "color2": "#764ba2",
        "subcategories": [
            {"name": "우울증/번아웃 증후군", "icon": "😔", "color1": "#667eea", "color2": "#764ba2"},
            {"name": "수면장애/불면증", "icon": "😴", "color1": "#4ECDC4", "color2": "#44A08D"},
            {"name": "치매/경도인지장애", "icon": "🧠", "color1": "#FA709A", "color2": "#FEE140"},
            {"name": "이명/어지럼증", "icon": "👂", "color1": "#A18CD1", "color2": "#FBC2EB"}
        ]
    },
    "— 소화기 질환": {
        "icon": "🍽️",
        "color1": "#f093fb",
        "color2": "#f5576c",
        "subcategories": [
            {"name": "위염/위궤양", "icon": "🤢", "color1": "#f093fb", "color2": "#f5576c"},
            {"name": "역류성 식도염", "icon": "🔥", "color1": "#FA709A", "color2": "#FEE140"},
            {"name": "과민성 대장증후군", "icon": "💨", "color1": "#667eea", "color2": "#764ba2"},
            {"name": "지방간/간기능 저하", "icon": "🫀", "color1": "#4ECDC4", "color2": "#44A08D"}
        ]
    },
    "— 안과/치과/기타": {
        "icon": "👁️",
        "color1": "#4facfe",
        "color2": "#00f2fe",
        "subcategories": [
            {"name": "백내장/녹내장", "icon": "👓", "color1": "#4facfe", "color2": "#00f2fe"},
            {"name": "치주염/치아손실", "icon": "🦷", "color1": "#FA709A", "color2": "#FEE140"},
            {"name": "비만/체형변화", "icon": "⚖️", "color1": "#667eea", "color2": "#764ba2"}
        ]
    }
}

# ---------------------------------------------------------
# 🎨 서브 카테고리 페이지 HTML 템플릿 생성
# ---------------------------------------------------------
def generate_subcategory_html(category_slug, category_data):
    subcategory_cards = ""
    for sub in category_data["subcategories"]:
        # 서브카테고리 슬러그 생성 (URL 인코딩된 형태로)
        sub_slug = sub['name'].replace('/', '-').replace(' ', '-').replace('(', '').replace(')', '')
        
        subcategory_cards += f"""
        <div class="health-card" style="--card-color-1:{sub['color1']}; --card-color-2:{sub['color2']};">
            <div class="health-card-icon">{sub['icon']}</div>
            <h3>{sub['name']}</h3>
            <a href="{WP_BASE_URL}/category/{category_slug}/{sub_slug}" aria-label="{sub['name']}"></a>
        </div>
        """
    
    html = f"""
<style>
/* 카테고리 설명 영역만 표시 */
.category-description {{
    display: block !important;
}}
.health-card-container {{
    padding: 60px 20px;
    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    min-height: 60vh;
}}
.health-cards-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 25px;
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
}}
.health-card {{
    position: relative;
    padding: 35px 25px;
    border-radius: 24px;
    background: linear-gradient(135deg, var(--card-color-1) 0%, var(--card-color-2) 100%);
    box-shadow: 0 10px 30px rgba(0,0,0,0.15);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    cursor: pointer;
    overflow: hidden;
    min-height: 180px;
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
    width: 120px;
    height: 120px;
    background: rgba(255,255,255,0.1);
    border-radius: 50%;
    transform: translate(40%, -40%);
}}
.health-card-icon {{
    font-size: 56px;
    margin-bottom: 15px;
    filter: drop-shadow(0 2px 4px rgba(0,0,0,0.2));
}}
.health-card h3 {{
    font-size: 22px;
    font-weight: 700;
    color: #ffffff;
    margin: 0;
    text-shadow: 0 2px 4px rgba(0,0,0,0.1);
    position: relative;
    z-index: 1;
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
    margin-bottom: 20px;
}}
.section-title .back-link {{
    display: inline-block;
    margin-bottom: 20px;
    padding: 10px 20px;
    background: rgba(255,255,255,0.9);
    border-radius: 50px;
    text-decoration: none;
    color: #667eea;
    font-weight: 600;
    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    transition: all 0.3s;
}}
.section-title .back-link:hover {{
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(0,0,0,0.15);
}}
.section-title h2 {{
    font-size: 38px;
    font-weight: 800;
    background: linear-gradient(135deg, {category_data['color1']} 0%, {category_data['color2']} 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0 0 40px 0;
}}
.section-title .main-icon {{
    font-size: 64px;
    margin-bottom: 10px;
}}
@media (max-width: 768px) {{
    .health-cards-grid {{
        grid-template-columns: 1fr;
        gap: 20px;
    }}
    .section-title h2 {{
        font-size: 28px;
    }}
}}
/* 카테고리 제목 숨기기 */
.archive-title {{
    display: none;
}}
</style>

<div class="health-card-container">
    <div class="section-title">
        <a href="{WP_BASE_URL}" class="back-link">← 홈으로 돌아가기</a>
        <div class="main-icon">{category_data['icon']}</div>
        <h2>{category_slug.replace('-', ' ')}</h2>
    </div>
    
    <div class="health-cards-grid">
        {subcategory_cards}
    </div>
</div>
"""
    return html


# ---------------------------------------------------------
# ✅ WebDriver 설정
# ---------------------------------------------------------
def setup_driver():
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    return driver


def wp_login(driver):
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


# ---------------------------------------------------------
# 📝 카테고리 설명 업데이트
# ---------------------------------------------------------
def update_category_description(driver, category_slug, html_content):
    print(f"\n--- 📂 '{category_slug}' 카테고리 페이지 생성 중 ---")
    
    try:
        # 카테고리 편집 페이지로 이동
        driver.get(f"{WP_ADMIN_URL}edit-tags.php?taxonomy=category")
        time.sleep(2)
        
        # 카테고리 찾기 및 편집 링크 클릭
        try:
            category_link = driver.find_element(By.XPATH, f"//a[contains(@class, 'row-title') and contains(text(), '{category_slug}')]")
            edit_url = category_link.get_attribute('href')
            driver.get(edit_url)
            time.sleep(2)
            print(f"  ✓ 카테고리 편집 페이지 접근")
        except:
            print(f"  ❌ 카테고리를 찾을 수 없습니다: {category_slug}")
            return False
        
        # Description 필드에 HTML 주입
        try:
            description_field = driver.find_element(By.ID, "description")
            driver.execute_script("arguments[0].value = arguments[1];", description_field, html_content)
            print(f"  ✓ HTML 콘텐츠 주입 완료")
            time.sleep(1)
        except Exception as e:
            print(f"  ❌ Description 필드를 찾을 수 없습니다: {e}")
            return False
        
        # 업데이트 버튼 클릭
        try:
            # Try multiple methods to submit the form
            try:
                update_button = driver.find_element(By.ID, "submit")
                driver.execute_script("arguments[0].click();", update_button)
            except:
                # Alternative: find by name or class
                try:
                    update_button = driver.find_element(By.CSS_SELECTOR, "input[type='submit'].button-primary")
                    driver.execute_script("arguments[0].click();", update_button)
                except:
                    # Last resort: submit the form directly
                    form = driver.find_element(By.ID, "edittag")
                    driver.execute_script("arguments[0].submit();", form)
            
            time.sleep(2)
            print(f"  ✅ '{category_slug}' 카테고리 페이지 생성 완료!")
            return True
        except Exception as e:
            print(f"  ❌ 업데이트 버튼 클릭 실패: {e}")
            return False
            
    except Exception as e:
        print(f"  ❌ 오류 발생: {e}")
        return False


# ---------------------------------------------------------
# 🚀 메인 실행
# ---------------------------------------------------------
def main():
    driver = setup_driver()
    
    if not wp_login(driver):
        print("❌ 로그인 실패. 사용자명/비밀번호를 확인하세요.")
        driver.quit()
        return
    
    print("\n" + "="*60)
    print("🎨 워드프레스 카테고리 페이지 자동 생성 시작")
    print("="*60 + "\n")
    
    # 각 카테고리별 서브 카테고리 페이지 생성
    success_count = 0
    for category_slug, category_data in CATEGORY_STRUCTURE.items():
        html_content = generate_subcategory_html(category_slug, category_data)
        if update_category_description(driver, category_slug, html_content):
            success_count += 1
        time.sleep(2)
    
    print("\n" + "="*60)
    print(f"✨ 완료! {success_count}/{len(CATEGORY_STRUCTURE)}개 카테고리 페이지 생성됨")
    print("="*60)
    print("\n📌 다음 단계:")
    print("1. 워드프레스 사이트에서 각 카테고리 페이지를 확인하세요")
    print("2. 서브카테고리를 클릭하면 해당 글 목록이 2열로 표시됩니다")
    print("3. CSS는 이미 적용되어 있습니다 (강력한-카테고리-스타일.css)")
    print("\n🌐 사이트 확인: " + WP_BASE_URL)
    
    driver.quit()


if __name__ == "__main__":
    main()

