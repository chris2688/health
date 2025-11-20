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


def fix_mobile_menu_clean(filepath):
    """모바일 메뉴 CSS 정리 및 수정"""
    if not os.path.exists(filepath):
        print(f"  ⚠️ 파일 없음: {filepath}")
        return False
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 1. 기본 mobile-menu-btn 스타일 (PC에서는 숨김)
        basic_mobile_btn = """        .mobile-menu-btn {
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
        }"""
        
        # 2. 기본 mobile-close-btn 스타일
        basic_close_btn = """        .mobile-close-btn {
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
        }"""
        
        # 3. 모바일 미디어 쿼리 스타일
        mobile_media = """        @media (max-width: 768px) {
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
            
            .main-nav.active ~ .mobile-close-btn,
            .header-content:has(.main-nav.active) .mobile-close-btn {
                opacity: 1;
                transform: scale(1);
            }
        }"""
        
        # 4. 기존 중복된 mobile-menu-btn, mobile-close-btn 스타일 모두 제거
        # 기본 스타일 영역 찾기 (</style> 전)
        # mobile-menu-btn과 mobile-close-btn의 모든 정의 제거
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
        
        # 중복된 @media (max-width: 768px) 블록 제거 (모바일 메뉴 관련)
        # 하지만 다른 반응형 스타일은 유지해야 함
        # 일단 모바일 메뉴 관련 중복만 제거
        
        # 5. 기본 스타일 추가 (</style> 태그 바로 전)
        if '</style>' in content:
            # 기본 mobile-menu-btn과 mobile-close-btn 스타일 추가
            style_end_pos = content.rfind('</style>')
            before_style = content[:style_end_pos]
            after_style = content[style_end_pos:]
            
            # 이미 추가되어 있는지 확인
            if '.mobile-menu-btn {' not in before_style:
                before_style += '\n' + basic_mobile_btn + '\n'
            if '.mobile-close-btn {' not in before_style:
                before_style += '\n' + basic_close_btn + '\n'
            
            content = before_style + after_style
        
        # 6. 모바일 미디어 쿼리 찾아서 교체
        # 기존 모바일 미디어 쿼리에서 main-nav 관련 부분만 교체
        mobile_nav_pattern = r'(@media\s*\(max-width:\s*768px\)[^}]*?\.header-content\s*\{[^}]*?\}[^}]*?\.logo-image\s*\{[^}]*?\}[^}]*?)(\.main-nav\s*\{[^}]*?\}[^}]*?\.main-nav\.active\s*\{[^}]*?\}[^}]*?\.nav-item\s*\{[^}]*?\}[^}]*?\.mobile-menu-btn\s*\{[^}]*?display:\s*[^}]*?\}[^}]*?)(\.mobile-close-btn\s*\{[^}]*?\}[^}]*?\.mobile-close-btn:hover\s*\{[^}]*?\}[^}]*?@media\s*\(max-width:\s*768px\)[^}]*?\.mobile-close-btn\s*\{[^}]*?\}[^}]*?\.main-nav\.active[^}]*?\.mobile-close-btn[^}]*?\}[^}]*?\.mobile-close-btn:hover\s*\{[^}]*?\}[^}]*?@media\s*\(max-width:\s*768px\)[^}]*?\.mobile-close-btn\s*\{[^}]*?\}[^}]*?\.main-nav\.active[^}]*?\.mobile-close-btn[^}]*?\}[^}]*?\.main-nav\.active\s*\.mobile-close-btn\s*\{[^}]*?\}[^}]*?\.mobile-close-btn:hover\s*\{[^}]*?\}[^}]*?@media\s*\(max-width:\s*768px\)[^}]*?\.mobile-close-btn\s*\{[^}]*?\}[^}]*?\.main-nav\.active[^}]*?\.mobile-close-btn[^}]*?\}[^}]*?\})'
        
        # 간단하게: 모바일 미디어 쿼리 전체를 찾아서 교체
        # 하지만 다른 반응형 스타일도 있을 수 있으므로 주의
        # 일단 모바일 미디어 쿼리에서 main-nav, mobile-menu-btn, mobile-close-btn 관련만 교체
        
        # 더 간단한 방법: 모바일 미디어 쿼리 블록을 찾아서 main-nav 관련 부분만 교체
        if '@media (max-width: 768px)' in content:
            # 모바일 미디어 쿼리에서 main-nav 스타일 부분 찾기
            # .main-nav부터 시작해서 다음 } 또는 다른 @media까지
            # 일단 전체 모바일 미디어 쿼리를 찾아서 필요한 부분만 교체
            
            # 패턴: @media (max-width: 768px) { ... .main-nav { ... } ... .mobile-menu-btn { ... } ... }
            # 이 부분을 새로운 스타일로 교체
            
            # 복잡하므로, 간단하게: 기존 모바일 미디어 쿼리에서 main-nav, mobile-menu-btn, mobile-close-btn 관련 스타일만 제거하고 새로 추가
            content = re.sub(
                r'(@media\s*\(max-width:\s*768px\)[^}]*?)(\.main-nav\s*\{[^}]*?\}[^}]*?\.main-nav\.active\s*\{[^}]*?\}[^}]*?\.nav-item\s*\{[^}]*?\}[^}]*?\.mobile-menu-btn\s*\{[^}]*?\}[^}]*?\.mobile-menu-btn:hover\s*\{[^}]*?\}[^}]*?\.mobile-close-btn\s*\{[^}]*?\}[^}]*?\.mobile-close-btn:hover\s*\{[^}]*?\}[^}]*?@media\s*\(max-width:\s*768px\)[^}]*?\.mobile-close-btn\s*\{[^}]*?\}[^}]*?\.main-nav\.active[^}]*?\.mobile-close-btn[^}]*?\}[^}]*?\.mobile-close-btn:hover\s*\{[^}]*?\}[^}]*?@media\s*\(max-width:\s*768px\)[^}]*?\.mobile-close-btn\s*\{[^}]*?\}[^}]*?\.main-nav\.active[^}]*?\.mobile-close-btn[^}]*?\}[^}]*?\.main-nav\.active\s*\.mobile-close-btn\s*\{[^}]*?\}[^}]*?\.mobile-close-btn:hover\s*\{[^}]*?\}[^}]*?@media\s*\(max-width:\s*768px\)[^}]*?\.mobile-close-btn\s*\{[^}]*?\}[^}]*?\.main-nav\.active[^}]*?\.mobile-close-btn[^}]*?\}[^}]*?\})',
                r'\1' + mobile_media.replace('        @media (max-width: 768px) {', ''),
                content,
                flags=re.DOTALL
            )
        
        # 7. JavaScript에서 X 버튼 클릭 시 메뉴 닫기 확인
        # 이미 있을 수 있음
        
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  ✅ {filepath} - 모바일 메뉴 정리 완료")
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
    print("🔧 모바일 메뉴 CSS 정리 및 수정")
    print("=" * 60)
    print("\n💡 중복된 CSS 제거 및 올바른 스타일 적용\n")
    
    print("📝 파일 수정 중...\n")
    fixed_files = []
    
    for file in ALL_FILES:
        if fix_mobile_menu_clean(file):
            fixed_files.append(file)
    
    print(f"\n✅ 총 {len(fixed_files)}개 파일 수정 완료!")
    print("=" * 60)


if __name__ == "__main__":
    main()

