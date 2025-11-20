import sys
import io
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select
import time
import os

# UTF-8 인코딩 설정
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# WordPress 정보
WP_URL = "https://health9988234.mycafe24.com"
WP_USERNAME = "health9988234"
WP_PASSWORD = "ssurlf7904!"

def login_to_wordpress(driver):
    """WordPress 로그인"""
    print("🔐 WordPress 로그인 중...")
    driver.get(f"{WP_URL}/wp-login.php")
    time.sleep(2)
    
    username_field = driver.find_element(By.ID, "user_login")
    password_field = driver.find_element(By.ID, "user_pass")
    
    username_field.clear()
    username_field.send_keys(WP_USERNAME)
    password_field.clear()
    password_field.send_keys(WP_PASSWORD)
    
    login_button = driver.find_element(By.ID, "wp-submit")
    login_button.click()
    time.sleep(3)
    print("✅ 로그인 완료!")

def upload_template_file(driver):
    """템플릿 파일을 테마 폴더에 업로드"""
    print("\n📁 템플릿 파일 업로드 중...")
    
    try:
        # 파일 관리자 또는 플러그인을 통해 업로드하는 것은 복잡하므로
        # FTP나 파일 관리자를 통해 수동으로 업로드해야 할 수 있습니다
        # 대신 테마 편집기를 통해 직접 파일을 생성하겠습니다
        
        # 테마 편집기로 이동
        driver.get(f"{WP_URL}/wp-admin/theme-editor.php")
        time.sleep(3)
        
        # 새 파일 추가 (일부 테마는 지원하지 않을 수 있음)
        print("  ℹ️ 테마 편집기를 통한 파일 추가는 제한적입니다")
        print("  💡 대안: 페이지 빌더를 사용하거나 기존 페이지 템플릿 수정")
        
        return False  # 수동 업로드 필요
        
    except Exception as e:
        print(f"  ❌ 템플릿 파일 업로드 실패: {e}")
        return False

def create_custom_homepage(driver):
    """커스텀 홈페이지 생성"""
    print("\n📝 커스텀 홈페이지 생성 중...")
    
    try:
        # 새 페이지 추가
        driver.get(f"{WP_URL}/wp-admin/post-new.php?post_type=page")
        time.sleep(3)
        
        # Gutenberg 에디터가 로드될 때까지 대기
        try:
            # 제목 입력
            title_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "h1.editor-post-title__input, .editor-post-title__input, input[placeholder='제목 추가'], textarea[placeholder='제목 추가']"))
            )
            title_field.click()
            time.sleep(1)
            title_field.send_keys("메인 홈")
            print("  ✓ 페이지 제목 입력: 메인 홈")
            time.sleep(2)
            
            # HTML 블록 추가
            # + 버튼 클릭
            try:
                add_block_button = driver.find_element(By.CSS_SELECTOR, ".block-editor-inserter__toggle, .edit-post-header-toolbar__inserter-toggle")
                add_block_button.click()
                time.sleep(2)
                
                # HTML 검색
                search_box = driver.find_element(By.CSS_SELECTOR, "input[placeholder='검색'], .block-editor-inserter__search input")
                search_box.send_keys("HTML")
                time.sleep(2)
                
                # HTML 블록 선택
                html_block = driver.find_element(By.XPATH, "//button[contains(., 'Custom HTML') or contains(., '사용자 정의 HTML')]")
                html_block.click()
                time.sleep(2)
                print("  ✓ HTML 블록 추가")
                
            except Exception as e:
                print(f"  ⚠️ 블록 추가 실패 (수동으로 진행 필요): {e}")
                return False
            
            # HTML 코드 읽기
            with open('page-home-custom.php', 'r', encoding='utf-8') as f:
                template_content = f.read()
            
            # PHP 태그 제거하고 HTML/CSS만 추출
            # get_header()와 get_footer() 사이의 내용만 가져오기
            start_marker = "get_header(); ?>"
            end_marker = "<?php get_footer();"
            
            if start_marker in template_content and end_marker in template_content:
                html_content = template_content.split(start_marker)[1].split(end_marker)[0]
            else:
                html_content = template_content
            
            # HTML 코드 입력
            try:
                html_textarea = driver.find_element(By.CSS_SELECTOR, "textarea.block-editor-plain-text")
                driver.execute_script("arguments[0].value = arguments[1];", html_textarea, html_content)
                print("  ✓ HTML 코드 입력")
                time.sleep(2)
            except Exception as e:
                print(f"  ❌ HTML 코드 입력 실패: {e}")
                return False
            
            # 게시 버튼 클릭
            try:
                publish_button = driver.find_element(By.CSS_SELECTOR, ".editor-post-publish-panel__toggle, .editor-post-publish-button__button")
                publish_button.click()
                time.sleep(2)
                
                # 최종 게시 버튼 클릭 (2단계 게시)
                try:
                    final_publish = driver.find_element(By.CSS_SELECTOR, ".editor-post-publish-button")
                    final_publish.click()
                    time.sleep(3)
                    print("  ✅ 페이지 게시 완료!")
                except:
                    print("  ✓ 페이지 저장됨 (1단계 게시)")
                
                return True
            except Exception as e:
                print(f"  ⚠️ 게시 버튼 클릭 실패: {e}")
                # 수동 게시 필요
                return False
                
        except Exception as e:
            print(f"  ❌ 페이지 생성 실패: {e}")
            return False
            
    except Exception as e:
        print(f"  ❌ 오류 발생: {e}")
        return False

def set_as_homepage(driver, page_title="메인 홈"):
    """생성한 페이지를 홈페이지로 설정"""
    print("\n🏠 홈페이지 설정 중...")
    
    try:
        # 설정 > 읽기 페이지로 이동
        driver.get(f"{WP_URL}/wp-admin/options-reading.php")
        time.sleep(3)
        
        # "고정 페이지" 라디오 버튼 선택
        try:
            static_page_radio = driver.find_element(By.CSS_SELECTOR, "input[value='page']#page_on_front")
            if not static_page_radio.is_selected():
                driver.execute_script("arguments[0].click();", static_page_radio)
                time.sleep(1)
                print("  ✓ '고정 페이지' 옵션 선택")
        except Exception as e:
            print(f"  ⚠️ 고정 페이지 옵션 선택 실패: {e}")
        
        # 홈페이지 드롭다운에서 "메인 홈" 페이지 선택
        try:
            homepage_select = Select(driver.find_element(By.ID, "page_on_front"))
            
            # 페이지 목록에서 "메인 홈" 찾기
            found = False
            for option in homepage_select.options:
                if page_title in option.text:
                    homepage_select.select_by_visible_text(option.text)
                    found = True
                    print(f"  ✓ 홈페이지로 '{option.text}' 선택")
                    break
            
            if not found:
                print(f"  ⚠️ '{page_title}' 페이지를 찾을 수 없습니다")
                print("  📋 사용 가능한 페이지:")
                for option in homepage_select.options:
                    print(f"     - {option.text}")
                return False
                
        except Exception as e:
            print(f"  ❌ 홈페이지 선택 실패: {e}")
            return False
        
        # 변경사항 저장
        try:
            save_button = driver.find_element(By.ID, "submit")
            save_button.click()
            time.sleep(3)
            print("  ✅ 설정 저장 완료!")
            return True
        except Exception as e:
            print(f"  ❌ 저장 실패: {e}")
            return False
            
    except Exception as e:
        print(f"  ❌ 홈페이지 설정 실패: {e}")
        return False

def main():
    print("=" * 60)
    print("🏠 9988 건강 연구소 커스텀 홈페이지 설정")
    print("=" * 60)
    
    # 크롬 드라이버 설정
    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        # 로그인
        login_to_wordpress(driver)
        
        # 커스텀 홈페이지 생성
        if create_custom_homepage(driver):
            print("\n⏳ 페이지가 완전히 생성될 때까지 5초 대기 중...")
            time.sleep(5)
            
            # 홈페이지로 설정
            if set_as_homepage(driver):
                print("\n" + "=" * 60)
                print("✅ 모든 작업 완료!")
                print("🌐 사이트를 방문해서 Ctrl+F5로 새로고침하세요!")
                print("=" * 60)
            else:
                print("\n" + "=" * 60)
                print("⚠️ 페이지는 생성되었지만 홈페이지 설정 실패")
                print("💡 수동으로: 설정 > 읽기 > 홈페이지에서 '메인 홈' 선택")
                print("=" * 60)
        else:
            print("\n" + "=" * 60)
            print("❌ 페이지 생성 실패")
            print("💡 수동으로 페이지를 생성해주세요")
            print("=" * 60)
        
        # 브라우저 유지 (수동 확인 가능)
        print("\n⏳ 10초 후 브라우저가 닫힙니다...")
        time.sleep(10)
        
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()

