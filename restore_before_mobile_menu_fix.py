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


def restore_file(filepath):
    """파일을 모바일 메뉴 수정 전 상태로 복구"""
    if not os.path.exists(filepath):
        print(f"  ⚠️ 파일 없음: {filepath}")
        return False
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 1. 깨진 CSS 제거 및 정리
        # 중복된 @media 블록 제거
        content = re.sub(
            r'@media\s*\(max-width:\s*768px\)\s*\{[^}]*?\.main-nav\.active\s*~\s*\.mobile-close-btn[^}]*?\}[^}]*?\}',
            '',
            content,
            flags=re.DOTALL
        )
        
        # 깨진 CSS 제거
        content = re.sub(
            r'\.main-nav\.active\s*$',
            '',
            content,
            flags=re.MULTILINE
        )
        
        # 2. 기본 mobile-menu-btn 스타일 (PC에서 숨김)
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
        
        # 기존 mobile-menu-btn 스타일 교체
        if '.mobile-menu-btn {' in content:
            content = re.sub(
                r'\.mobile-menu-btn\s*\{[^}]*?\}',
                basic_mobile_btn.strip(),
                content,
                flags=re.DOTALL
            )
        else:
            # nav-item:hover::before 다음에 추가
            if '.nav-item:hover::before' in content:
                content = re.sub(
                    r'(\.nav-item:hover::before\s*\{[^}]*?\})',
                    r'\1\n' + basic_mobile_btn,
                    content
                )
        
        # 3. 기본 mobile-close-btn 스타일
        basic_close_btn = """        .mobile-close-btn {
            display: none;
            background: none;
            border: none;
            color: white;
            font-size: 24px;
            cursor: pointer;
            padding: 8px 12px;
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
        }"""
        
        # 기존 mobile-close-btn 스타일 교체
        if '.mobile-close-btn {' in content:
            content = re.sub(
                r'\.mobile-close-btn\s*\{[^}]*?\}',
                basic_close_btn.strip(),
                content,
                flags=re.DOTALL
            )
        else:
            # mobile-menu-btn 다음에 추가
            if '.mobile-menu-btn:hover' in content:
                content = re.sub(
                    r'(\.mobile-menu-btn:hover\s*\{[^}]*?\})',
                    r'\1\n' + basic_close_btn,
                    content
                )
        
        # 4. 모바일 미디어 쿼리 정리 (애니메이션 없이 단순하게)
        mobile_media = """        @media (max-width: 768px) {
            .header-content {
                min-height: 70px;
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
            
            .main-nav.active .mobile-close-btn {
                display: block;
            }
        }"""
        
        # 기존 모바일 미디어 쿼리 찾아서 교체
        if '@media (max-width: 768px)' in content:
            # 첫 번째 모바일 미디어 쿼리에서 main-nav 관련 부분 교체
            pattern = r'(@media\s*\(max-width:\s*768px\)\s*\{[^}]*?\.header-content[^}]*?\}[^}]*?\.logo-image[^}]*?\}[^}]*?)(\.main-nav[^}]*?\}[^}]*?\.main-nav\.active[^}]*?\}[^}]*?\.nav-item[^}]*?\}[^}]*?\.mobile-menu-btn[^}]*?\}[^}]*?\.mobile-close-btn[^}]*?\}[^}]*?\.main-nav\.active[^}]*?\.mobile-close-btn[^}]*?\}[^}]*?\})'
            
            if re.search(pattern, content, re.DOTALL):
                content = re.sub(
                    pattern,
                    r'\1' + mobile_media.replace('        @media (max-width: 768px) {', ''),
                    content,
                    flags=re.DOTALL
                )
            else:
                # 간단하게 첫 번째 모바일 미디어 쿼리 전체 교체
                first_media = re.search(r'@media\s*\(max-width:\s*768px\)\s*\{[^}]*?\}', content, re.DOTALL)
                if first_media:
                    # header-content가 포함된 첫 번째 미디어 쿼리 찾기
                    header_media = re.search(r'@media\s*\(max-width:\s*768px\)\s*\{[^}]*?\.header-content[^}]*?\}[^}]*?\}', content, re.DOTALL)
                    if header_media:
                        content = re.sub(
                            header_media.group(0),
                            mobile_media,
                            content,
                            count=1
                        )
        
        # 5. HTML 구조 확인
        # mobile-menu-btn이 없으면 추가
        if 'id="mobileMenuBtn"' not in content:
            if '</nav>' in content:
                content = re.sub(
                    r'(</nav>\s*)(<button class="mobile-close-btn")',
                    r'\1            <button class="mobile-menu-btn" id="mobileMenuBtn">☰</button>\n            \2',
                    content
                )
        
        # mobile-close-btn이 main-nav 안에 있으면 밖으로 이동
        if '<nav class="main-nav" id="mainNav">' in content and '<button class="mobile-close-btn"' in content:
            # nav 안의 close 버튼 제거
            content = re.sub(
                r'<nav class="main-nav" id="mainNav">\s*<button class="mobile-close-btn"[^>]*>✕</button>',
                '<nav class="main-nav" id="mainNav">',
                content
            )
            # nav 밖에 close 버튼 추가
            if 'id="mobileMenuBtn"' in content:
                content = re.sub(
                    r'(<button class="mobile-menu-btn" id="mobileMenuBtn">☰</button>)',
                    r'\1\n            <button class="mobile-close-btn" id="mobileCloseBtn">✕</button>',
                    content
                )
        
        # 6. JavaScript 확인
        if 'mobileCloseBtn' not in content or 'addEventListener' not in content:
            # JavaScript 추가
            if '</script>' in content:
                close_js = '''
        document.getElementById('mobileCloseBtn').addEventListener('click', function() {
            document.getElementById('mainNav').classList.remove('active');
        });'''
                content = re.sub(
                    r'(</script>)',
                    close_js + '\n    \1',
                    content
                )
        
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  ✅ {filepath} - 복구 완료")
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
    print("🔧 모바일 메뉴 수정 전 상태로 복구")
    print("=" * 60)
    print("\n💡 복구 사항:")
    print("   1. 깨진 CSS 정리")
    print("   2. PC: 햄버거 바 숨김")
    print("   3. 모바일: 단순 메뉴 (애니메이션 없음)")
    print("   4. X 버튼: 메뉴 안에 위치\n")
    
    print("📝 파일 수정 중...\n")
    fixed_files = []
    
    for file in ALL_FILES:
        if restore_file(file):
            fixed_files.append(file)
    
    print(f"\n✅ 총 {len(fixed_files)}개 파일 복구 완료!")
    print("=" * 60)


if __name__ == "__main__":
    main()

