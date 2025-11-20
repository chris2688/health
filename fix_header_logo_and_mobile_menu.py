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


def fix_header_and_mobile_menu(filepath):
    """헤더 로고 텍스트 제거 및 모바일 메뉴 X 버튼 추가"""
    if not os.path.exists(filepath):
        print(f"  ⚠️ 파일 없음: {filepath}")
        return False
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 1. 로고 옆 텍스트 제거
        content = re.sub(
            r'<span class="logo-text">9988 건강 연구소</span>',
            '',
            content
        )
        
        # 2. logo-text 스타일 제거 (더 이상 필요 없음)
        content = re.sub(
            r'\.logo-text\s*\{[^}]*\}',
            '',
            content,
            flags=re.DOTALL
        )
        
        # 3. 모바일 메뉴에 X 버튼 추가
        # main-nav 안에 닫기 버튼 추가
        if '<nav class="main-nav" id="mainNav">' in content:
            # 닫기 버튼이 없으면 추가
            if 'mobile-close-btn' not in content:
                # nav 시작 부분에 닫기 버튼 추가
                content = re.sub(
                    r'(<nav class="main-nav" id="mainNav">)',
                    r'\1\n                <button class="mobile-close-btn" id="mobileCloseBtn">✕</button>',
                    content
                )
        
        # 4. 모바일 닫기 버튼 스타일 추가
        if '.mobile-close-btn' not in content:
            # mobile-menu-btn 스타일 뒤에 추가
            close_btn_style = """
        .mobile-close-btn {
            display: none;
            background: none;
            border: none;
            color: white;
            font-size: 32px;
            cursor: pointer;
            padding: 10px;
            position: absolute;
            top: 15px;
            right: 15px;
            z-index: 1001;
            line-height: 1;
            width: 40px;
            height: 40px;
            border-radius: 50%;
            transition: all 0.3s;
        }
        
        .mobile-close-btn:hover {
            background: rgba(255,255,255,0.2);
            transform: rotate(90deg);
        }
        
        @media (max-width: 768px) {
            .mobile-close-btn {
                display: block;
            }
            
            .main-nav {
                position: relative;
            }
        }
"""
            # mobile-menu-btn 스타일 뒤에 추가
            content = re.sub(
                r'(\.mobile-menu-btn\s*\{[^}]*\})',
                r'\1' + close_btn_style,
                content,
                flags=re.DOTALL
            )
        
        # 5. 모바일 메뉴 닫기 버튼 JavaScript 추가
        # 기존 mobileMenuBtn 이벤트 리스너 찾기
        if 'mobileCloseBtn' not in content:
            # mobileMenuBtn 이벤트 리스너 뒤에 닫기 버튼 이벤트 추가
            content = re.sub(
                r'(document\.getElementById\(\'mobileMenuBtn\'\)\.addEventListener\(\'click\',\s*function\(\)\s*\{[^}]+\}\);?)',
                r'\1\n        document.getElementById(\'mobileCloseBtn\').addEventListener(\'click\', function() {\n            document.getElementById(\'mainNav\').classList.remove(\'active\');\n        });',
                content,
                flags=re.DOTALL
            )
        
        # 6. 모바일 햄버거 바 디자인 통일 (모든 페이지에서 동일하게)
        # mobile-menu-btn 스타일을 표준화
        standard_mobile_btn_style = """
        .mobile-menu-btn {
            display: none;
            background: none;
            border: none;
            color: white;
            font-size: 28px;
            cursor: pointer;
            padding: 10px;
            transition: all 0.3s;
        }
        
        .mobile-menu-btn:hover {
            background: rgba(255,255,255,0.15);
            border-radius: 8px;
        }
"""
        # 기존 mobile-menu-btn 스타일 교체
        content = re.sub(
            r'\.mobile-menu-btn\s*\{[^}]*\}',
            standard_mobile_btn_style.strip(),
            content,
            flags=re.DOTALL
        )
        
        # 7. 모바일에서 main-nav 스타일 통일
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
            }
            
            .main-nav.active {
                display: flex;
            }
            
            .nav-item {
                padding: 15px 20px;
                text-align: center;
            }
            
            .mobile-menu-btn {
                display: block;
            }
"""
        # 모바일 미디어 쿼리 안의 main-nav 스타일 교체
        content = re.sub(
            r'(@media\s*\(max-width:\s*768px\)\s*\{[^}]*\.main-nav\s*\{[^}]*\}[^}]*\.main-nav\.active\s*\{[^}]*\}[^}]*\.nav-item\s*\{[^}]*\}[^}]*\.mobile-menu-btn\s*\{[^}]*\})',
            mobile_nav_style.strip(),
            content,
            flags=re.DOTALL
        )
        
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  ✅ {filepath} - 헤더 및 모바일 메뉴 수정 완료")
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
    print("🔧 헤더 로고 텍스트 제거 및 모바일 메뉴 개선")
    print("=" * 60)
    print("\n💡 수정 사항:")
    print("   1. 로고 옆 '9988 건강 연구소' 텍스트 제거")
    print("   2. 모바일 햄버거 바 디자인 통일")
    print("   3. 모바일 메뉴에 X 버튼 추가\n")
    
    print("📝 파일 수정 중...\n")
    fixed_files = []
    
    for file in ALL_FILES:
        if fix_header_and_mobile_menu(file):
            fixed_files.append(file)
    
    print(f"\n✅ 총 {len(fixed_files)}개 파일 수정 완료!")
    
    print("\n" + "=" * 60)
    print("✅ 수정 완료!")
    print("=" * 60)
    print("\n💡 수정된 내용:")
    print("   - 로고 옆 텍스트 제거 (로고만 표시)")
    print("   - 모바일 햄버거 바 디자인 통일")
    print("   - 모바일 메뉴에 X 버튼 추가 (우측 상단)")
    print("=" * 60)


if __name__ == "__main__":
    main()

