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

# 각 카테고리의 서브 카테고리 정의 (실제 WordPress에 등록된 것 기준)
CATEGORY_SUBCATEGORIES = {
    "— 심혈관 질환": {
        "icon": "❤️",
        "color1": "#FF6B6B",
        "color2": "#EE5A6F",
        "subcategories": []  # 일단 비워두고, 실제 글들을 앱 아이콘으로 표시
    },
    "— 당뇨병": {
        "icon": "💉",
        "color1": "#4ECDC4",
        "color2": "#44A08D",
        "subcategories": []
    },
    "— 관절/근골격계 질환": {
        "icon": "🦴",
        "color1": "#A18CD1",
        "color2": "#FBC2EB",
        "subcategories": []
    },
    "— 호르몬/내분비 질환": {
        "icon": "🌡️",
        "color1": "#FA709A",
        "color2": "#FEE140",
        "subcategories": []
    },
    "— 정신 건강/신경계": {
        "icon": "🧠",
        "color1": "#667eea",
        "color2": "#764ba2",
        "subcategories": []
    },
    "— 소화기 질환": {
        "icon": "🍽️",
        "color1": "#f093fb",
        "color2": "#f5576c",
        "subcategories": []
    },
    "— 안과/치과/기타": {
        "icon": "👁️",
        "color1": "#4facfe",
        "color2": "#00f2fe",
        "subcategories": []
    }
}


def generate_category_header_html(category_name, category_data):
    """카테고리 상단에 표시할 HTML (뒤로가기 버튼 + 아이콘)"""
    html = f"""
<style>
.category-header-custom {{
    text-align: center;
    padding: 30px 20px;
    background: linear-gradient(135deg, {category_data['color1']} 0%, {category_data['color2']} 100%);
    border-radius: 20px;
    margin-bottom: 30px;
}}
.back-to-home {{
    display: inline-block;
    margin-bottom: 15px;
    padding: 10px 24px;
    background: rgba(255,255,255,0.95);
    border-radius: 50px;
    text-decoration: none;
    color: {category_data['color1']};
    font-weight: 600;
    font-size: 14px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    transition: all 0.3s;
}}
.back-to-home:hover {{
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(0,0,0,0.15);
    background: #ffffff;
}}
.category-icon-large {{
    font-size: 64px;
    margin-bottom: 10px;
    filter: drop-shadow(0 4px 8px rgba(0,0,0,0.2));
}}
.category-title-custom {{
    font-size: 32px;
    font-weight: 800;
    color: #ffffff;
    margin: 0;
    text-shadow: 0 2px 4px rgba(0,0,0,0.1);
}}
</style>

<div class="category-header-custom">
    <a href="{WP_BASE_URL}" class="back-to-home">← 홈으로 돌아가기</a>
    <div class="category-icon-large">{category_data['icon']}</div>
    <h2 class="category-title-custom">{category_name.replace('— ', '')}</h2>
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


def update_category_description(driver, category_name, html_content):
    print(f"\n--- 📂 '{category_name}' 카테고리 업데이트 중 ---")
    
    try:
        # 카테고리 목록 페이지로 이동
        driver.get(f"{WP_ADMIN_URL}edit-tags.php?taxonomy=category")
        time.sleep(2)
        
        # 카테고리 찾기
        try:
            category_link = driver.find_element(By.XPATH, f"//a[contains(@class, 'row-title') and text()='{category_name}']")
            edit_url = category_link.get_attribute('href')
            driver.get(edit_url)
            time.sleep(2)
            print(f"  ✓ 카테고리 편집 페이지 접근")
        except:
            print(f"  ❌ 카테고리를 찾을 수 없습니다: {category_name}")
            return False
        
        # Description 필드에 HTML 주입
        try:
            description_field = driver.find_element(By.ID, "description")
            current_desc = description_field.get_attribute("value")
            
            # 기존 커스텀 헤더가 있으면 제거하고 새로 추가
            if "<div class=\"category-header-custom\"" in current_desc:
                # 기존 커스텀 헤더 제거
                import re
                current_desc = re.sub(r'<style>.*?</style>\s*<div class="category-header-custom">.*?</div>', '', current_desc, flags=re.DOTALL)
            
            new_desc = html_content + "\n" + current_desc
            driver.execute_script("arguments[0].value = arguments[1];", description_field, new_desc)
            print(f"  ✓ HTML 콘텐츠 주입 완료")
            time.sleep(1)
        except Exception as e:
            print(f"  ❌ Description 필드 접근 실패: {e}")
            return False
        
        # 업데이트 버튼 클릭
        try:
            update_button = driver.find_element(By.ID, "submit")
            driver.execute_script("arguments[0].click();", update_button)
            time.sleep(2)
            print(f"  ✅ '{category_name}' 업데이트 완료!")
            return True
        except Exception as e:
            print(f"  ❌ 업데이트 실패: {e}")
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
    total_count = len(CATEGORY_SUBCATEGORIES)
    
    for category_name, category_data in CATEGORY_SUBCATEGORIES.items():
        html_content = generate_category_header_html(category_name, category_data)
        if update_category_description(driver, category_name, html_content):
            success_count += 1
        time.sleep(2)
    
    print("\n" + "=" * 60)
    print(f"✨ 완료! {success_count}/{total_count}개 카테고리 업데이트됨")
    print("=" * 60)
    
    driver.quit()


if __name__ == "__main__":
    main()

