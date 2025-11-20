import os
import re
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 수정할 파일 목록
FILES_TO_FIX = [
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
    "news-main.html",
]

# 표준 헤더 HTML (index-v2.html 기준)
STANDARD_HEADER = """    <header class="main-header">
        <div class="header-content">
            <a href="index-v2.html" class="logo-container">
                <img src="https://health9988234.mycafe24.com/wp-content/uploads/2025/11/cropped-1-1.png" 
                     alt="9988 건강 연구소" 
                     class="logo-image">
                <span class="logo-text">9988 건강 연구소</span>
            </a>
            
            <nav class="main-nav" id="mainNav">
                <a href="index-v2.html" class="nav-item">질환별 정보</a>
                <a href="food-main.html" class="nav-item">식단/음식</a>
                <a href="exercise-main.html" class="nav-item">운동/활동</a>
                <a href="lifestyle-main.html" class="nav-item">생활습관</a>
                <a href="news-main.html" class="nav-item">건강News</a>
            </nav>
            
            <button class="mobile-menu-btn" id="mobileMenuBtn">☰</button>
        </div>
    </header>"""


def extract_header_section(content):
    """헤더 섹션 추출"""
    # <header class="main-header">부터 </header>까지
    pattern = r'(<header class="main-header">.*?</header>)'
    match = re.search(pattern, content, re.DOTALL)
    if match:
        return match.group(1)
    return None


def fix_header_in_file(filepath):
    """파일의 헤더를 표준 헤더로 교체"""
    if not os.path.exists(filepath):
        print(f"  ⚠️ 파일 없음: {filepath}")
        return False
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 기존 헤더 찾기
        header_pattern = r'(<header class="main-header">.*?</header>)'
        match = re.search(header_pattern, content, re.DOTALL)
        
        if match:
            # 헤더 교체
            content = re.sub(header_pattern, STANDARD_HEADER, content, flags=re.DOTALL)
            
            # 로고 텍스트 스타일이 없으면 추가 (logo-text 클래스용)
            if '.logo-text' not in content:
                # </style> 태그 앞에 logo-text 스타일 추가
                logo_text_style = """
        .logo-text {
            color: white;
            font-size: 24px;
            font-weight: 800;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        }
"""
                content = re.sub(r'(</style>)', logo_text_style + r'\1', content)
            
            if content != original_content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"  ✅ {filepath} - 헤더 수정 완료")
                return True
            else:
                print(f"  ℹ️ {filepath} - 이미 올바른 헤더")
                return False
        else:
            print(f"  ⚠️ {filepath} - 헤더를 찾을 수 없음")
            return False
            
    except Exception as e:
        print(f"  ❌ {filepath} - 오류: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """메인 실행"""
    print("=" * 60)
    print("🔧 모든 파일의 헤더 링크 통일")
    print("=" * 60)
    print("\n💡 index-v2.html의 헤더를 기준으로")
    print("   모든 파일의 헤더를 동일하게 수정합니다.\n")
    
    print("📝 파일 수정 중...\n")
    fixed_files = []
    
    for file in FILES_TO_FIX:
        if fix_header_in_file(file):
            fixed_files.append(file)
    
    print(f"\n✅ 총 {len(fixed_files)}개 파일 수정 완료!")
    
    print("\n" + "=" * 60)
    print("✅ 수정 완료!")
    print("=" * 60)
    print("\n💡 모든 파일의 헤더가 동일하게 수정되었습니다:")
    print("   - 로고: index-v2.html로 링크")
    print("   - 질환별 정보: index-v2.html")
    print("   - 식단/음식: food-main.html")
    print("   - 운동/활동: exercise-main.html")
    print("   - 생활습관: lifestyle-main.html")
    print("   - 건강News: news-main.html")
    print("=" * 60)


if __name__ == "__main__":
    main()
