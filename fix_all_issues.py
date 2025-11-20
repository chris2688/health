import os
import re
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 서브 카테고리 매핑 (카테고리명 -> sub-파일명)
SUB_CATEGORY_MAPPING = {
    '고혈압': 'sub-고혈압.html',
    '고지혈증-콜레스테롤': 'sub-고지혈증.html',
    '협심증-심근경색': 'sub-협심증심근경색.html',
    '동맥경화': 'sub-동맥경화.html',
    '뇌졸중': 'sub-뇌졸중.html',
}

# 수정할 파일 목록
ALL_FILES = [
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
    "food-피해야할과일.html",
    "food-질환별식단.html",
    "food-모르면독이된다.html",
    "exercise-질환별운동가이드.html",
    "exercise-운동팁.html",
    "lifestyle-생활습관.html",
    "lifestyle-생활습관바꾸기팁.html",
]

# index-v2.html의 헤더 구조
CORRECT_HEADER = '''    <!-- 헤더 -->
    <header class="main-header">
        <div class="header-content">
            <a href="index-v2.html" class="logo-container">
                <img src="https://health9988234.mycafe24.com/wp-content/uploads/2025/11/cropped-1-1.png" 
                     alt="9988 건강 연구소" 
                     class="logo-image">
            </a>
            
            <nav class="main-nav" id="mainNav">
                <button class="mobile-close-btn" id="mobileCloseBtn">✕</button>
                <a href="index-v2.html" class="nav-item">질환별 정보</a>
                <a href="food-main.html" class="nav-item">식단/음식</a>
                <a href="exercise-main.html" class="nav-item">운동/활동</a>
                <a href="lifestyle-main.html" class="nav-item">생활습관</a>
                <a href="news-main.html" class="nav-item">건강News</a>
            </nav>
            
            <button class="mobile-menu-btn" id="mobileMenuBtn">☰</button>
        </div>
    </header>'''


def fix_sub_category_links(filepath):
    """서브 카테고리 링크 수정"""
    if not os.path.exists(filepath):
        return False
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # data-category와 onclick을 사용하는 링크를 sub-*.html로 변경
        # 패턴: <a href="#" data-category="고혈압" onclick="loadCategoryPosts('고혈압'); return false;"
        pattern = r'<a href="#" data-category="([^"]+)" onclick="loadCategoryPosts\([^)]+\); return false;"'
        
        def replace_link(match):
            category = match.group(1)
            # sub- 파일명 찾기
            sub_file = SUB_CATEGORY_MAPPING.get(category, f'sub-{category}.html')
            return f'<a href="{sub_file}"'
        
        content = re.sub(pattern, replace_link, content)
        
        # 빈 data-category도 처리
        content = re.sub(
            r'<a href="#" data-category="" onclick="loadCategoryPosts\(\'\'\); return false;"',
            r'<a href="#"',
            content
        )
        
        return content != original_content, content
        
    except Exception as e:
        print(f"  ❌ {filepath} - 오류: {e}")
        return False, None


def fix_header(filepath):
    """헤더를 index-v2.html과 동일하게 수정"""
    if not os.path.exists(filepath):
        return False
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 기존 헤더 찾기 및 교체
        header_pattern = r'<header class="main-header">.*?</header>'
        header_match = re.search(header_pattern, content, re.DOTALL)
        
        if header_match:
            # 헤더 교체
            content = content.replace(header_match.group(0), CORRECT_HEADER)
        
        return content != original_content, content
        
    except Exception as e:
        print(f"  ❌ {filepath} - 오류: {e}")
        return False, None


def fix_back_button_css(filepath):
    """뒤로가기 버튼 CSS 수정"""
    if not os.path.exists(filepath):
        return False
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # .back-button CSS가 있는지 확인
        if '.back-button' not in content:
            # CSS 추가 (</style> 전에)
            back_button_css = '''
        /* ========== 뒤로가기 버튼 ========== */
        .back-button {
            display: inline-block;
            padding: 12px 24px;
            margin: 20px 0;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            text-decoration: none;
            border-radius: 8px;
            font-weight: 600;
            font-size: 16px;
            transition: all 0.3s;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        }
        
        .back-button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
            background: rgba(102, 126, 234, 0.2);
        }
        
        .back-button::before {
            content: '← ';
            margin-right: 5px;
        }
'''
            content = re.sub(r'(</style>)', back_button_css + r'\1', content, count=1)
        
        return content != original_content, content
        
    except Exception as e:
        print(f"  ❌ {filepath} - 오류: {e}")
        return False, None


def fix_news_main_link(filepath):
    """건강News 링크 확인 및 수정"""
    if not os.path.exists(filepath):
        return False
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # news-main.html 링크 확인
        content = re.sub(
            r'href="https://health9988234\.mycafe24\.com/news-main\.html"',
            'href="news-main.html"',
            content
        )
        content = re.sub(
            r'href="https://health9988234\.mycafe24\.com/category/건강-new/"',
            'href="news-main.html"',
            content
        )
        
        return content != original_content, content
        
    except Exception as e:
        print(f"  ❌ {filepath} - 오류: {e}")
        return False, None


def main():
    """메인 실행"""
    print("=" * 60)
    print("🔧 모든 문제 수정")
    print("=" * 60)
    print("\n💡 수정 사항:")
    print("   1. 서브 카테고리 링크 수정 (sub-*.html)")
    print("   2. 헤더 통일 (index-v2.html 기준)")
    print("   3. 뒤로가기 버튼 CSS 추가")
    print("   4. 건강News 링크 확인\n")
    
    print("📝 파일 수정 중...\n")
    
    fixed_count = 0
    
    for file in ALL_FILES:
        changed = False
        content = None
        
        # 1. 서브 카테고리 링크 수정 (category 파일만)
        if file.startswith('category-'):
            sub_changed, content = fix_sub_category_links(file)
            if sub_changed and content:
                changed = True
                with open(file, 'w', encoding='utf-8') as f:
                    f.write(content)
        
        # 2. 헤더 통일
        if not content:
            with open(file, 'r', encoding='utf-8') as f:
                content = f.read()
        
        header_changed, content = fix_header(file)
        if header_changed and content:
            changed = True
            with open(file, 'w', encoding='utf-8') as f:
                f.write(content)
        
        # 3. 뒤로가기 버튼 CSS (category 파일만)
        if file.startswith('category-'):
            if not content:
                with open(file, 'r', encoding='utf-8') as f:
                    content = f.read()
            
            css_changed, content = fix_back_button_css(file)
            if css_changed and content:
                changed = True
                with open(file, 'w', encoding='utf-8') as f:
                    f.write(content)
        
        # 4. 건강News 링크
        if not content:
            with open(file, 'r', encoding='utf-8') as f:
                content = f.read()
        
        news_changed, content = fix_news_main_link(file)
        if news_changed and content:
            changed = True
            with open(file, 'w', encoding='utf-8') as f:
                f.write(content)
        
        if changed:
            print(f"  ✅ {file} - 수정 완료")
            fixed_count += 1
        else:
            print(f"  ℹ️ {file} - 변경사항 없음")
    
    print(f"\n✅ 총 {fixed_count}개 파일 수정 완료!")
    print("=" * 60)


if __name__ == "__main__":
    main()

