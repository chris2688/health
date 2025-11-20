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


def fix_file(filepath):
    """파일 완전 수정"""
    if not os.path.exists(filepath):
        print(f"  ⚠️ 파일 없음: {filepath}")
        return False
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        original_lines = lines.copy()
        new_lines = []
        i = 0
        
        while i < len(lines):
            line = lines[i]
            
            # 빈 CSS 블록 제거
            if '.main-nav.active' in line and i + 1 < len(lines):
                # 다음 몇 줄 확인
                next_lines = ''.join(lines[i:min(i+10, len(lines))])
                if re.match(r'\.main-nav\.active\s*\{[^}]*?\}', next_lines, re.DOTALL):
                    # 빈 블록이면 건너뛰기
                    brace_count = 0
                    skip_to = i
                    for j in range(i, min(i+20, len(lines))):
                        brace_count += lines[j].count('{')
                        brace_count -= lines[j].count('}')
                        if brace_count == 0 and '{' in lines[j]:
                            skip_to = j + 1
                            break
                    i = skip_to
                    continue
            
            new_lines.append(line)
            i += 1
        
        content = ''.join(new_lines)
        
        # 1. 빈 CSS 블록 제거 (정규식으로)
        content = re.sub(
            r'\.main-nav\.active\s*\{\s*\}',
            '',
            content
        )
        
        # 2. 미디어 쿼리 구조 정리
        # 미디어 쿼리 안에 필요한 스타일 추가
        if '@media (max-width: 768px)' in content:
            # .mobile-menu-btn { display: block; } 다음에 .main-nav.active .mobile-close-btn 추가
            if '.main-nav.active .mobile-close-btn' not in content:
                content = re.sub(
                    r'(@media[^}]*?\.mobile-menu-btn[^}]*?display:\s*block;[^}]*?\})',
                    r'''\1
            
            .main-nav.active .mobile-close-btn {
                display: block;
            }''',
                    content,
                    flags=re.DOTALL
                )
            
            # 미디어 쿼리 안에 .health-cards-grid 추가 (없으면)
            if '.health-cards-grid' in content and '@media' in content:
                # 미디어 쿼리 안에 있는지 확인
                media_start = content.find('@media (max-width: 768px)')
                if media_start != -1:
                    # 미디어 쿼리 블록 찾기
                    brace_count = 0
                    media_end = media_start
                    for j in range(media_start, len(content)):
                        if content[j] == '{':
                            brace_count += 1
                        elif content[j] == '}':
                            brace_count -= 1
                            if brace_count == 0:
                                media_end = j + 1
                                break
                    
                    media_content = content[media_start:media_end]
                    if '.health-cards-grid' not in media_content:
                        # 미디어 쿼리 안에 추가
                        content = re.sub(
                            r'(@media[^}]*?\.main-nav\.active\s*\.mobile-close-btn[^}]*?display:\s*block;[^}]*?\})',
                            r'''\1
            
            .health-cards-grid {
                grid-template-columns: 1fr;
                gap: 20px;
            }''',
                            content,
                            flags=re.DOTALL
                        )
        
        # 3. HTML 구조 확인 - X 버튼이 nav 안에 있는지
        if '<nav class="main-nav" id="mainNav">' in content:
            nav_start = content.find('<nav class="main-nav" id="mainNav">')
            nav_end = content.find('</nav>', nav_start)
            nav_content = content[nav_start:nav_end]
            
            if '<button class="mobile-close-btn" id="mobileCloseBtn">✕</button>' not in nav_content:
                # nav 안에 X 버튼 추가
                content = re.sub(
                    r'(<nav class="main-nav" id="mainNav">)',
                    r'\1\n                <button class="mobile-close-btn" id="mobileCloseBtn">✕</button>',
                    content
                )
            
            # nav 밖에 있는 X 버튼 제거
            content = re.sub(
                r'(</nav>\s*)(<button class="mobile-menu-btn"[^>]*>☰</button>\s*)(<button class="mobile-close-btn"[^>]*>✕</button>)',
                r'\1\2',
                content
            )
        
        # 4. 헤더 링크 확인 및 수정
        content = re.sub(
            r'href="https://health9988234\.mycafe24\.com/category/식단-음식/"',
            'href="food-main.html"',
            content
        )
        content = re.sub(
            r'href="https://health9988234\.mycafe24\.com/category/운동-활동/"',
            'href="exercise-main.html"',
            content
        )
        content = re.sub(
            r'href="https://health9988234\.mycafe24\.com/category/생활습관/"',
            'href="lifestyle-main.html"',
            content
        )
        content = re.sub(
            r'href="https://health9988234\.mycafe24\.com/category/건강-new/"',
            'href="news-main.html"',
            content
        )
        
        if content != ''.join(original_lines):
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  ✅ {filepath} - 수정 완료")
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
    print("🔧 모든 파일 완전 수정")
    print("=" * 60)
    print("\n💡 수정 사항:")
    print("   1. 빈 CSS 블록 제거")
    print("   2. 미디어 쿼리 구조 정리")
    print("   3. X 버튼: 메뉴 안에 위치")
    print("   4. 헤더 링크: 상대 경로로 수정\n")
    
    print("📝 파일 수정 중...\n")
    fixed_files = []
    
    for file in ALL_FILES:
        if fix_file(file):
            fixed_files.append(file)
    
    print(f"\n✅ 총 {len(fixed_files)}개 파일 수정 완료!")
    print("=" * 60)


if __name__ == "__main__":
    main()

