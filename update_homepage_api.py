import sys
import io
import time
import requests
import json
import base64

# UTF-8 인코딩 설정 (Windows 콘솔 지원)
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# ---------------------------------------------------------
# ✅ 설정 변수
# ---------------------------------------------------------
WP_BASE_URL = "https://health9988234.mycafe24.com"
WP_API_URL = f"{WP_BASE_URL}/wp-json/wp/v2"
WP_USER = "health9988234"
WP_PASSWORD = "ssurlf7904!"

# ---------------------------------------------------------
# 🎨 홈페이지 HTML 콘텐츠
# ---------------------------------------------------------
HOMEPAGE_HTML = """
<!-- wp:html -->
<style>
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

/* 페이지 제목 숨기기 */
.entry-title, .page-title, h1.entry-title {
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
        <a href="{base_url}/category/질환별-정보/심혈관-질환/" class="health-card" style="--card-color-1:#FF6B6B; --card-color-2:#EE5A6F;">
            <div class="health-card-icon">❤️</div>
            <h3>심혈관 질환</h3>
            <p>고혈압, 심근경색, 동맥경화</p>
        </a>
        
        <a href="{base_url}/category/질환별-정보/당뇨병/" class="health-card" style="--card-color-1:#4ECDC4; --card-color-2:#44A08D;">
            <div class="health-card-icon">💉</div>
            <h3>당뇨병</h3>
            <p>혈당관리, 공복혈당, 합병증</p>
        </a>
        
        <a href="{base_url}/category/질환별-정보/관절-근골격계-질환/" class="health-card" style="--card-color-1:#A18CD1; --card-color-2:#FBC2EB;">
            <div class="health-card-icon">🦴</div>
            <h3>관절/근골격계 질환</h3>
            <p>관절염, 허리디스크, 골다공증</p>
        </a>
        
        <a href="{base_url}/category/질환별-정보/호르몬-내분비-질환/" class="health-card" style="--card-color-1:#FA709A; --card-color-2:#FEE140;">
            <div class="health-card-icon">🌡️</div>
            <h3>호르몬/내분비 질환</h3>
            <p>갱년기, 갑상선, 대사증후군</p>
        </a>
        
        <a href="{base_url}/category/질환별-정보/정신-건강-신경계/" class="health-card" style="--card-color-1:#667eea; --card-color-2:#764ba2;">
            <div class="health-card-icon">🧠</div>
            <h3>정신 건강/신경계</h3>
            <p>우울증, 치매, 수면장애</p>
        </a>
        
        <a href="{base_url}/category/질환별-정보/소화기-질환/" class="health-card" style="--card-color-1:#f093fb; --card-color-2:#f5576c;">
            <div class="health-card-icon">🍽️</div>
            <h3>소화기 질환</h3>
            <p>위염, 지방간, 역류성 식도염</p>
        </a>
        
        <a href="{base_url}/category/질환별-정보/안과-치과-기타/" class="health-card" style="--card-color-1:#4facfe; --card-color-2:#00f2fe;">
            <div class="health-card-icon">👁️</div>
            <h3>안과/치과/기타</h3>
            <p>백내장, 녹내장, 치주질환</p>
        </a>
    </div>
</div>
<!-- /wp:html -->
""".replace("{base_url}", WP_BASE_URL)


def get_auth_header():
    """인증 헤더 생성"""
    credentials = f"{WP_USER}:{WP_PASSWORD}"
    token = base64.b64encode(credentials.encode()).decode('utf-8')
    return {
        'Authorization': f'Basic {token}',
        'Content-Type': 'application/json'
    }


def get_pages():
    """모든 페이지 가져오기"""
    print("📄 페이지 목록 조회 중...")
    try:
        response = requests.get(
            f"{WP_API_URL}/pages",
            headers=get_auth_header()
        )
        if response.status_code == 200:
            pages = response.json()
            print(f"  ✓ {len(pages)}개의 페이지 발견")
            return pages
        else:
            print(f"  ❌ 페이지 조회 실패: {response.status_code}")
            print(f"  응답: {response.text}")
            return []
    except Exception as e:
        print(f"  ❌ 오류: {e}")
        return []


def create_or_update_homepage():
    """홈페이지 생성 또는 업데이트"""
    print("\n" + "="*60)
    print("🏠 워드프레스 홈페이지 설정")
    print("="*60 + "\n")
    
    # 기존 페이지 확인
    pages = get_pages()
    home_page = None
    
    for page in pages:
        if page['title']['rendered'] == '홈':
            home_page = page
            print(f"  ✓ 기존 '홈' 페이지 발견 (ID: {page['id']})")
            break
    
    # 페이지 데이터 준비
    page_data = {
        'title': '홈',
        'content': HOMEPAGE_HTML,
        'status': 'publish'
    }
    
    try:
        if home_page:
            # 기존 페이지 업데이트
            print("\n📝 기존 페이지 업데이트 중...")
            response = requests.post(
                f"{WP_API_URL}/pages/{home_page['id']}",
                headers=get_auth_header(),
                json=page_data
            )
        else:
            # 새 페이지 생성
            print("\n✨ 새 페이지 생성 중...")
            response = requests.post(
                f"{WP_API_URL}/pages",
                headers=get_auth_header(),
                json=page_data
            )
        
        if response.status_code in [200, 201]:
            page_result = response.json()
            print(f"  ✅ 페이지 생성/업데이트 완료! (ID: {page_result['id']})")
            return page_result['id']
        else:
            print(f"  ❌ 실패: {response.status_code}")
            print(f"  응답: {response.text}")
            return None
            
    except Exception as e:
        print(f"  ❌ 오류: {e}")
        return None


def set_as_front_page(page_id):
    """페이지를 프론트 페이지로 설정"""
    print("\n⚙️ 프론트 페이지 설정 중...")
    
    try:
        # show_on_front 설정
        response1 = requests.post(
            f"{WP_API_URL}/settings",
            headers=get_auth_header(),
            json={
                'show_on_front': 'page',
                'page_on_front': page_id
            }
        )
        
        if response1.status_code == 200:
            print("  ✅ 프론트 페이지 설정 완료!")
            return True
        else:
            print(f"  ⚠️ 프론트 페이지 설정 실패: {response1.status_code}")
            print(f"  응답: {response1.text}")
            print("\n  📌 수동 설정 방법:")
            print("     1. WordPress 관리자 > 설정 > 읽기")
            print("     2. '홈페이지 표시' > '정적 페이지' 선택")
            print("     3. '홈페이지' 드롭다운에서 '홈' 선택")
            print("     4. '변경사항 저장' 클릭")
            return False
            
    except Exception as e:
        print(f"  ❌ 오류: {e}")
        return False


def main():
    """메인 실행"""
    print("\n" + "="*60)
    print("🎨 워드프레스 홈페이지 자동 생성 (REST API)")
    print("="*60 + "\n")
    
    # 홈페이지 생성/업데이트
    page_id = create_or_update_homepage()
    
    if page_id:
        # 프론트 페이지로 설정
        set_as_front_page(page_id)
        
        print("\n" + "="*60)
        print("✨ 모든 작업 완료!")
        print("="*60)
        print(f"\n🌐 사이트 확인: {WP_BASE_URL}")
        print("\n💡 팁: 메인 화면에 7개의 카테고리 카드가 표시됩니다!")
    else:
        print("\n❌ 홈페이지 생성/업데이트 실패")


if __name__ == "__main__":
    main()

