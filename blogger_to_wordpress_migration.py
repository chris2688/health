import sys
import io
import os
import time
import requests
import mimetypes
import random
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from PIL import Image

# ---------------------------------------------------------
# ✅ 설정 변수 (비밀번호 확인!)
# ---------------------------------------------------------
WP_LOGIN_URL = "https://health9988234.mycafe24.com/wp-login.php"
WP_ADMIN_URL = "https://health9988234.mycafe24.com/wp-admin/"
WP_USER = "health9988234"
WP_PASSWORD = "ssurlf7904!"

# 이미지 최대 크기 (가로/세로 긴 쪽 기준)
MAX_DIMENSION = 2500

# 📅 날짜 랜덤 범위 설정 (이 기간 사이로 발행됨)
START_DATE = datetime(2024, 1, 1)
END_DATE = datetime(2025, 10, 31)

DOMAIN_CATEGORY_MAP = {
    "index001": "질환별 정보",
    "index002": "식단/음식",
    "index003": "운동/활동",
    "index004": "생활습관",
    "index005": "건강News",
    "post001": "생활습관", "post002": "식단/음식", "post003": "운동/활동"
}

TARGET_URLS = [
    "https://index001.ceolife4u.com/",
    "https://index002.ceolife4u.com/",
    "https://index003.ceolife4u.com/",
    "https://index004.ceolife4u.com/",
    "https://index005.ceolife4u.com/",
    "https://post001.ceolife4u.com/",
    "https://post002.ceolife4u.com/",
    "https://post003.ceolife4u.com/"
]

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

def get_random_date():
    """지정된 범위 내의 랜덤 날짜 생성"""
    delta = END_DATE - START_DATE
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = random.randrange(int_delta)
    rand_date = START_DATE + timedelta(seconds=random_second)
    # 활동 시간대 (08:00 ~ 23:00)로 조정
    return rand_date.replace(hour=random.randint(8, 23), minute=random.randint(0, 59))

def setup_driver():
    print("🌐 Chrome 브라우저 시작 중...")
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-notifications")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    driver.maximize_window()
    return driver

def wp_login(driver):
    print(f"🔐 WordPress 로그인 시도: {WP_LOGIN_URL}")
    driver.get(WP_LOGIN_URL)
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "user_login"))).send_keys(WP_USER)
        driver.find_element(By.ID, "user_pass").send_keys(WP_PASSWORD)
        driver.find_element(By.ID, "wp-submit").click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "adminmenu")))
        print("  ✓ 로그인 성공!")
        return True
    except Exception as e:
        print(f"  ❌ 로그인 실패: {e}")
        return False

def download_and_resize_image(img_url):
    try:
        if not img_url.startswith("http"): return None
        headers = {'User-Agent': 'Mozilla/5.0', 'Referer': 'https://www.google.com/'}
        response = requests.get(img_url, headers=headers, timeout=20)
        
        if response.status_code == 200:
            content_type = response.headers.get('content-type', '').lower()
            ext = mimetypes.guess_extension(content_type)
            if not ext: ext = '.jpg'
            if ext == '.jpe': ext = '.jpg'
            output_ext = '.jpg' if ext == '.webp' else ext
            
            filename = f"img_{int(time.time())}_{str(os.urandom(4).hex())}{output_ext}"
            save_path = os.path.abspath(filename)
            
            try:
                img_data = io.BytesIO(response.content)
                with Image.open(img_data) as img:
                    if img.mode != 'RGB': img = img.convert('RGB')
                    width, height = img.size
                    if width > MAX_DIMENSION or height > MAX_DIMENSION:
                        if width > height:
                            new_width = MAX_DIMENSION
                            new_height = int((MAX_DIMENSION / width) * height)
                        else:
                            new_height = MAX_DIMENSION
                            new_width = int((MAX_DIMENSION / height) * width)
                        img = img.resize((new_width, new_height), Image.LANCZOS)
                    img.save(save_path, quality=85, optimize=True)
                return save_path
            except:
                with open(save_path, 'wb') as f: f.write(response.content)
                return save_path
        return None
    except: return None

def upload_image_in_new_tab(driver, file_path):
    if not file_path or not os.path.exists(file_path): return None
    main_window = driver.current_window_handle
    new_url = None
    try:
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[-1])
        driver.get(WP_ADMIN_URL + "media-new.php")
        
        file_input = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, "//input[@type='file']")))
        file_input.send_keys(file_path)
        
        edit_link = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.CLASS_NAME, "edit-attachment")))
        edit_href = edit_link.get_attribute("href")
        driver.get(edit_href)
        
        url_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "attachment_url")))
        new_url = url_input.get_attribute("value")
    except Exception as e:
        print(f"      ⚠ 업로드 실패: {e}")
    finally:
        if len(driver.window_handles) > 1: driver.close()
        driver.switch_to.window(main_window)
    return new_url

def process_content_images(driver, soup):
    for tag in soup.find_all('div', class_=['tab-wrapper', '.apply-container', 'link-container']): tag.decompose()
    for tag in soup.find_all(['script', 'ins']): tag.decompose()
    
    imgs = soup.find_all('img')
    if imgs:
        print(f"    🖼️ 본문 이미지 {len(imgs)}개 처리 시작...")
        for img in imgs:
            target_url = img.get('src')
            parent_a = img.find_parent('a')
            if parent_a and 'blogger.googleusercontent.com' in str(parent_a.get('href')):
                target_url = parent_a.get('href')
            if not target_url: continue

            local_path = download_and_resize_image(target_url)
            if local_path:
                new_url = upload_image_in_new_tab(driver, local_path)
                if new_url:
                    print(f"      ✅ 교체 완료")
                    img['src'] = new_url
                    if parent_a: parent_a['href'] = new_url
                    
                    if img.has_attr('srcset'): del img['srcset']
                    if img.has_attr('width'): del img['width']
                    if img.has_attr('height'): del img['height']
                    classes = img.get('class', [])
                    if 'aligncenter' not in classes: classes.append('aligncenter')
                    if 'size-full' not in classes: classes.append('size-full')
                    img['class'] = classes
                    img['style'] = "max-width: 100%; height: auto;"
                if os.path.exists(local_path): os.remove(local_path)
            else: print("      ⚠ 다운로드 실패")
    return soup

def write_to_wordpress(driver, title, content_html, category_name):
    print("    📝 글 작성 페이지 이동...")
    driver.get(WP_ADMIN_URL + "post-new.php")
    
    try:
        # 1. 제목 입력
        title_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "post_title")))
        title_field.clear()
        title_field.send_keys(title)
        
        # 2. 카테고리 자동 선택 & 미분류 해제
        if category_name:
            try:
                print(f"      📂 카테고리: {category_name}")
                xpath = f"//ul[@id='categorychecklist']//label[contains(text(), '{category_name}')]/input"
                target = driver.find_element(By.XPATH, xpath)
                if not target.is_selected(): driver.execute_script("arguments[0].click();", target)
                
                # 미분류 해제
                try:
                    uncat = driver.find_element(By.ID, "in-category-1")
                    if uncat.is_selected(): driver.execute_script("arguments[0].click();", uncat)
                except: pass
            except: pass

        # 3. 본문 입력
        try:
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "content-html"))).click()
            time.sleep(1)
            content_field = driver.find_element(By.ID, "content")
            content_field.clear()
            driver.execute_script("arguments[0].value = arguments[1];", content_field, content_html)
        except: pass

        # 4. 🔥 날짜 수정 (Random Date)
        try:
            rand_date = get_random_date()
            print(f"      📅 날짜 설정: {rand_date.strftime('%Y-%m-%d %H:%M')}")
            
            # '편집' 링크 클릭 (Publish immediately 옆)
            edit_date_link = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "edit-timestamp"))
            )
            edit_date_link.click()
            time.sleep(0.5)

            # 월 선택
            Select(driver.find_element(By.ID, "mm")).select_by_value(f"{rand_date.month:02d}")
            # 일, 년, 시, 분 입력 (Classic Editor 기준)
            driver.find_element(By.ID, "jj").clear()
            driver.find_element(By.ID, "jj").send_keys(f"{rand_date.day:02d}")
            driver.find_element(By.ID, "aa").clear()
            driver.find_element(By.ID, "aa").send_keys(f"{rand_date.year}")
            driver.find_element(By.ID, "hh").clear()
            driver.find_element(By.ID, "hh").send_keys(f"{rand_date.hour:02d}")
            driver.find_element(By.ID, "mn").clear()
            driver.find_element(By.ID, "mn").send_keys(f"{rand_date.minute:02d}")
            
            # 확인 버튼 클릭
            driver.find_element(By.CLASS_NAME, "save-timestamp").click()
            time.sleep(0.5)
        except Exception as e:
            print(f"      ⚠ 날짜 설정 실패(오늘 날짜로 발행됨): {e}")

        # 5. 발행
        print("    🚀 발행 버튼 클릭...")
        publish_btn = driver.find_element(By.ID, "publish")
        driver.execute_script("arguments[0].scrollIntoView();", publish_btn)
        time.sleep(1)
        publish_btn.click()
        time.sleep(5)
        print("    ✓ 발행 완료!")
            
    except Exception as e:
        print(f"    ❌ 작성 실패: {e}")

def crawl_and_migrate():
    driver = setup_driver()
    if not wp_login(driver): return

    total_posts = 0
    for domain in TARGET_URLS:
        print(f"\n🌐 {domain} 처리 중...")
        category_name = None
        for key in DOMAIN_CATEGORY_MAP:
            if key in domain:
                category_name = DOMAIN_CATEGORY_MAP[key]
                break
        
        try:
            sitemap_url = domain.rstrip('/') + "/sitemap.xml"
            resp = requests.get(sitemap_url)
            post_urls = []
            if resp.status_code == 200:
                soup = BeautifulSoup(resp.content, 'xml')
                post_urls = [url.text for url in soup.find_all('loc') if '.html' in url.text]
            
            if not post_urls:
                resp = requests.get(domain)
                soup = BeautifulSoup(resp.content, 'html.parser')
                for a in soup.find_all('a', href=True):
                    if domain in a['href'] and '.html' in a['href'] and a['href'] not in post_urls:
                        post_urls.append(a['href'])

            print(f"  ✓ {len(post_urls)}개 글 발견 (카테고리: {category_name})")
            
            for idx, url in enumerate(post_urls):
                print(f"\n  [{idx+1}/{len(post_urls)}] {url}")
                try:
                    page_resp = requests.get(url)
                    page_soup = BeautifulSoup(page_resp.content, 'html.parser')
                    
                    title = page_soup.find('h3', class_='post-title')
                    if not title: title = page_soup.find('h1')
                    title_text = title.text.strip() if title else "제목 없음"
                    
                    content_div = page_soup.find('div', class_='post-body')
                    if not content_div: content_div = page_soup.find('div', class_='entry-content')
                    
                    if content_div:
                        content_div = process_content_images(driver, content_div)
                        content_html = str(content_div)
                        write_to_wordpress(driver, title_text, content_html, category_name)
                        total_posts += 1
                except Exception as e:
                    print(f"    ❌ 에러: {e}")
        except: pass

    print(f"\n✨ 완료! 총 {total_posts}개 이동.")
    driver.quit()

if __name__ == "__main__":
    crawl_and_migrate()