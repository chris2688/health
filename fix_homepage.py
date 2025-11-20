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

# ---------------------------------------------------------
# ✅ 설정 변수
# ---------------------------------------------------------
WP_LOGIN_URL = "https://health9988234.mycafe24.com/wp-login.php"
WP_ADMIN_URL = "https://health9988234.mycafe24.com/wp-admin/"
WP_USER = "health9988234"
WP_PASSWORD = "ssurlf7904!"
WP_BASE_URL = "https://health9988234.mycafe24.com"

# ---------------------------------------------------------
# 🎨 홈페이지 HTML
# ---------------------------------------------------------
HOMEPAGE_HTML = """
<style>
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

/* 페이지 제목과 기본 콘텐츠 숨기기 */
.entry-title, .page-title, h1.entry-title, .entry-content > *:not(.health-card-container) {
    display: none !important;
}

.health-card-container {
    padding: 60px 20px;
    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    min-height: 80vh;
}

.health-cards-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 30px;
    max-width: 1400px;
    margin: 0 auto;
    padding: 0 20px;
}

.health-card {
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

.health-card:hover {
    transform: translateY(-8px);
    box-shadow: 0 20px 40px rgba(0,0,0,0.25);
}

.health-card::before {
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

.health-card-icon {
    font-size: 48px;
    margin-bottom: 20px;
    filter: drop-shadow(0 2px 4px rgba(0,0,0,0.2));
    position: relative;
    z-index: 1;
}

.health-card h3 {
    font-size: 24px;
    font-weight: 700;
    color: #ffffff;
    margin: 0 0 12px 0;
    text-shadow: 0 2px 4px rgba(0,0,0,0.1);
    position: relative;
    z-index: 1;
}

.health-card p {
    font-size: 15px;
    color: rgba(255,255,255,0.9);
    margin: 0;
    line-height: 1.6;
    position: relative;
    z-index: 1;
}

.section-title {
    text-align: center;
    margin-bottom: 20px;
}

.section-title .subtitle {
    font-size: 16px;
    font-weight: 600;
    color: #4A90E2;
    text-transform: uppercase;
    letter-spacing: 2px;
    margin-bottom: 10px;
}

.section-title h2 {
    font-size: 42px;
    font-weight: 800;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0 0 50px 0;
}

@media (max-width: 768px) {
    .health-cards-grid {
        grid-template-columns: 1fr;
        gap: 20px;
    }
    .section-title h2 {
        font-size: 32px;
    }
}
</style>

<div class="health-card-container">
    <div class="section-title">
        <p class="subtitle">9988 건강 연구소 핵심 가이드</p>
        <h2>중년 건강의 모든 것, 분야별로 찾아보세요</h2>
    </div>
    
    <div class="health-cards-grid">
        <a href="https://health9988234.mycafe24.com/category/질환별-정보/심혈관-질환/" class="health-card" style="--card-color-1:#FF6B6B; --card-color-2:#EE5A6F;">
            <div class="health-card-icon">❤️</div>
            <h3>심혈관 질환</h3>
            <p>고혈압, 심근경색, 동맥경화</p>
        </a>
        
        <a href="https://health9988234.mycafe24.com/category/질환별-정보/당뇨병/" class="health-card" style="--card-color-1:#4ECDC4; --card-color-2:#44A08D;">
            <div class="health-card-icon">💉</div>
            <h3>당뇨병</h3>
            <p>혈당관리, 공복혈당, 합병증</p>
        </a>
        
        <a href="https://health9988234.mycafe24.com/category/질환별-정보/관절-근골격계-질환/" class="health-card" style="--card-color-1:#A18CD1; --card-color-2:#FBC2EB;">
            <div class="health-card-icon">🦴</div>
            <h3>관절/근골격계 질환</h3>
            <p>관절염, 허리디스크, 골다공증</p>
        </a>
        
        <a href="https://health9988234.mycafe24.com/category/질환별-정보/호르몬-내분비-질환/" class="health-card" style="--card-color-1:#FA709A; --card-color-2:#FEE140;">
            <div class="health-card-icon">🌡️</div>
            <h3>호르몬/내분비 질환</h3>
            <p>갱년기, 갑상선, 대사증후군</p>
        </a>
        
        <a href="https://health9988234.mycafe24.com/category/질환별-정보/정신-건강-신경계/" class="health-card" style="--card-color-1:#667eea; --card-color-2:#764ba2;">
            <div class="health-card-icon">🧠</div>
            <h3>정신 건강/신경계</h3>
            <p>우울증, 치매, 수면장애</p>
        </a>
        
        <a href="https://health9988234.mycafe24.com/category/질환별-정보/소화기-질환/" class="health-card" style="--card-color-1:#f093fb; --card-color-2:#f5576c;">
            <div class="health-card-icon">🍽️</div>
            <h3>소화기 질환</h3>
            <p>위염, 지방간, 역류성 식도염</p>
        </a>
        
        <a href="https://health9988234.mycafe24.com/category/질환별-정보/안과-치과-기타/" class="health-card" style="--card-color-1:#4facfe; --card-color-2:#00f2fe;">
            <div class="health-card-icon">👁️</div>
            <h3>안과/치과/기타</h3>
            <p>백내장, 녹내장, 치주질환</p>
        </a>
    </div>
</div>
"""


def setup_driver():
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    return driver


def wp_login(driver):
    print(f"🔐 WordPress 로그인 중...")
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
        print(f"  ❌ 로그인 실패: {e}")
        return False


def check_homepage_settings(driver):
    """현재 홈페이지 설정 확인"""
    print("🔍 현재 홈페이지 설정 확인 중...\n")
    
    try:
        driver.get(f"{WP_ADMIN_URL}options-reading.php")
        time.sleep(2)
        
        # 현재 설정 확인
        try:
            posts_radio = driver.find_element(By.ID, "show_on_front_posts")
            page_radio = driver.find_element(By.ID, "page_on_front_radio")
            
            if posts_radio.is_selected():
                print("  ℹ️ 현재 설정: 최신 글 표시 (블로그)")
            elif page_radio.is_selected():
                print("  ℹ️ 현재 설정: 정적 페이지")
                try:
                    front_page_select = driver.find_element(By.ID, "page_on_front")
                    selected_option = front_page_select.find_element(By.CSS_SELECTOR, "option:checked")
                    print(f"  📄 프론트 페이지: {selected_option.text}")
                except:
                    pass
        except Exception as e:
            print(f"  ⚠️ 설정 확인 실패: {e}")
        
        return True
    except Exception as e:
        print(f"  ❌ 오류: {e}")
        return False


def find_or_create_homepage(driver):
    """홈 페이지 찾기 또는 생성"""
    print("\n📄 홈 페이지 찾는 중...\n")
    
    try:
        driver.get(f"{WP_ADMIN_URL}edit.php?post_type=page")
        time.sleep(2)
        
        # "홈" 페이지 찾기
        try:
            # 여러 가능한 이름으로 검색
            for page_name in ['홈', 'Home', '메인', 'Main']:
                try:
                    home_link = driver.find_element(By.XPATH, f"//a[contains(@class, 'row-title') and text()='{page_name}']")
                    print(f"  ✓ '{page_name}' 페이지 발견!")
                    edit_url = home_link.get_attribute('href')
                    return edit_url, page_name
                except:
                    continue
            
            # 페이지가 없으면 생성
            print("  ℹ️ 홈 페이지가 없습니다. 새로 생성합니다...")
            driver.get(f"{WP_ADMIN_URL}post-new.php?post_type=page")
            time.sleep(3)
            return None, "홈"
            
        except Exception as e:
            print(f"  ⚠️ 페이지 검색 중 오류: {e}")
            return None, "홈"
            
    except Exception as e:
        print(f"  ❌ 오류: {e}")
        return None, None


def update_page_content(driver, edit_url, page_name):
    """페이지 콘텐츠 업데이트"""
    print(f"\n✏️ '{page_name}' 페이지 업데이트 중...\n")
    
    try:
        if edit_url:
            driver.get(edit_url)
        # 이미 새 페이지 생성 화면에 있음
        
        time.sleep(3)
        
        # 페이지 제목 입력 (새 페이지인 경우)
        if not edit_url:
            try:
                # Gutenberg 편집기에서 제목 입력
                title_selectors = [
                    ".editor-post-title__input",
                    "#post-title-0",
                    "h1[aria-label*='제목']",
                    ".wp-block-post-title"
                ]
                
                for selector in title_selectors:
                    try:
                        title_field = driver.find_element(By.CSS_SELECTOR, selector)
                        title_field.clear()
                        title_field.send_keys(page_name)
                        print(f"  ✓ 페이지 제목 입력: {page_name}")
                        time.sleep(1)
                        break
                    except:
                        continue
            except Exception as e:
                print(f"  ⚠️ 제목 입력 건너뜀: {e}")
        
        # 코드 편집기로 전환
        print("  📝 코드 편집기로 전환 중...")
        try:
            # 도구 더보기 버튼 클릭
            more_buttons = [
                "button[aria-label='도구 더 보기']",
                "button[aria-label='More tools & options']",
                ".edit-post-more-menu button",
                ".interface-more-menu-dropdown button"
            ]
            
            for selector in more_buttons:
                try:
                    more_btn = driver.find_element(By.CSS_SELECTOR, selector)
                    driver.execute_script("arguments[0].click();", more_btn)
                    time.sleep(1)
                    print("  ✓ 도구 메뉴 열림")
                    break
                except:
                    continue
            
            # 코드 편집기 버튼 클릭
            time.sleep(1)
            code_editor_buttons = [
                "//button[contains(text(), '코드 편집기')]",
                "//button[contains(text(), 'Code editor')]",
                "//button[contains(@class, 'edit-post-more-menu__content')]//span[contains(text(), '코드')]/..",
                ".components-menu-item__button[role='menuitem']"
            ]
            
            for xpath in code_editor_buttons:
                try:
                    if xpath.startswith("//"):
                        code_btn = driver.find_element(By.XPATH, xpath)
                    else:
                        code_btn = driver.find_element(By.CSS_SELECTOR, xpath)
                    driver.execute_script("arguments[0].click();", code_btn)
                    time.sleep(2)
                    print("  ✓ 코드 편집기 모드 활성화")
                    break
                except:
                    continue
            
            # 코드 편집기에 HTML 입력
            editor_selectors = [
                ".editor-post-text-editor",
                "textarea.editor-post-text-editor",
                ".edit-post-text-editor__body textarea"
            ]
            
            for selector in editor_selectors:
                try:
                    editor = driver.find_element(By.CSS_SELECTOR, selector)
                    # 기존 내용 지우고 새 HTML 입력
                    driver.execute_script("arguments[0].value = '';", editor)
                    driver.execute_script("arguments[0].value = arguments[1];", editor, HOMEPAGE_HTML)
                    print("  ✓ HTML 콘텐츠 주입 완료")
                    time.sleep(1)
                    break
                except:
                    continue
            
        except Exception as e:
            print(f"  ❌ 코드 편집기 전환 실패: {e}")
            print("  💡 수동으로 다음 HTML을 복사해서 페이지에 붙여넣으세요:")
            print("\n" + "="*60)
            print(HOMEPAGE_HTML[:500] + "...")
            print("="*60 + "\n")
            return False
        
        # 페이지 발행/업데이트
        print("  💾 페이지 저장 중...")
        try:
            # 발행/업데이트 버튼 찾기
            publish_selectors = [
                ".editor-post-publish-panel__toggle",
                ".editor-post-publish-button",
                "button.editor-post-publish-button__button"
            ]
            
            for selector in publish_selectors:
                try:
                    publish_btn = driver.find_element(By.CSS_SELECTOR, selector)
                    driver.execute_script("arguments[0].click();", publish_btn)
                    time.sleep(2)
                    
                    # 최종 발행 확인 버튼이 있다면 클릭
                    try:
                        final_btn = driver.find_element(By.CSS_SELECTOR, ".editor-post-publish-button")
                        driver.execute_script("arguments[0].click();", final_btn)
                        time.sleep(2)
                    except:
                        pass
                    
                    print("  ✅ 페이지 저장 완료!")
                    return True
                except:
                    continue
                    
            print("  ⚠️ 저장 버튼을 찾을 수 없습니다")
            return False
            
        except Exception as e:
            print(f"  ⚠️ 저장 중 오류: {e}")
            return False
            
    except Exception as e:
        print(f"  ❌ 페이지 업데이트 실패: {e}")
        return False


def set_as_homepage(driver, page_name):
    """페이지를 홈페이지로 설정"""
    print(f"\n🏠 '{page_name}' 페이지를 홈페이지로 설정 중...\n")
    
    try:
        driver.get(f"{WP_ADMIN_URL}options-reading.php")
        time.sleep(2)
        
        # 정적 페이지 옵션 선택
        try:
            page_radio = driver.find_element(By.ID, "page_on_front_radio")
            driver.execute_script("arguments[0].click();", page_radio)
            time.sleep(1)
            print("  ✓ 정적 페이지 옵션 선택")
        except Exception as e:
            print(f"  ⚠️ 라디오 버튼 선택 실패: {e}")
        
        # 프론트 페이지 선택
        try:
            front_page_select = driver.find_element(By.ID, "page_on_front")
            # 페이지 이름으로 옵션 찾기
            page_option = driver.find_element(By.XPATH, f"//select[@id='page_on_front']/option[contains(text(), '{page_name}')]")
            driver.execute_script("arguments[0].selected = true;", page_option)
            time.sleep(1)
            print(f"  ✓ '{page_name}' 페이지를 프론트 페이지로 선택")
        except Exception as e:
            print(f"  ⚠️ 프론트 페이지 선택 실패: {e}")
        
        # 저장
        try:
            save_btn = driver.find_element(By.ID, "submit")
            driver.execute_script("arguments[0].click();", save_btn)
            time.sleep(2)
            print("  ✅ 설정 저장 완료!")
            return True
        except Exception as e:
            print(f"  ⚠️ 저장 실패: {e}")
            return False
            
    except Exception as e:
        print(f"  ❌ 홈페이지 설정 실패: {e}")
        return False


def main():
    print("\n" + "="*60)
    print("🎨 워드프레스 홈페이지 완전 수정")
    print("="*60 + "\n")
    
    driver = setup_driver()
    
    try:
        if not wp_login(driver):
            print("❌ 로그인 실패")
            return
        
        # 현재 설정 확인
        check_homepage_settings(driver)
        
        # 홈 페이지 찾기 또는 생성
        edit_url, page_name = find_or_create_homepage(driver)
        
        if page_name:
            # 페이지 콘텐츠 업데이트
            if update_page_content(driver, edit_url, page_name):
                # 홈페이지로 설정
                set_as_homepage(driver, page_name)
                
                print("\n" + "="*60)
                print("✨ 완료!")
                print("="*60)
                print(f"\n🌐 사이트 확인: {WP_BASE_URL}")
                print("\n💡 7개의 카테고리 카드가 메인 화면에 표시됩니다!")
        else:
            print("\n❌ 페이지를 찾을 수 없습니다")
        
    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
    finally:
        time.sleep(3)
        driver.quit()


if __name__ == "__main__":
    main()

