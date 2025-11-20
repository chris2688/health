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

# 전역 CSS 스타일 (모든 카테고리 페이지에 적용)
GLOBAL_CATEGORY_CSS = """
<style>
/* 카테고리 아카이브 페이지 전체 스타일 */
.archive .site-main,
.category .site-main {
    max-width: 1400px;
    margin: 0 auto;
    padding: 40px 20px;
}

/* 카테고리 헤더 스타일 */
.archive .page-header,
.category .page-header {
    text-align: center;
    margin-bottom: 50px;
    padding: 40px 20px;
    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    border-radius: 20px;
}

.page-header .page-title {
    font-size: 42px;
    font-weight: 800;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0;
}

/* 카테고리 설명 숨기기 (우리가 커스텀 HTML 넣을 거라) */
.archive-description {
    margin-top: 15px;
    color: #666;
    font-size: 16px;
}

/* 글 목록을 앱 아이콘 스타일 그리드로 */
.archive .site-main article,
.category .site-main article {
    margin: 0 !important;
}

.archive .posts-container,
.category .posts-container {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 25px;
    max-width: 1200px;
    margin: 0 auto;
}

/* 개별 글 카드 스타일 (앱 아이콘 형태) */
.archive article.post,
.category article.post {
    position: relative;
    background: #ffffff;
    border-radius: 20px;
    overflow: hidden;
    box-shadow: 0 8px 25px rgba(0,0,0,0.1);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    cursor: pointer;
    display: flex;
    flex-direction: column;
    height: 100%;
}

.archive article.post:hover,
.category article.post:hover {
    transform: translateY(-8px);
    box-shadow: 0 15px 35px rgba(0,0,0,0.15);
}

/* 썸네일을 앱 아이콘처럼 */
.post-thumbnail {
    position: relative;
    width: 100%;
    padding-top: 100%; /* 1:1 정사각형 */
    overflow: hidden;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.post-thumbnail img {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform 0.3s ease;
}

.archive article.post:hover .post-thumbnail img,
.category article.post:hover .post-thumbnail img {
    transform: scale(1.1);
}

/* 썸네일이 없는 경우 기본 아이콘 */
.post-thumbnail:empty::before {
    content: '📄';
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    font-size: 80px;
    opacity: 0.3;
}

/* 글 제목 및 내용 */
.entry-header {
    padding: 20px;
    flex: 1;
    display: flex;
    flex-direction: column;
}

.entry-title {
    font-size: 18px;
    font-weight: 700;
    line-height: 1.4;
    margin: 0 0 10px 0;
    color: #2c3e50;
}

.entry-title a {
    text-decoration: none;
    color: inherit;
    transition: color 0.3s;
}

.entry-title a:hover {
    color: #667eea;
}

.entry-meta {
    font-size: 13px;
    color: #7f8c8d;
    margin-bottom: 10px;
}

.entry-summary,
.entry-content {
    font-size: 14px;
    color: #555;
    line-height: 1.6;
    display: -webkit-box;
    -webkit-line-clamp: 3;
    -webkit-box-orient: vertical;
    overflow: hidden;
}

/* 더보기 버튼 숨기기 */
.more-link {
    display: none;
}

/* 페이지네이션 스타일 */
.pagination {
    margin-top: 50px;
    text-align: center;
}

.pagination .nav-links {
    display: flex;
    justify-content: center;
    gap: 10px;
    flex-wrap: wrap;
}

.pagination a,
.pagination span {
    padding: 10px 15px;
    background: #ffffff;
    border-radius: 10px;
    text-decoration: none;
    color: #667eea;
    font-weight: 600;
    box-shadow: 0 2px 10px rgba(0,0,0,0.08);
    transition: all 0.3s;
}

.pagination a:hover {
    background: #667eea;
    color: #ffffff;
    transform: translateY(-2px);
}

.pagination .current {
    background: #667eea;
    color: #ffffff;
}

/* 모바일 반응형 (좁은 화면은 1열) */
@media (max-width: 640px) {
    .archive .posts-container,
    .category .posts-container {
        grid-template-columns: 1fr;
        gap: 20px;
    }
    
    .page-header .page-title {
        font-size: 28px;
    }
    
    .entry-title {
        font-size: 16px;
    }
}

/* 태블릿 반응형 (2열 유지) */
@media (min-width: 641px) and (max-width: 1024px) {
    .archive .posts-container,
    .category .posts-container {
        grid-template-columns: repeat(2, 1fr);
    }
}

/* 서브 카테고리 목록도 앱 아이콘 스타일로 */
.category-list-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 25px;
    max-width: 1200px;
    margin: 40px auto;
}

.category-card {
    position: relative;
    padding: 40px 30px;
    border-radius: 24px;
    background: linear-gradient(135deg, var(--card-color-1, #667eea) 0%, var(--card-color-2, #764ba2) 100%);
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
}

.category-card:hover {
    transform: translateY(-8px) scale(1.02);
    box-shadow: 0 20px 40px rgba(0,0,0,0.25);
}

.category-card::before {
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

.category-card-icon {
    font-size: 64px;
    margin-bottom: 20px;
    filter: drop-shadow(0 2px 4px rgba(0,0,0,0.2));
}

.category-card h3 {
    font-size: 24px;
    font-weight: 700;
    color: #ffffff;
    margin: 0 0 10px 0;
    text-shadow: 0 2px 4px rgba(0,0,0,0.1);
    position: relative;
    z-index: 1;
}

.category-card p {
    font-size: 14px;
    color: rgba(255,255,255,0.9);
    margin: 0;
    position: relative;
    z-index: 1;
}

@media (max-width: 640px) {
    .category-list-grid {
        grid-template-columns: 1fr;
    }
}
</style>
"""


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


def add_global_css_to_theme():
    """
    테마의 추가 CSS에 전역 스타일 추가
    WordPress 관리자 > 외모 > 사용자 정의하기 > 추가 CSS
    """
    print("\n📝 전역 CSS를 추가하는 방법:")
    print("=" * 60)
    print("1. WordPress 관리자 페이지 접속")
    print("2. '외모' > '사용자 정의하기' 메뉴 클릭")
    print("3. '추가 CSS' 섹션 클릭")
    print("4. 아래 CSS 코드를 복사해서 붙여넣기")
    print("5. '공개' 버튼 클릭")
    print("=" * 60)
    print("\n💾 복사할 CSS 코드:")
    print(GLOBAL_CATEGORY_CSS)


def inject_css_via_customizer(driver):
    """
    WordPress Customizer를 통해 CSS 주입 시도
    """
    print("\n--- 🎨 전역 CSS 주입 시작 ---")
    
    try:
        # Customizer 페이지로 이동
        driver.get(f"{WP_ADMIN_URL}customize.php")
        time.sleep(5)
        print("  ⏳ Customizer 로딩 중...")
        
        # iframe으로 전환
        try:
            iframe = driver.find_element(By.ID, "customize-preview")
            driver.switch_to.frame(iframe)
            driver.switch_to.default_content()
        except:
            pass
        
        # 추가 CSS 버튼 찾기 및 클릭
        try:
            css_button = driver.find_element(By.CSS_SELECTOR, "#accordion-section-custom_css")
            driver.execute_script("arguments[0].click();", css_button)
            time.sleep(2)
            print("  ✓ 추가 CSS 섹션 열기")
        except Exception as e:
            print(f"  ⚠️ 추가 CSS 버튼을 찾을 수 없습니다: {e}")
            print("  → 수동으로 추가해주세요.")
            return False
        
        # CSS 입력 필드 찾기
        try:
            css_textarea = driver.find_element(By.ID, "custom_css")
            current_css = css_textarea.get_attribute("value")
            new_css = current_css + "\n\n" + GLOBAL_CATEGORY_CSS
            driver.execute_script("arguments[0].value = arguments[1];", css_textarea, new_css)
            time.sleep(2)
            print("  ✓ CSS 코드 주입 완료")
        except Exception as e:
            print(f"  ⚠️ CSS 입력 필드를 찾을 수 없습니다: {e}")
            return False
        
        # 공개 버튼 클릭
        try:
            publish_button = driver.find_element(By.ID, "save")
            driver.execute_script("arguments[0].click();", publish_button)
            time.sleep(3)
            print("  ✅ CSS 저장 완료!")
            return True
        except Exception as e:
            print(f"  ⚠️ 공개 버튼 클릭 실패: {e}")
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
    
    # CSS 주입 시도
    success = inject_css_via_customizer(driver)
    
    if not success:
        print("\n⚠️ 자동 주입 실패. 수동으로 CSS를 추가해주세요:")
        add_global_css_to_theme()
    
    print("\n" + "="*60)
    print("📋 추가 작업 필요:")
    print("="*60)
    print("1. functions.php에 posts_container 클래스 추가")
    print("2. 또는 테마의 archive.php 수정")
    print("\n아래 코드를 functions.php에 추가:")
    print("""
add_filter('post_class', 'custom_post_class');
function custom_post_class($classes) {
    $classes[] = 'post';
    return $classes;
}

add_action('genesis_before_loop', 'wrap_posts_in_container');
function wrap_posts_in_container() {
    if (is_archive() || is_category()) {
        echo '<div class="posts-container">';
    }
}

add_action('genesis_after_loop', 'close_posts_container');
function close_posts_container() {
    if (is_archive() || is_category()) {
        echo '</div>';
    }
}
""")
    
    driver.quit()


if __name__ == "__main__":
    main()

