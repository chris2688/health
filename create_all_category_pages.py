import sys
import io
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

WP_LOGIN_URL = "https://health9988234.mycafe24.com/wp-login.php"
WP_ADMIN_URL = "https://health9988234.mycafe24.com/wp-admin/"
WP_USER = "health9988234"
WP_PASSWORD = "ssurlf7904!"
WP_BASE_URL = "https://health9988234.mycafe24.com"

# 전체 카테고리 구조
ALL_CATEGORIES = {
    "질환별-정보": {
        "title": "질환별 정보",
        "icon": "🏥",
        "color1": "#FF6B6B",
        "color2": "#EE5A6F",
        "subcategories": [
            {"name": "심혈관 질환", "icon": "❤️", "slug": "심혈관-질환", "color1": "#FF6B6B", "color2": "#EE5A6F"},
            {"name": "당뇨병", "icon": "💉", "slug": "당뇨병", "color1": "#4ECDC4", "color2": "#44A08D"},
            {"name": "관절/근골격계 질환", "icon": "🦴", "slug": "관절-근골격계-질환", "color1": "#A18CD1", "color2": "#FBC2EB"},
            {"name": "호르몬/내분비 질환", "icon": "🌡️", "slug": "호르몬-내분비-질환", "color1": "#FA709A", "color2": "#FEE140"},
            {"name": "정신 건강/신경계", "icon": "🧠", "slug": "정신-건강-신경계", "color1": "#667eea", "color2": "#764ba2"},
            {"name": "소화기 질환", "icon": "🍽️", "slug": "소화기-질환", "color1": "#f093fb", "color2": "#f5576c"},
            {"name": "안과/치과/기타", "icon": "👁️", "slug": "안과-치과-기타", "color1": "#4facfe", "color2": "#00f2fe"}
        ]
    },
    "식단-음식": {
        "title": "식단/음식",
        "icon": "🍱",
        "color1": "#11998e",
        "color2": "#38ef7d",
        "subcategories": [
            {"name": "질환별 식단", "icon": "🥗", "color1": "#11998e", "color2": "#38ef7d"},
            {"name": "피해야 할 과일", "icon": "🚫🍎", "color1": "#ee0979", "color2": "#ff6a00"},
            {"name": "모르면 독이 된다", "icon": "⚠️", "color1": "#f2994a", "color2": "#f2c94c"}
        ]
    },
    "운동-활동": {
        "title": "운동/활동",
        "icon": "💪",
        "color1": "#667eea",
        "color2": "#764ba2",
        "subcategories": [
            {"name": "질환별 운동 가이드", "icon": "🏃‍♂️", "color1": "#4facfe", "color2": "#00f2fe"},
            {"name": "운동 팁!", "icon": "✨", "color1": "#43e97b", "color2": "#38f9d7"}
        ]
    },
    "생활습관": {
        "title": "생활습관",
        "icon": "🌱",
        "color1": "#fa709a",
        "color2": "#fee140",
        "subcategories": [
            {"name": "생활습관", "icon": "📅", "color1": "#fa709a", "color2": "#fee140"},
            {"name": "생활습관 바꾸기 팁", "icon": "💡", "color1": "#30cfd0", "color2": "#330867"}
        ]
    }
}


def generate_page_html(page_slug, page_data):
    subcategory_cards = ""
    for sub in page_data["subcategories"]:
        # slug가 있으면 카테고리 링크, 없으면 태그 검색 링크
        if "slug" in sub:
            link = f"{WP_BASE_URL}/category/{sub['slug']}"
        else:
            # 태그 또는 검색으로 연결
            link = f"{WP_BASE_URL}/?s={sub['name']}"
        
        subcategory_cards += f"""
        <a href="{link}" class="category-card" style="--card-color-1:{sub.get('color1', page_data['color1'])}; --card-color-2:{sub.get('color2', page_data['color2'])};">
            <div class="category-card-icon">{sub['icon']}</div>
            <h3>{sub['name']}</h3>
            <p>관련 글 보기 →</p>
        </a>
        """
    
    html = f"""
<style>
.entry-title {{
    display: none !important;
}}
.health-card-container {{
    padding: 60px 20px;
    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    min-height: 60vh;
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
.category-list-grid {{
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 25px;
    max-width: 1200px;
    margin: 0 auto;
}}
.category-card {{
    position: relative;
    padding: 40px 30px;
    border-radius: 24px;
    background: linear-gradient(135deg, var(--card-color-1) 0%, var(--card-color-2) 100%);
    box-shadow: 0 10px 30px rgba(0,0,0,0.15);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    cursor: pointer;
    overflow: hidden;
    min-height: 200px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
    text-decoration: none;
}}
.category-card:hover {{
    transform: translateY(-8px) scale(1.02);
    box-shadow: 0 20px 40px rgba(0,0,0,0.25);
}}
.category-card::before {{
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
.category-card-icon {{
    font-size: 64px;
    margin-bottom: 20px;
    filter: drop-shadow(0 2px 4px rgba(0,0,0,0.2));
}}
.category-card h3 {{
    font-size: 24px;
    font-weight: 700;
    color: #ffffff;
    margin: 0 0 10px 0;
    text-shadow: 0 2px 4px rgba(0,0,0,0.1);
    position: relative;
    z-index: 1;
}}
.category-card p {{
    font-size: 16px;
    color: rgba(255,255,255,0.9);
    margin: 0;
    font-weight: 500;
    position: relative;
    z-index: 1;
}}
@media (max-width: 640px) {{
    .category-list-grid {{
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
        <p class="subtitle">관심 주제를 선택하세요</p>
    </div>
    
    <div class="category-list-grid">
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
    print(f"🔐 WordPress 로그인...")
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


def find_or_create_page(driver, page_title, html_content):
    print(f"\n--- 📄 '{page_title}' 페이지 처리 중 ---")
    
    try:
        # 페이지 목록에서 기존 페이지 찾기
        driver.get(f"{WP_ADMIN_URL}edit.php?post_type=page")
        time.sleep(2)
        
        try:
            # 기존 페이지 찾기
            page_link = driver.find_element(By.XPATH, f"//a[contains(text(), '{page_title}')]")
            page_url = page_link.get_attribute("href")
            page_id = page_url.split('post=')[1].split('&')[0] if 'post=' in page_url else None
            
            if page_id:
                # 기존 페이지 수정
                driver.get(f"{WP_ADMIN_URL}post.php?post={page_id}&action=edit")
                time.sleep(10)
                print(f"  ✓ 기존 페이지 발견, 업데이트 중...")
            else:
                raise Exception("페이지 ID를 찾을 수 없습니다")
                
        except:
            # 새 페이지 생성
            driver.get(f"{WP_ADMIN_URL}post-new.php?post_type=page")
            time.sleep(10)
            print(f"  ✓ 새 페이지 생성 중...")
            
            # 제목 입력
            try:
                title_field = driver.find_element(By.ID, "title")
                title_field.clear()
                title_field.send_keys(page_title)
            except:
                pass
        
        # HTML 모드로 전환 및 콘텐츠 주입
        try:
            html_tab = driver.find_element(By.ID, "content-html")
            html_tab.click()
            time.sleep(1)
            content_field = driver.find_element(By.ID, "content")
            driver.execute_script("arguments[0].value = arguments[1];", content_field, html_content)
            print("  ✓ HTML 콘텐츠 주입 완료")
            time.sleep(2)
        except Exception as e:
            print(f"  ❌ HTML 주입 실패: {e}")
            return False
        
        # 발행/업데이트
        try:
            publish_button = driver.find_element(By.ID, "publish")
            driver.execute_script("arguments[0].click();", publish_button)
            time.sleep(3)
            print(f"  ✅ '{page_title}' 페이지 완료!")
            return True
        except Exception as e:
            print(f"  ❌ 발행 실패: {e}")
            return False
            
    except Exception as e:
        print(f"  ❌ 오류: {e}")
        return False


def main():
    driver = setup_driver()
    
    if not wp_login(driver):
        print("❌ 로그인 실패")
        driver.quit()
        return
    
    print("✓ 로그인 성공\n")
    print("=" * 60)
    
    success_count = 0
    total_count = len(ALL_CATEGORIES)
    
    for page_slug, page_data in ALL_CATEGORIES.items():
        html_content = generate_page_html(page_slug, page_data)
        if find_or_create_page(driver, page_data['title'], html_content):
            success_count += 1
        time.sleep(3)
    
    print("\n" + "=" * 60)
    print(f"✨ 완료! {success_count}/{total_count}개 카테고리 페이지 생성/업데이트됨")
    print("=" * 60)
    print("\n📋 다음 단계:")
    print("1. WordPress 관리자 → 외모 → 사용자 정의하기")
    print("2. '추가 CSS' 클릭")
    print("3. category-archive-style.css 파일 내용 붙여넣기")
    print("4. '공개' 버튼 클릭")
    
    driver.quit()


if __name__ == "__main__":
    main()

