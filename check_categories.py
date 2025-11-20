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

def main():
    driver = setup_driver()
    
    if not wp_login(driver):
        print("❌ 로그인 실패")
        driver.quit()
        return
    
    print("✓ 로그인 성공\n")
    
    # 카테고리 목록 페이지로 이동
    driver.get(f"{WP_ADMIN_URL}edit-tags.php?taxonomy=category")
    time.sleep(3)
    
    print("📂 현재 등록된 카테고리 목록:\n")
    print("=" * 60)
    
    # 모든 카테고리 행 찾기
    try:
        category_rows = driver.find_elements(By.CSS_SELECTOR, "#the-list tr")
        
        for row in category_rows:
            try:
                name_cell = row.find_element(By.CLASS_NAME, "name")
                category_link = name_cell.find_element(By.CLASS_NAME, "row-title")
                category_name = category_link.text
                
                slug_cell = row.find_element(By.CLASS_NAME, "slug")
                category_slug = slug_cell.text
                
                count_cell = row.find_element(By.CLASS_NAME, "posts")
                count = count_cell.text
                
                print(f"📌 이름: {category_name}")
                print(f"   Slug: {category_slug}")
                print(f"   글 개수: {count}")
                print("-" * 60)
                
            except:
                continue
                
    except Exception as e:
        print(f"❌ 오류: {e}")
    
    driver.quit()

if __name__ == "__main__":
    main()

