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
        
        # 1. 중복된 mobile-menu-btn, mobile-close-btn 스타일 제거
        # 기본 스타일 영역에서 중복 제거
        content = re.sub(
            r'\.mobile-menu-btn\s*\{[^}]*?\}',
            '',
            content,
            flags=re.DOTALL
        )
        content = re.sub(
            r'\.mobile-menu-btn:hover\s*\{[^}]*?\}',
            '',
            content,
            flags=re.DOTALL
        )
        content = re.sub(
            r'\.mobile-close-btn\s*\{[^}]*?\}',
            '',
            content,
            flags=re.DOTALL
        )
        content = re.sub(
            r'\.mobile-close-btn:hover\s*\{[^}]*?\}',
            '',
            content,
            flags=re.DOTALL
        )
        content = re.sub(
            r'\.main-nav\.active\s*\.mobile-close-btn\s*\{[^}]*?\}',
            '',
            content,
            flags=re.DOTALL
        )
        
        # 2. 기본 스타일 추가 (nav-item:hover::before 다음에)
        basic_styles = """
        /* 모바일 메뉴 버튼 */
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
        
        /* 모바일 닫기 버튼 */
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
"""
        
        if '.nav-item:hover::before' in content and '.mobile-menu-btn {' not in content:
            content = re.sub(
                r'(\.nav-item:hover::before\s*\{[^}]*?\})',
                r'\1' + basic_styles,
                content
            )
        
        # 3. 모바일 미디어 쿼리 정리
        # 기존 중복된 모바일 미디어 쿼리 제거 후 새로 추가
        mobile_media_new = """        @media (max-width: 768px) {
            .header-content {
                min-height: 70px;
                position: relative;
            }
            
            .logo-image {
                height: 40px;
            }
            
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
            
            .mobile-close-btn {
                display: block;
            }
            
            .main-nav.active ~ .mobile-close-btn {
                opacity: 1;
                transform: scale(1);
            }
        }"""
        
        # 모바일 미디어 쿼리 찾아서 교체
        # 첫 번째 @media (max-width: 768px) 블록 찾기
        if '@media (max-width: 768px)' in content:
            # .header-content부터 시작하는 첫 번째 모바일 미디어 쿼리 찾기
            pattern = r'(@media\s*\(max-width:\s*768px\)\s*\{[^}]*?\.header-content\s*\{[^}]*?\}[^}]*?\.logo-image\s*\{[^}]*?\}[^}]*?)(\.main-nav[^}]*?\}[^}]*?\.main-nav\.active[^}]*?\}[^}]*?\.nav-item[^}]*?\}[^}]*?\.mobile-menu-btn[^}]*?\}[^}]*?\.mobile-menu-btn:hover[^}]*?\}[^}]*?\.mobile-close-btn[^}]*?\}[^}]*?\.mobile-close-btn:hover[^}]*?\}[^}]*?)(@media\s*\(max-width:\s*768px\)[^}]*?\.mobile-close-btn[^}]*?\}[^}]*?\.main-nav\.active[^}]*?\.mobile-close-btn[^}]*?\}[^}]*?\.mobile-close-btn:hover[^}]*?\}[^}]*?@media\s*\(max-width:\s*768px\)[^}]*?\.mobile-close-btn[^}]*?\}[^}]*?\.main-nav\.active[^}]*?\.mobile-close-btn[^}]*?\}[^}]*?\.main-nav\.active\s*\.mobile-close-btn[^}]*?\}[^}]*?\.mobile-close-btn:hover[^}]*?\}[^}]*?@media\s*\(max-width:\s*768px\)[^}]*?\.mobile-close-btn[^}]*?\}[^}]*?\.main-nav\.active[^}]*?\.mobile-close-btn[^}]*?\}[^}]*?\})'
            
            # 더 간단하게: 첫 번째 모바일 미디어 쿼리에서 main-nav 관련 부분만 교체
            # .header-content { ... } .logo-image { ... } 다음 부분을 새 스타일로 교체
            content = re.sub(
                r'(@media\s*\(max-width:\s*768px\)\s*\{[^}]*?\.header-content\s*\{[^}]*?\}[^}]*?\.logo-image\s*\{[^}]*?\}[^}]*?)(\.main-nav[^}]*?\}[^}]*?\.main-nav\.active[^}]*?\}[^}]*?\.nav-item[^}]*?\}[^}]*?\.mobile-menu-btn[^}]*?\}[^}]*?\.mobile-menu-btn:hover[^}]*?\}[^}]*?\.mobile-close-btn[^}]*?\}[^}]*?\.mobile-close-btn:hover[^}]*?\}[^}]*?)(@media\s*\(max-width:\s*768px\)[^}]*?\.mobile-close-btn[^}]*?\}[^}]*?\.main-nav\.active[^}]*?\.mobile-close-btn[^}]*?\}[^}]*?\.mobile-close-btn:hover[^}]*?\}[^}]*?@media\s*\(max-width:\s*768px\)[^}]*?\.mobile-close-btn[^}]*?\}[^}]*?\.main-nav\.active[^}]*?\.mobile-close-btn[^}]*?\}[^}]*?\.main-nav\.active\s*\.mobile-close-btn[^}]*?\}[^}]*?\.mobile-close-btn:hover[^}]*?\}[^}]*?@media\s*\(max-width:\s*768px\)[^}]*?\.mobile-close-btn[^}]*?\}[^}]*?\.main-nav\.active[^}]*?\.mobile-close-btn[^}]*?\}[^}]*?\})',
                r'\1' + mobile_media_new.replace('        @media (max-width: 768px) {', '') + '\n        }',
                content,
                flags=re.DOTALL
            )
        
        # 4. HTML에서 mobile-menu-btn 추가
        if 'id="mobileMenuBtn"' not in content:
            # </nav> 다음에 mobile-menu-btn 추가
            content = re.sub(
                r'(</nav>\s*)(<button class="mobile-close-btn")',
                r'\1            <button class="mobile-menu-btn" id="mobileMenuBtn">☰</button>\n            \2',
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
    print("🔧 모든 파일 모바일 메뉴 수정")
    print("=" * 60)
    print("\n💡 수정 사항:")
    print("   1. 중복 CSS 제거")
    print("   2. 부드러운 메뉴 애니메이션 추가")
    print("   3. 햄버거 바: PC에서 숨김, 모바일에서만 표시")
    print("   4. X 버튼 위치 조정\n")
    
    print("📝 파일 수정 중...\n")
    fixed_files = []
    
    for file in ALL_FILES:
        if fix_file(file):
            fixed_files.append(file)
    
    print(f"\n✅ 총 {len(fixed_files)}개 파일 수정 완료!")
    print("=" * 60)


if __name__ == "__main__":
    main()

