import sys
import io
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException

# ---------------------------------------------------------
# ✅ 설정 변수 (로그인 정보 및 워드프레스 주소)
# ---------------------------------------------------------
WP_LOGIN_URL = "https://health9988234.mycafe24.com/wp-login.php"
WP_ADMIN_URL = "https://health9988234.mycafe24.com/wp-admin/"
WP_USER = "health9988234"
WP_PASSWORD = "ssurlf7904!" # <-- 꼭 수정하세요!

# ---------------------------------------------------------
# 🎯 분류할 글 제목 목록 (사용자님이 직접 입력해주신 정답지)
# ---------------------------------------------------------
TITLE_TO_CATEGORY_MAP = {
    # 1. 질환별 정보
    "고혈압 낮추는 방법 및 관리, 예방 법": "질환별 정보",
    "협심증과 심근경색 차이점, 예방법": "질환별 정보",
    "중풍예방, 뇌졸중 전조증상, 중년 이후 절대 무시하면 안 되는 5가지 신호": "질환별 정보",
    "동맥경화증 초기 증상 검사, 예방법": "질환별 정보",
    
    # 2. 운동/활동
    "고혈압 좋은 운동 가이드, 추천": "운동/활동",
    "당뇨병에 좋은 운동 추천, 가이드": "운동/활동",
    "콜레스테롤(고지혈증) 운동 추천": "운동/활동",
    
    # 이 외의 추가해야 할 제목들을 이 목록에 계속 추가해주세요.
}

# ---------------------------------------------------------
# 기본 함수 (로그인 및 드라이버 설정)
# ---------------------------------------------------------

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

def setup_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)")
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    return driver

def wp_login(driver):
    driver.get(WP_LOGIN_URL)
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "user_login"))).send_keys(WP_USER)
        driver.find_element(By.ID, "user_pass").send_keys(WP_PASSWORD)
        driver.find_element(By.ID, "wp-submit").click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "adminmenu")))
        return True
    except:
        return False

# ---------------------------------------------------------
# 🤖 자동 분류 메인 함수
# ---------------------------------------------------------

def assign_category_by_title(driver):
    """
    제목을 검색하여 해당 글을 정확한 카테고리로 이동시킵니다.
    """
    print(f"\n--- 🎯 정확한 제목 기반 자동 분류 시작 ---")
    
    for title, target_category in TITLE_TO_CATEGORY_MAP.items():
        print(f"🔎 글 검색 중: '{title}' (목표: {target_category})")
        
        try:
            # 1. 글 목록 페이지로 이동 및 정확한 제목 검색
            driver.get(WP_ADMIN_URL + "edit.php") 
            
            search_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "post-search-input"))
            )
            search_field.clear()
            search_field.send_keys(title)
            driver.find_element(By.ID, "search-submit").click()
            time.sleep(1.5) # 검색 결과 로딩 대기

            # 2. 검색 결과가 1개 이상인지 확인
            try:
                driver.find_element(By.CLASS_NAME, "no-items")
                print(f"    ⚠ 글을 찾을 수 없습니다. (제목 오타 가능성)")
                continue 
            except NoSuchElementException:
                # 글이 있으니 계속 진행
                pass
            
            # 3. 결과 모두 선택 및 일괄 편집 적용
            select_all_checkbox = driver.find_element(By.ID, "cb-select-all-1")
            if not select_all_checkbox.is_selected():
                 driver.execute_script("arguments[0].click();", select_all_checkbox)
            
            Select(driver.find_element(By.ID, "bulk-action-selector-top")).select_by_value("edit")
            driver.find_element(By.ID, "doaction").click()
            
            # 4. 일괄 편집 박스가 완전히 열릴 때까지 대기
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "bulk-edit"))
            )
            time.sleep(1) 
            
            # 5. 원하는 카테고리 체크
            cat_xpath = f"//label[contains(text(), '{target_category}')]/input"
            cat_checkbox = driver.find_element(By.XPATH, cat_xpath)
            
            if not cat_checkbox.is_selected():
                 driver.execute_script("arguments[0].click();", cat_checkbox)
            
            # 6. '미분류' 체크 해제
            try:
                 uncat_checkbox = driver.find_element(By.ID, "in-category-1")
                 if uncat_checkbox.is_selected():
                     driver.execute_script("arguments[0].click();", uncat_checkbox)
            except:
                 pass

            # 7. 업데이트 버튼 클릭 (최종 적용)
            WebDriverWait(driver, 10).until(
                 EC.element_to_be_clickable((By.ID, "bulk_edit_apply"))
            ).click()
            
            print(f"    ✓ '{title}' -> {target_category} 이동 완료.")
            
        except Exception as e:
            print(f"    ❌ 오류 발생 또는 요소 찾기 실패: {e}")
            
    print(f"\n--- ✨ 자동 분류 작업 종료 ---")


def main():
    driver = setup_driver()
    if not wp_login(driver):
        print("❌ 로그인 실패. 사용자명/비밀번호를 확인하세요.")
        return

    # 분류할 글들을 TITLE_TO_CATEGORY_MAP에 추가한 후 실행하세요.
    assign_category_by_title(driver)

    driver.quit()

if __name__ == "__main__":
    main()