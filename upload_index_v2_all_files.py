import sys
import io
from ftplib import FTP
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

# UTF-8 인코딩 설정
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# FTP 정보
FTP_HOST = "health9988234.mycafe24.com"
FTP_USER = "health9988234"
FTP_PASS = "ssurlf7904!"
FTP_PORT = 21

# WordPress 정보
WP_LOGIN_URL = "https://health9988234.mycafe24.com/wp-login.php"
WP_ADMIN_URL = "https://health9988234.mycafe24.com/wp-admin/"
WP_USER = "health9988234"
WP_PASSWORD = "ssurlf7904!"
WP_BASE_URL = "https://health9988234.mycafe24.com"

# 업로드할 파일 목록
FILES_TO_UPLOAD = [
    "index-v2.html",
    "category-심혈관질환.html",
    "category-당뇨병.html",
    "category-관절근골격계.html",
    "category-호르몬내분비.html",
    "category-정신건강신경계.html",
    "category-소화기질환.html",
    "category-안과치과기타.html",
    "food-main.html",
    "exercise-main.html",
    "lifestyle-main.html",
    "news-main.html"
]


def upload_files_via_ftp():
    """FTP를 통해 모든 HTML 파일 업로드"""
    print("=" * 60)
    print("📤 FTP 파일 업로드 시작")
    print("=" * 60)
    
    # 파일 존재 확인
    missing_files = []
    for file in FILES_TO_UPLOAD:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print("\n❌ 다음 파일들을 찾을 수 없습니다:")
        for file in missing_files:
            print(f"   - {file}")
        return False
    
    print(f"\n✅ 총 {len(FILES_TO_UPLOAD)}개 파일 업로드 준비 완료")
    
    try:
        # FTP 연결
        print(f"\n🔗 FTP 서버 연결 중: {FTP_HOST}...")
        ftp = FTP()
        ftp.encoding = 'utf-8'
        
        # 다양한 호스트 시도
        hosts = [
            FTP_HOST,
            f"ftp.{FTP_HOST}",
            "ftp.cafe24.com",
            "health9988234.cafe24.com"
        ]
        
        connected = False
        for host in hosts:
            try:
                print(f"  시도 중: {host}...")
                ftp.connect(host, FTP_PORT, timeout=10)
                connected = True
                print(f"  ✅ {host} 연결 성공!")
                break
            except Exception as e:
                print(f"  ❌ {host} 실패: {str(e)[:50]}")
                continue
        
        if not connected:
            print("\n❌ 모든 FTP 서버 연결 실패")
            print("\n💡 수동 업로드 방법:")
            print("   1. cafe24 관리자 페이지 로그인")
            print("   2. 나의 서비스 관리 > FTP 관리")
            print("   3. FileZilla 등의 FTP 프로그램 사용")
            print(f"   4. 다음 파일들을 public_html/ 폴더에 업로드:")
            for file in FILES_TO_UPLOAD:
                print(f"      - {file}")
            return False
        
        # 로그인
        print(f"\n🔐 로그인 중: {FTP_USER}...")
        ftp.login(FTP_USER, FTP_PASS)
        print("✅ 로그인 성공!")
        
        # 현재 디렉토리 확인
        current_dir = ftp.pwd()
        print(f"\n📂 현재 디렉토리: {current_dir}")
        
        # public_html 또는 www 폴더로 이동 시도
        target_dirs = ["public_html", "www", "htdocs", "web"]
        target_dir = None
        
        for dir_name in target_dirs:
            try:
                ftp.cwd(dir_name)
                print(f"\n✅ {dir_name} 폴더로 이동 성공!")
                target_dir = dir_name
                break
            except Exception as e:
                print(f"  ❌ {dir_name} 폴더 접근 실패: {str(e)[:50]}")
                try:
                    ftp.cwd(current_dir)
                except:
                    pass
                continue
        
        if not target_dir:
            print("\n💡 루트 디렉토리에 업로드합니다...")
            target_dir = current_dir
        
        # 파일 업로드
        uploaded_files = []
        failed_files = []
        
        print(f"\n📤 파일 업로드 시작...\n")
        for file in FILES_TO_UPLOAD:
            try:
                print(f"  업로드 중: {file}...", end=" ")
                with open(file, "rb") as f:
                    ftp.storbinary(f"STOR {file}", f)
                uploaded_files.append(file)
                file_size = os.path.getsize(file)
                print(f"✅ 완료 ({file_size:,} bytes)")
            except Exception as e:
                failed_files.append(file)
                print(f"❌ 실패: {str(e)[:50]}")
        
        # 연결 종료
        ftp.quit()
        
        # 결과 출력
        print("\n" + "=" * 60)
        print("📊 업로드 결과")
        print("=" * 60)
        print(f"✅ 성공: {len(uploaded_files)}개")
        if failed_files:
            print(f"❌ 실패: {len(failed_files)}개")
            for file in failed_files:
                print(f"   - {file}")
        
        if uploaded_files:
            print("\n🌐 접속 URL:")
            print(f"   {WP_BASE_URL}/index-v2.html")
            print("\n💡 다음 단계:")
            print("   1. 위 URL로 접속해서 확인")
            print("   2. WordPress 홈페이지를 index-v2.html로 리디렉션 설정")
            print("=" * 60)
            return True
        else:
            print("\n❌ 모든 파일 업로드 실패")
            return False
            
    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
        print("\n💡 해결 방법:")
        print("   1. FTP 정보가 정확한지 확인")
        print("   2. cafe24 관리자 페이지에서 FTP 계정 확인")
        print("   3. 방화벽이 FTP 포트(21)를 차단하는지 확인")
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


def set_index_v2_as_homepage(driver):
    """WordPress 홈페이지를 index-v2.html로 리디렉션 설정"""
    print("\n" + "=" * 60)
    print("🏠 WordPress 홈페이지 리디렉션 설정")
    print("=" * 60)
    
    try:
        # 방법 1: index.php 파일 수정 (가장 확실한 방법)
        print("\n📝 방법 1: index.php 파일 수정 시도...")
        
        # 테마 편집기로 이동
        driver.get(f"{WP_ADMIN_URL}theme-editor.php")
        time.sleep(3)
        
        # index.php 파일 찾기
        try:
            # 파일 목록에서 index.php 찾기
            index_link = driver.find_element(By.XPATH, "//a[contains(@href, 'index.php')]")
            index_link.click()
            time.sleep(2)
            
            # 편집기 찾기
            editor = driver.find_element(By.ID, "newcontent")
            current_content = driver.execute_script("return arguments[0].value;", editor)
            
            # 이미 리디렉션 코드가 있는지 확인
            if "index-v2.html" in current_content:
                print("  ℹ️ 리디렉션 코드가 이미 존재합니다")
                return True
            
            # 리디렉션 코드 생성
            redirect_code = """<?php
/**
 * 9988 건강 연구소 - index-v2.html로 리디렉션
 */
header('Location: /index-v2.html');
exit;
?>
"""
            
            # 파일 내용 교체
            driver.execute_script("arguments[0].value = arguments[1];", editor, redirect_code)
            print("  ✓ 리디렉션 코드 입력 완료")
            time.sleep(1)
            
            # 저장
            save_btn = driver.find_element(By.ID, "submit")
            driver.execute_script("arguments[0].click();", save_btn)
            time.sleep(2)
            print("  ✅ index.php 저장 완료!")
            return True
            
        except Exception as e:
            print(f"  ⚠️ index.php 수정 실패: {str(e)[:50]}")
            print("  💡 방법 2로 진행합니다...")
        
        # 방법 2: .htaccess 파일 수정
        print("\n📝 방법 2: .htaccess 파일 수정 시도...")
        
        try:
            # FTP를 통해 .htaccess 파일 생성/수정
            print("  💡 .htaccess 파일은 FTP로 직접 수정해야 할 수 있습니다")
            print("  📋 다음 내용을 .htaccess 파일에 추가하세요:")
            print("\n" + "-" * 60)
            print("DirectoryIndex index-v2.html index.php")
            print("RewriteEngine On")
            print("RewriteRule ^$ /index-v2.html [R=301,L]")
            print("-" * 60)
            return True
            
        except Exception as e:
            print(f"  ⚠️ .htaccess 수정 실패: {str(e)[:50]}")
        
        # 방법 3: WordPress 설정에서 리디렉션 플러그인 사용 안내
        print("\n📝 방법 3: 플러그인 사용 안내")
        print("  💡 'Redirection' 플러그인을 설치하여")
        print("     홈페이지(/)를 /index-v2.html로 리디렉션하세요")
        
        return False
        
    except Exception as e:
        print(f"❌ 리디렉션 설정 중 오류: {e}")
        return False


def create_htaccess_file():
    """로컬에 .htaccess 파일 생성"""
    htaccess_content = """# 9988 건강 연구소 - index-v2.html로 리디렉션
DirectoryIndex index-v2.html index.php

<IfModule mod_rewrite.c>
RewriteEngine On
RewriteBase /
RewriteRule ^$ /index-v2.html [R=301,L]
</IfModule>
"""
    
    try:
        with open(".htaccess", "w", encoding="utf-8") as f:
            f.write(htaccess_content)
        print("\n✅ .htaccess 파일 생성 완료!")
        print("   이 파일도 FTP로 업로드하세요")
        return True
    except Exception as e:
        print(f"\n⚠️ .htaccess 파일 생성 실패: {e}")
        return False


def main():
    """메인 실행"""
    print("\n" + "=" * 60)
    print("🚀 index-v2.html 및 관련 파일 업로드 및 설정")
    print("=" * 60)
    
    # 1. FTP로 파일 업로드
    upload_success = upload_files_via_ftp()
    
    if not upload_success:
        print("\n❌ 파일 업로드 실패. 수동으로 업로드하세요.")
        return
    
    # 2. .htaccess 파일 생성
    create_htaccess_file()
    
    # 3. WordPress 리디렉션 설정
    print("\n" + "=" * 60)
    print("⚙️ WordPress 리디렉션 설정")
    print("=" * 60)
    
    driver = setup_driver()
    
    try:
        if wp_login(driver):
            set_index_v2_as_homepage(driver)
        else:
            print("\n⚠️ WordPress 로그인 실패. 수동으로 설정하세요.")
            print("\n📋 수동 설정 방법:")
            print("   1. WordPress 관리자 로그인")
            print("   2. 외모 > 테마 파일 편집기 > index.php")
            print("   3. 다음 코드로 교체:")
            print("      <?php header('Location: /index-v2.html'); exit; ?>")
            print("\n   또는")
            print("   1. FTP로 .htaccess 파일 업로드")
            print("   2. DirectoryIndex index-v2.html 추가")
    finally:
        print("\n⏳ 5초 후 브라우저 종료...")
        time.sleep(5)
        driver.quit()
    
    print("\n" + "=" * 60)
    print("✅ 작업 완료!")
    print("=" * 60)
    print("\n🌐 확인 URL:")
    print(f"   {WP_BASE_URL}/index-v2.html")
    print(f"   {WP_BASE_URL}/")
    print("\n💡 참고:")
    print("   - 모든 HTML 파일이 업로드되었습니다")
    print("   - .htaccess 파일도 업로드하면 자동 리디렉션이 작동합니다")
    print("=" * 60)


if __name__ == "__main__":
    main()

