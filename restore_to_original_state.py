import sys
import io
import os
import re
import time
from ftplib import FTP
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# WordPress 정보
WP_LOGIN_URL = "https://health9988234.mycafe24.com/wp-login.php"
WP_ADMIN_URL = "https://health9988234.mycafe24.com/wp-admin/"
WP_USER = "health9988234"
WP_PASSWORD = "ssurlf7904!"

# FTP 정보
FTP_HOST = "health9988234.mycafe24.com"
FTP_USER = "health9988234"
FTP_PASS = "ssurlf7904!"
FTP_PORT = 21

# 카테고리 파일 목록
CATEGORY_FILES = [
    "category-심혈관질환.html",
    "category-당뇨병.html",
    "category-관절근골격계.html",
    "category-호르몬내분비.html",
    "category-정신건강신경계.html",
    "category-소화기질환.html",
    "category-안과치과기타.html",
]


def restore_htaccess():
    """원래 .htaccess 파일로 복구"""
    print("=" * 60)
    print("📝 .htaccess 파일 복구")
    print("=" * 60)
    
    original_htaccess = """# 9988 건강 연구소 - index-v2.html로 리디렉션
DirectoryIndex index-v2.html index.php

<IfModule mod_rewrite.c>
RewriteEngine On
RewriteBase /
RewriteRule ^$ /index-v2.html [R=301,L]
</IfModule>
"""
    
    try:
        with open(".htaccess", "w", encoding="utf-8") as f:
            f.write(original_htaccess)
        print("✅ .htaccess 파일 복구 완료!")
        return True
    except Exception as e:
        print(f"❌ .htaccess 파일 복구 실패: {e}")
        return False


def remove_wordpress_posts_section(filepath):
    """카테고리 파일에서 WordPress 글 목록 섹션 제거"""
    if not os.path.exists(filepath):
        print(f"  ⚠️ 파일 없음: {filepath}")
        return False
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # posts-section과 관련 스타일, 스크립트 제거
        # 스타일 부분 제거
        content = re.sub(
            r'<style>\s*/\* 글 목록 스타일 \*/\s*.*?</style>',
            '',
            content,
            flags=re.DOTALL
        )
        
        # posts-section div 제거
        content = re.sub(
            r'<div class="posts-section">.*?</div>\s*</div>',
            '',
            content,
            flags=re.DOTALL
        )
        
        # loadCategoryPosts 함수와 관련 스크립트 제거
        content = re.sub(
            r'<script>\s*// 썸네일 URL 가져오기.*?// 페이지 로드 시 실행.*?</script>',
            '',
            content,
            flags=re.DOTALL
        )
        
        # CATEGORY_MAPPING 관련 코드 제거
        content = re.sub(
            r'const CATEGORY_MAPPING = \{.*?\};',
            '',
            content,
            flags=re.DOTALL
        )
        
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  ✅ {filepath} - WordPress 글 기능 제거 완료")
            return True
        else:
            print(f"  ℹ️ {filepath} - 변경사항 없음")
            return False
            
    except Exception as e:
        print(f"  ❌ {filepath} - 오류: {e}")
        return False


def restore_permalink_to_default(driver):
    """Permalink를 '일반 설정'으로 복구"""
    print("\n" + "=" * 60)
    print("⚙️ Permalink를 '일반 설정'으로 복구")
    print("=" * 60)
    
    try:
        driver.get(f"{WP_ADMIN_URL}options-permalink.php")
        time.sleep(3)
        
        print("\n📝 '일반 설정' 옵션 찾기 중...")
        
        try:
            # "일반 설정" 라디오 버튼 찾기 (value="")
            common_radio = driver.find_element(By.CSS_SELECTOR, "input[type='radio'][value='']")
            
            if not common_radio.is_selected():
                print("  ✓ '일반 설정' 선택 중...")
                driver.execute_script("arguments[0].click();", common_radio)
                time.sleep(1)
            else:
                print("  ℹ️ '일반 설정'이 이미 선택되어 있습니다")
        except Exception as e:
            print(f"  ⚠️ '일반 설정' 라디오 버튼을 찾을 수 없습니다: {e}")
            return False
        
        # 저장 버튼 클릭
        try:
            save_button = driver.find_element(By.ID, "submit")
            print("\n💾 설정 저장 중...")
            driver.execute_script("arguments[0].click();", save_button)
            time.sleep(3)
            print("  ✅ 저장 완료!")
            return True
        except Exception as e:
            print(f"  ❌ 저장 버튼 클릭 실패: {e}")
            return False
            
    except Exception as e:
        print(f"❌ Permalink 복구 중 오류: {e}")
        return False


def upload_files_via_ftp(files):
    """FTP로 파일 업로드"""
    print("\n" + "=" * 60)
    print("📤 FTP 파일 업로드")
    print("=" * 60)
    
    try:
        print(f"\n🔗 FTP 서버 연결 중...")
        ftp = FTP()
        ftp.encoding = 'utf-8'
        ftp.connect(FTP_HOST, FTP_PORT, timeout=10)
        print("✅ 연결 성공!")
        
        print(f"🔐 로그인 중...")
        ftp.login(FTP_USER, FTP_PASS)
        print("✅ 로그인 성공!")
        
        uploaded_count = 0
        print(f"\n📤 파일 업로드 시작...\n")
        
        for file in files:
            if os.path.exists(file):
                try:
                    print(f"  업로드 중: {file}...", end=" ")
                    with open(file, "rb") as f:
                        ftp.storbinary(f"STOR {file}", f)
                    print("✅ 완료")
                    uploaded_count += 1
                except Exception as e:
                    print(f"❌ 실패: {str(e)[:50]}")
        
        ftp.quit()
        print(f"\n✅ 총 {uploaded_count}개 파일 업로드 완료!")
        return True
            
    except Exception as e:
        print(f"\n❌ FTP 업로드 오류: {e}")
        return False


def setup_driver():
    """WebDriver 설정"""
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    return driver


def wp_login(driver):
    """WordPress 로그인"""
    print("\n" + "=" * 60)
    print("🔐 WordPress 로그인")
    print("=" * 60)
    
    try:
        driver.get(WP_LOGIN_URL)
        time.sleep(2)
        
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
            print("✅ 로그인 성공!")
            return True
        else:
            print("❌ 로그인 실패")
            return False
    except Exception as e:
        print(f"❌ 로그인 중 오류: {e}")
        return False


def main():
    """메인 실행"""
    print("\n" + "=" * 60)
    print("🔄 원래 상태로 복구")
    print("=" * 60)
    print("\n💡 복구 작업:")
    print("   1. .htaccess 파일을 원래대로 복구")
    print("   2. 카테고리 페이지에서 WordPress 글 기능 제거")
    print("   3. WordPress Permalink를 '일반 설정'으로 복구")
    print("=" * 60)
    
    # 1. .htaccess 복구
    restore_htaccess()
    
    # 2. 카테고리 파일에서 WordPress 글 기능 제거
    print("\n" + "=" * 60)
    print("📝 카테고리 페이지에서 WordPress 글 기능 제거")
    print("=" * 60)
    print("\n📝 파일 수정 중...\n")
    
    fixed_files = []
    for file in CATEGORY_FILES:
        if remove_wordpress_posts_section(file):
            fixed_files.append(file)
    
    print(f"\n✅ 총 {len(fixed_files)}개 파일 수정 완료!")
    
    # 3. FTP 업로드
    files_to_upload = [".htaccess"] + fixed_files
    if files_to_upload:
        upload_files_via_ftp(files_to_upload)
    
    # 4. WordPress Permalink 복구
    print("\n" + "=" * 60)
    print("⚙️ WordPress 설정 복구")
    print("=" * 60)
    
    driver = setup_driver()
    try:
        if wp_login(driver):
            restore_permalink_to_default(driver)
    finally:
        print("\n⏳ 5초 후 브라우저 종료...")
        time.sleep(5)
        driver.quit()
    
    print("\n" + "=" * 60)
    print("✅ 복구 완료!")
    print("=" * 60)
    print("\n💡 복구된 상태:")
    print("   - .htaccess: index-v2.html로 리디렉션만 설정")
    print("   - 카테고리 페이지: 서브카테고리 링크만 있음 (WordPress 글 목록 없음)")
    print("   - WordPress Permalink: 일반 설정")
    print("=" * 60)


if __name__ == "__main__":
    main()

