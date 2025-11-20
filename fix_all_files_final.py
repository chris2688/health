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
    """파일 수정"""
    if not os.path.exists(filepath):
        print(f"  ⚠️ 파일 없음: {filepath}")
        return False
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 1. 중복된 mobile-close-btn:hover 제거
        content = re.sub(
            r'\.mobile-close-btn:hover\s*\{[^}]*?\}\s*\.mobile-close-btn:hover\s*\{[^}]*?\}',
            '.mobile-close-btn:hover {\n            background: rgba(255,255,255,0.2);\n            transform: rotate(90deg);\n        }',
            content,
            flags=re.DOTALL
        )
        
        # 2. 모바일 미디어 쿼리 정리
        # 깨진 nav-item 스타일 수정
        content = re.sub(
            r'\.nav-item\s*\{[^}]*?opacity\s+0\.3s[^}]*?\}',
            '.nav-item {\n                padding: 15px 20px;\n                text-align: center;\n            }',
            content,
            flags=re.DOTALL
        )
        
        # 빈 .main-nav.active .nav-item 제거
        content = re.sub(
            r'\.main-nav\.active\s*\.nav-item\s*\{\s*\}',
            '',
            content
        )
        
        # .mobile-close-btn { display: block; } 제거 (모바일 미디어 쿼리 안에서)
        content = re.sub(
            r'(@media[^}]*?\.mobile-menu-btn\s*\{[^}]*?display:\s*block;[^}]*?\})\s*\.mobile-close-btn\s*\{[^}]*?display:\s*block;[^}]*?\}',
            r'\1',
            content,
            flags=re.DOTALL
        )
        
        # .main-nav.active ~ .mobile-close-btn 빈 블록 제거
        content = re.sub(
            r'\.main-nav\.active\s*~\s*\.mobile-close-btn\s*\{\s*\}',
            '',
            content
        )
        
        # .main-nav.active .mobile-close-btn 추가 (없으면)
        if '@media (max-width: 768px)' in content and '.main-nav.active .mobile-close-btn' not in content:
            content = re.sub(
                r'(@media[^}]*?\.mobile-menu-btn\s*\{[^}]*?display:\s*block;[^}]*?\})',
                r'''\1
            
            .main-nav.active .mobile-close-btn {
                display: block;
            }''',
                content,
                flags=re.DOTALL
            )
        
        # 3. HTML 구조 수정 - X 버튼을 nav 안으로
        if '<nav class="main-nav" id="mainNav">' in content:
            # nav 밖의 X 버튼 제거
            content = re.sub(
                r'(</nav>\s*)(<button class="mobile-menu-btn"[^>]*>☰</button>\s*)(<button class="mobile-close-btn"[^>]*>✕</button>)',
                r'\2',
                content
            )
            
            # nav 안에 X 버튼 추가 (없으면)
            if '<button class="mobile-close-btn" id="mobileCloseBtn">✕</button>' not in content.split('</nav>')[0]:
                content = re.sub(
                    r'(<nav class="main-nav" id="mainNav">)',
                    r'\1\n                <button class="mobile-close-btn" id="mobileCloseBtn">✕</button>',
                    content
                )
        
        if content != original_content:
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
    print("🔧 모든 파일 최종 정리")
    print("=" * 60)
    print("\n💡 수정 사항:")
    print("   1. 중복 CSS 제거")
    print("   2. 깨진 스타일 수정")
    print("   3. X 버튼: 메뉴 안에 위치\n")
    
    print("📝 파일 수정 중...\n")
    fixed_files = []
    
    for file in ALL_FILES:
        if fix_file(file):
            fixed_files.append(file)
    
    print(f"\n✅ 총 {len(fixed_files)}개 파일 수정 완료!")
    print("=" * 60)


if __name__ == "__main__":
    main()

