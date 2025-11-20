import os
import re
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 수정할 파일 목록
ALL_FILES = [
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
    "food-피해야할과일.html",
    "food-질환별식단.html",
    "food-모르면독이된다.html",
    "exercise-질환별운동가이드.html",
    "exercise-운동팁.html",
    "lifestyle-생활습관.html",
    "lifestyle-생활습관바꾸기팁.html",
]


def fix_mobile_menu(filepath):
    """모바일 메뉴 애니메이션 및 햄버거 바 표시 수정"""
    if not os.path.exists(filepath):
        print(f"  ⚠️ 파일 없음: {filepath}")
        return False
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 1. 기본 mobile-menu-btn을 display: none으로 설정 (PC에서는 숨김)
        content = re.sub(
            r'\.mobile-menu-btn\s*\{[^}]*display:\s*block;',
            '.mobile-menu-btn {\n            display: none;',
            content,
            flags=re.DOTALL
        )
        
        # display 속성이 없는 경우 추가
        if '.mobile-menu-btn {' in content:
            btn_style_match = re.search(r'\.mobile-menu-btn\s*\{[^}]*\}', content, re.DOTALL)
            if btn_style_match and 'display:' not in btn_style_match.group(0):
                content = re.sub(
                    r'(\.mobile-menu-btn\s*\{)',
                    r'\1\n            display: none;',
                    content
                )
        
        # 2. 모바일 미디어 쿼리에서 main-nav에 부드러운 애니메이션 추가
        # main-nav를 transform과 opacity로 애니메이션
        mobile_nav_style = """
            .main-nav {
                display: none;
                position: absolute;
                top: 100%;
                left: 0;
                right: 0;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                flex-direction: column;
                padding: 20px;
                box-shadow: 0 4px 20px rgba(0,0,0,0.2);
                z-index: 1000;
                opacity: 0;
                transform: translateY(-20px);
                transition: opacity 0.3s ease, transform 0.3s ease;
                max-height: 0;
                overflow: hidden;
            }
            
            .main-nav.active {
                display: flex;
                opacity: 1;
                transform: translateY(0);
                max-height: 500px;
            }
            
            .nav-item {
                padding: 15px 20px;
                text-align: center;
                opacity: 0;
                transform: translateY(-10px);
                transition: opacity 0.3s ease 0.1s, transform 0.3s ease 0.1s;
            }
            
            .main-nav.active .nav-item {
                opacity: 1;
                transform: translateY(0);
            }
            
            .mobile-menu-btn {
                display: block;
            }
"""
        
        # 기존 모바일 미디어 쿼리의 main-nav 스타일 교체
        content = re.sub(
            r'(@media\s*\(max-width:\s*768px\)[^}]*?\.main-nav\s*\{[^}]*?\}[^}]*?\.main-nav\.active\s*\{[^}]*?\}[^}]*?\.nav-item\s*\{[^}]*?\}[^}]*?\.mobile-menu-btn\s*\{[^}]*?display:\s*block;[^}]*?\})',
            '@media (max-width: 768px) {' + mobile_nav_style + '\n        }',
            content,
            flags=re.DOTALL
        )
        
        # 3. X 버튼을 헤더 우측 상단으로 이동 (햄버거 바 아래)
        # X 버튼을 main-nav 안이 아닌 header-content 안으로 이동
        # HTML 구조 수정: X 버튼을 nav 밖으로 이동
        if '<button class="mobile-close-btn" id="mobileCloseBtn">✕</button>' in content:
            # nav 안의 X 버튼 제거
            content = re.sub(
                r'<nav class="main-nav" id="mainNav">\s*<button class="mobile-close-btn" id="mobileCloseBtn">✕</button>',
                '<nav class="main-nav" id="mainNav">',
                content
            )
            
            # header-content 안, mobile-menu-btn 위에 X 버튼 추가
            content = re.sub(
                r'(<button class="mobile-menu-btn" id="mobileMenuBtn">☰</button>)',
                '<button class="mobile-close-btn" id="mobileCloseBtn">✕</button>\n            \1',
                content
            )
        
        # 4. X 버튼 스타일 수정 (헤더 우측 상단, 햄버거 바 아래)
        close_btn_style = """
        .mobile-close-btn {
            display: none;
            background: none;
            border: none;
            color: white;
            font-size: 24px;
            cursor: pointer;
            padding: 8px 12px;
            position: absolute;
            top: 50px;
            right: 20px;
            z-index: 1001;
            line-height: 1;
            width: 36px;
            height: 36px;
            border-radius: 50%;
            transition: all 0.3s;
            opacity: 0;
            transform: scale(0.8);
        }
        
        .mobile-close-btn:hover {
            background: rgba(255,255,255,0.2);
            transform: scale(1) rotate(90deg);
        }
        
        @media (max-width: 768px) {
            .mobile-close-btn {
                display: block;
            }
            
            .main-nav.active ~ .mobile-close-btn,
            .main-nav.active + * + .mobile-close-btn {
                opacity: 1;
                transform: scale(1);
            }
        }
"""
        
        # 기존 mobile-close-btn 스타일 교체
        content = re.sub(
            r'\.mobile-close-btn\s*\{[^}]*?\}',
            close_btn_style.strip(),
            content,
            flags=re.DOTALL
        )
        
        # 중복된 mobile-close-btn 스타일 제거
        content = re.sub(
            r'(@media\s*\(max-width:\s*768px\)[^}]*?\.mobile-close-btn\s*\{[^}]*?\}[^}]*?\.main-nav\.active\s*\.mobile-close-btn\s*\{[^}]*?\})',
            '',
            content,
            flags=re.DOTALL
        )
        
        # 5. JavaScript에서 X 버튼이 제대로 작동하도록 확인
        # 이미 추가되어 있을 수 있음
        
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  ✅ {filepath} - 모바일 메뉴 수정 완료")
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
    print("🔧 모바일 메뉴 애니메이션 및 햄버거 바 수정")
    print("=" * 60)
    print("\n💡 수정 사항:")
    print("   1. 햄버거 바: PC에서 숨김, 모바일에서만 표시")
    print("   2. 메뉴 애니메이션: 부드럽게 내려오도록")
    print("   3. X 버튼: 헤더 우측 상단(햄버거 바 아래)으로 이동\n")
    
    print("📝 파일 수정 중...\n")
    fixed_files = []
    
    for file in ALL_FILES:
        if fix_mobile_menu(file):
            fixed_files.append(file)
    
    print(f"\n✅ 총 {len(fixed_files)}개 파일 수정 완료!")
    print("=" * 60)


if __name__ == "__main__":
    main()

