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


def fix_header_links(filepath):
    """헤더 링크 수정"""
    if not os.path.exists(filepath):
        print(f"  ⚠️ 파일 없음: {filepath}")
        return False
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 1. 모든 헤더 링크를 올바른 상대 경로로 수정
        # index-v2.html 링크
        content = re.sub(
            r'href="https://health9988234\.mycafe24\.com/index-v2\.html"',
            'href="index-v2.html"',
            content
        )
        content = re.sub(
            r'href="https://health9988234\.mycafe24\.com/"',
            'href="index-v2.html"',
            content
        )
        
        # food-main.html 링크
        content = re.sub(
            r'href="https://health9988234\.mycafe24\.com/food-main\.html"',
            'href="food-main.html"',
            content
        )
        content = re.sub(
            r'href="https://health9988234\.mycafe24\.com/category/식단-음식/"',
            'href="food-main.html"',
            content
        )
        
        # exercise-main.html 링크
        content = re.sub(
            r'href="https://health9988234\.mycafe24\.com/exercise-main\.html"',
            'href="exercise-main.html"',
            content
        )
        content = re.sub(
            r'href="https://health9988234\.mycafe24\.com/category/운동-활동/"',
            'href="exercise-main.html"',
            content
        )
        
        # lifestyle-main.html 링크
        content = re.sub(
            r'href="https://health9988234\.mycafe24\.com/lifestyle-main\.html"',
            'href="lifestyle-main.html"',
            content
        )
        content = re.sub(
            r'href="https://health9988234\.mycafe24\.com/category/생활습관/"',
            'href="lifestyle-main.html"',
            content
        )
        
        # news-main.html 링크
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
        
        # 카테고리 링크들
        content = re.sub(
            r'href="https://health9988234\.mycafe24\.com/category-심혈관질환\.html"',
            'href="category-심혈관질환.html"',
            content
        )
        content = re.sub(
            r'href="https://health9988234\.mycafe24\.com/category-당뇨병\.html"',
            'href="category-당뇨병.html"',
            content
        )
        content = re.sub(
            r'href="https://health9988234\.mycafe24\.com/category-관절근골격계\.html"',
            'href="category-관절근골격계.html"',
            content
        )
        content = re.sub(
            r'href="https://health9988234\.mycafe24\.com/category-호르몬내분비\.html"',
            'href="category-호르몬내분비.html"',
            content
        )
        content = re.sub(
            r'href="https://health9988234\.mycafe24\.com/category-정신건강신경계\.html"',
            'href="category-정신건강신경계.html"',
            content
        )
        content = re.sub(
            r'href="https://health9988234\.mycafe24\.com/category-소화기질환\.html"',
            'href="category-소화기질환.html"',
            content
        )
        content = re.sub(
            r'href="https://health9988234\.mycafe24\.com/category-안과치과기타\.html"',
            'href="category-안과치과기타.html"',
            content
        )
        
        # 2. 헤더의 nav 링크가 올바른지 확인
        # nav 안에 있는 링크들을 확인하고 수정
        nav_pattern = r'(<nav class="main-nav" id="mainNav">.*?</nav>)'
        nav_match = re.search(nav_pattern, content, re.DOTALL)
        
        if nav_match:
            nav_content = nav_match.group(1)
            
            # 올바른 링크 구조로 교체
            correct_nav = '''<nav class="main-nav" id="mainNav">
                <button class="mobile-close-btn" id="mobileCloseBtn">✕</button>
                <a href="index-v2.html" class="nav-item">질환별 정보</a>
                <a href="food-main.html" class="nav-item">식단/음식</a>
                <a href="exercise-main.html" class="nav-item">운동/활동</a>
                <a href="lifestyle-main.html" class="nav-item">생활습관</a>
                <a href="news-main.html" class="nav-item">건강News</a>
            </nav>'''
            
            content = content.replace(nav_content, correct_nav)
        
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  ✅ {filepath} - 링크 수정 완료")
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
    print("🔧 모든 파일 헤더 링크 수정")
    print("=" * 60)
    print("\n💡 수정 사항:")
    print("   1. 모든 절대 경로를 상대 경로로 변경")
    print("   2. 헤더 nav 링크 일관성 유지\n")
    
    print("📝 파일 수정 중...\n")
    fixed_files = []
    
    for file in ALL_FILES:
        if fix_header_links(file):
            fixed_files.append(file)
    
    print(f"\n✅ 총 {len(fixed_files)}개 파일 수정 완료!")
    print("=" * 60)


if __name__ == "__main__":
    main()

