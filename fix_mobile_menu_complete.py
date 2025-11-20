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


def fix_file_complete(filepath):
    """모바일 메뉴 완전 수정"""
    if not os.path.exists(filepath):
        print(f"  ⚠️ 파일 없음: {filepath}")
        return False
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 1. 깨진 모바일 미디어 쿼리 제거
        # @media (max-width: 768px) 블록이 제대로 닫히지 않은 경우 모두 제거
        content = re.sub(
            r'@media\s*\(max-width:\s*768px\)\s*\{[^}]*?\.main-nav\.active\s*~\s*\.mobile-close-btn[^}]*?\}',
            '',
            content,
            flags=re.DOTALL
        )
        
        # 2. 기본 스타일 정리
        # mobile-menu-btn 기본 스타일
        if '.mobile-menu-btn {' not in content or 'display: none;' not in re.search(r'\.mobile-menu-btn\s*\{[^}]*?\}', content, re.DOTALL).group(0) if re.search(r'\.mobile-menu-btn\s*\{[^}]*?\}', content, re.DOTALL) else '':
            content = re.sub(
                r'\.mobile-menu-btn\s*\{[^}]*?\}',
                '''        .mobile-menu-btn {
            display: none;
            background: none;
            border: none;
            color: white;
            font-size: 28px;
            cursor: pointer;
            padding: 10px;
            transition: all 0.3s;
            position: absolute;
            top: 20px;
            right: 20px;
            z-index: 1002;
        }''',
                content,
                flags=re.DOTALL
            )
        
        # mobile-menu-btn:hover
        if '.mobile-menu-btn:hover' not in content:
            content = re.sub(
                r'(\.mobile-menu-btn\s*\{[^}]*?\})',
                r'''\1
        
        .mobile-menu-btn:hover {
            background: rgba(255,255,255,0.15);
            border-radius: 8px;
        }''',
                content,
                flags=re.DOTALL
            )
        
        # mobile-close-btn 기본 스타일
        if '.mobile-close-btn {' not in content or 'display: none;' not in re.search(r'\.mobile-close-btn\s*\{[^}]*?\}', content, re.DOTALL).group(0) if re.search(r'\.mobile-close-btn\s*\{[^}]*?\}', content, re.DOTALL) else '':
            content = re.sub(
                r'\.mobile-close-btn\s*\{[^}]*?\}',
                '''        .mobile-close-btn {
            display: none;
            background: none;
            border: none;
            color: white;
            font-size: 24px;
            cursor: pointer;
            padding: 8px 12px;
            position: absolute;
            top: 70px;
            right: 20px;
            z-index: 1001;
            line-height: 1;
            width: 36px;
            height: 36px;
            border-radius: 50%;
            transition: all 0.3s;
            opacity: 0;
            transform: scale(0.8);
        }''',
                content,
                flags=re.DOTALL
            )
        
        # mobile-close-btn:hover
        if '.mobile-close-btn:hover' not in content:
            content = re.sub(
                r'(\.mobile-close-btn\s*\{[^}]*?\})',
                r'''\1
        
        .mobile-close-btn:hover {
            background: rgba(255,255,255,0.2);
            transform: scale(1) rotate(90deg);
        }''',
                content,
                flags=re.DOTALL
            )
        
        # 3. 모바일 미디어 쿼리 추가/수정
        mobile_media_css = '''        @media (max-width: 768px) {
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
        }'''
        
        # 기존 모바일 미디어 쿼리 찾아서 교체
        # 패턴: @media (max-width: 768px) { ... } (header-content 포함)
        if '@media (max-width: 768px)' in content:
            # 첫 번째 모바일 미디어 쿼리 찾기
            pattern = r'(@media\s*\(max-width:\s*768px\)\s*\{[^}]*?\.header-content[^}]*?\}[^}]*?\.logo-image[^}]*?\}[^}]*?)(\.main-nav[^}]*?\}[^}]*?\.main-nav\.active[^}]*?\}[^}]*?\.nav-item[^}]*?\}[^}]*?\.mobile-menu-btn[^}]*?\}[^}]*?\.mobile-close-btn[^}]*?\}[^}]*?\.main-nav\.active[^}]*?\.mobile-close-btn[^}]*?\}[^}]*?\})'
            
            if re.search(pattern, content, re.DOTALL):
                content = re.sub(
                    pattern,
                    r'\1' + mobile_media_css.replace('        @media (max-width: 768px) {', ''),
                    content,
                    flags=re.DOTALL
                )
            else:
                # 모바일 미디어 쿼리가 없거나 깨진 경우, footer 전에 추가
                if '/* ========== 반응형 ========== */' in content:
                    content = re.sub(
                        r'(/\* ========== 반응형 ========== \*/)',
                        r'\1\n' + mobile_media_css,
                        content
                    )
                elif '</style>' in content:
                    content = re.sub(
                        r'(</style>)',
                        mobile_media_css + '\n    \1',
                        content
                    )
        else:
            # 모바일 미디어 쿼리가 아예 없는 경우 추가
            if '</style>' in content:
                content = re.sub(
                    r'(</style>)',
                    mobile_media_css + '\n    \1',
                    content
                )
        
        # 4. HTML에서 mobile-menu-btn이 없으면 추가
        if 'id="mobileMenuBtn"' not in content:
            # </nav> 다음에 mobile-menu-btn 추가
            content = re.sub(
                r'(</nav>\s*)(<button class="mobile-close-btn")',
                r'\1            <button class="mobile-menu-btn" id="mobileMenuBtn">☰</button>\n            \2',
                content
            )
        
        # 5. JavaScript 확인
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
            print(f"  ✅ {filepath} - 완전 수정 완료")
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
    print("🔧 모바일 메뉴 완전 수정")
    print("=" * 60)
    print("\n💡 수정 사항:")
    print("   1. 깨진 CSS 정리")
    print("   2. PC: 햄버거 바 숨김")
    print("   3. 모바일: 햄버거 바 표시, 부드러운 애니메이션")
    print("   4. X 버튼: 헤더 우측 상단(햄버거 바 아래)\n")
    
    print("📝 파일 수정 중...\n")
    fixed_files = []
    
    for file in ALL_FILES:
        if fix_file_complete(file):
            fixed_files.append(file)
    
    print(f"\n✅ 총 {len(fixed_files)}개 파일 수정 완료!")
    print("=" * 60)


if __name__ == "__main__":
    main()

