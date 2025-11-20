import os
import re
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

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


def fix_header_structure(filepath):
    """헤더 구조 수정"""
    if not os.path.exists(filepath):
        print(f"  ⚠️ 파일 없음: {filepath}")
        return False
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 1. nav 안에 mobile-menu-btn이 있으면 밖으로 이동
        # 패턴: <nav>...<button class="mobile-menu-btn">...</button></nav>
        nav_pattern = r'(<nav class="main-nav" id="mainNav">.*?)(<button class="mobile-menu-btn"[^>]*>☰</button>)(.*?</nav>)'
        
        def fix_nav(match):
            nav_start = match.group(1)
            mobile_btn = match.group(2)
            nav_end = match.group(3)
            # mobile-menu-btn을 nav 밖으로 이동
            return nav_start + nav_end + '\n            ' + mobile_btn
        
        content = re.sub(nav_pattern, fix_nav, content, flags=re.DOTALL)
        
        # 2. nav가 제대로 닫혀있는지 확인
        # nav 안에 mobile-menu-btn이 있으면 제거하고 밖으로 이동
        if '<nav class="main-nav" id="mainNav">' in content:
            nav_start_pos = content.find('<nav class="main-nav" id="mainNav">')
            nav_end_pos = content.find('</nav>', nav_start_pos)
            
            if nav_start_pos != -1 and nav_end_pos != -1:
                nav_content = content[nav_start_pos:nav_end_pos]
                
                # nav 안에 mobile-menu-btn이 있으면
                if '<button class="mobile-menu-btn"' in nav_content:
                    # nav 안의 mobile-menu-btn 제거
                    nav_content = re.sub(
                        r'<button class="mobile-menu-btn"[^>]*>☰</button>\s*',
                        '',
                        nav_content
                    )
                    
                    # nav 밖에 mobile-menu-btn 추가
                    content = content[:nav_start_pos] + nav_content + content[nav_end_pos:]
                    
                    # </nav> 다음에 mobile-menu-btn 추가
                    nav_end_pos = content.find('</nav>', nav_start_pos)
                    if nav_end_pos != -1:
                        # 이미 밖에 있으면 추가하지 않음
                        after_nav = content[nav_end_pos + 6:nav_end_pos + 100]
                        if '<button class="mobile-menu-btn"' not in after_nav:
                            mobile_btn = '\n            <button class="mobile-menu-btn" id="mobileMenuBtn">☰</button>'
                            content = content[:nav_end_pos + 6] + mobile_btn + content[nav_end_pos + 6:]
        
        # 3. 헤더 링크가 올바른지 확인
        # 모든 링크가 상대 경로인지 확인
        content = re.sub(
            r'href="https://health9988234\.mycafe24\.com/index-v2\.html"',
            'href="index-v2.html"',
            content
        )
        content = re.sub(
            r'href="https://health9988234\.mycafe24\.com/food-main\.html"',
            'href="food-main.html"',
            content
        )
        content = re.sub(
            r'href="https://health9988234\.mycafe24\.com/exercise-main\.html"',
            'href="exercise-main.html"',
            content
        )
        content = re.sub(
            r'href="https://health9988234\.mycafe24\.com/lifestyle-main\.html"',
            'href="lifestyle-main.html"',
            content
        )
        content = re.sub(
            r'href="https://health9988234\.mycafe24\.com/news-main\.html"',
            'href="news-main.html"',
            content
        )
        
        # 4. nav 링크 구조 확인 및 수정
        correct_nav = '''<nav class="main-nav" id="mainNav">
                <button class="mobile-close-btn" id="mobileCloseBtn">✕</button>
                <a href="index-v2.html" class="nav-item">질환별 정보</a>
                <a href="food-main.html" class="nav-item">식단/음식</a>
                <a href="exercise-main.html" class="nav-item">운동/활동</a>
                <a href="lifestyle-main.html" class="nav-item">생활습관</a>
                <a href="news-main.html" class="nav-item">건강News</a>
            </nav>'''
        
        # nav 내용을 올바른 구조로 교체
        nav_match = re.search(r'<nav class="main-nav" id="mainNav">.*?</nav>', content, re.DOTALL)
        if nav_match:
            current_nav = nav_match.group(0)
            # 링크만 확인하고 구조는 유지
            if 'href="index-v2.html"' in current_nav and 'href="food-main.html"' in current_nav:
                # 링크는 올바름, 구조만 확인
                pass
            else:
                # nav 내용 교체
                content = content.replace(current_nav, correct_nav)
        
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  ✅ {filepath} - 헤더 구조 수정 완료")
            return True
        else:
            print(f"  ℹ️ {filepath} - 변경사항 없음")
            return False
            
    except Exception as e:
        print(f"  ❌ {filepath} - 오류: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """메인 실행"""
    print("=" * 60)
    print("🔧 모든 파일 헤더 구조 수정")
    print("=" * 60)
    print("\n💡 수정 사항:")
    print("   1. nav 구조 정리")
    print("   2. mobile-menu-btn을 nav 밖으로 이동")
    print("   3. 헤더 링크 확인\n")
    
    print("📝 파일 수정 중...\n")
    fixed_files = []
    
    for file in ALL_FILES:
        if fix_header_structure(file):
            fixed_files.append(file)
    
    print(f"\n✅ 총 {len(fixed_files)}개 파일 수정 완료!")
    print("=" * 60)


if __name__ == "__main__":
    main()

