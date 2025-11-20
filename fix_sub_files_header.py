import os
import re
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 모든 sub 파일 목록
SUB_FILES = [
    'sub-고혈압.html', 'sub-고지혈증.html', 'sub-협심증심근경색.html', 'sub-동맥경화.html', 'sub-뇌졸중.html',
    'sub-당뇨.html', 'sub-공복혈당장애.html', 'sub-당뇨병합병증.html',
    'sub-허리디스크목디스크.html', 'sub-골다공증.html', 'sub-오십견.html',
    'sub-갑상선.html', 'sub-갱년기증후군.html', 'sub-대사증후군.html',
    'sub-우울증번아웃.html', 'sub-수면장애불면증.html', 'sub-치매경도인지장애.html', 'sub-이명어지럼증.html',
    'sub-위염위궤양.html', 'sub-역류성식도염.html', 'sub-과민성대장증후군.html', 'sub-지방간.html',
    'sub-백내장녹내장.html', 'sub-치주염치아손실.html', 'sub-비만체형변화.html',
    'sub-관절염.html',  # 템플릿도 수정
]

# 올바른 헤더 구조 (index-v2.html 기준)
CORRECT_NAV = '''            <nav class="main-nav" id="mainNav">
                <button class="mobile-close-btn" id="mobileCloseBtn">✕</button>
                <a href="index-v2.html" class="nav-item">질환별 정보</a>
                <a href="food-main.html" class="nav-item">식단/음식</a>
                <a href="exercise-main.html" class="nav-item">운동/활동</a>
                <a href="lifestyle-main.html" class="nav-item">생활습관</a>
                <a href="news-main.html" class="nav-item">건강News</a>
            </nav>'''

# 모바일 닫기 버튼 스타일 추가
MOBILE_CLOSE_BTN_CSS = '''
        .mobile-close-btn {
            display: none;
            background: none;
            border: none;
            color: white;
            font-size: 24px;
            cursor: pointer;
            padding: 10px;
            position: absolute;
            top: 15px;
            right: 15px;
            z-index: 1001;
        }
        
        @media (max-width: 768px) {
            .mobile-close-btn {
                display: block;
            }
        }'''

# 모바일 닫기 버튼 JavaScript 추가
MOBILE_CLOSE_JS = '''
        document.getElementById('mobileCloseBtn').addEventListener('click', function() {
            document.getElementById('mainNav').classList.remove('active');
        });'''


def fix_sub_file_header(filepath):
    """sub 파일의 헤더 수정"""
    if not os.path.exists(filepath):
        return False
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 1. nav 태그 수정 (mobile-close-btn 추가)
        nav_pattern = r'<nav class="main-nav" id="mainNav">.*?</nav>'
        if re.search(nav_pattern, content, re.DOTALL):
            content = re.sub(nav_pattern, CORRECT_NAV, content, flags=re.DOTALL)
        
        # 2. mobile-close-btn CSS 추가 (이미 있으면 스킵)
        if '.mobile-close-btn' not in content:
            # .mobile-menu-btn 다음에 추가
            if '.mobile-menu-btn' in content:
                content = re.sub(
                    r'(\.mobile-menu-btn\s*\{[^}]+\})',
                    r'\1' + MOBILE_CLOSE_BTN_CSS,
                    content
                )
            else:
                # @media (max-width: 768px) 전에 추가
                content = re.sub(
                    r'(@media \(max-width: 768px\))',
                    MOBILE_CLOSE_BTN_CSS + r'\n        \1',
                    content
                )
        
        # 3. mobile-close-btn JavaScript 추가
        if 'mobileCloseBtn' not in content:
            # mobileMenuBtn 이벤트 리스너 다음에 추가
            if 'mobileMenuBtn' in content:
                content = re.sub(
                    r'(document\.getElementById\(\'mobileMenuBtn\'\)\.addEventListener\([^}]+\}\);?)',
                    r'\1' + MOBILE_CLOSE_JS,
                    content
                )
            else:
                # </script> 전에 추가
                content = re.sub(
                    r'(</script>)',
                    MOBILE_CLOSE_JS + r'\n    \1',
                    content,
                    count=1
                )
        
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
        
    except Exception as e:
        print(f"  ❌ {filepath} - 오류: {e}")
        return False


def main():
    """메인 실행"""
    print("=" * 60)
    print("🔧 모든 sub 파일 헤더 수정")
    print("=" * 60)
    print("\n💡 수정 사항:")
    print("   1. 모바일 닫기 버튼 추가")
    print("   2. 모바일 닫기 버튼 CSS 추가")
    print("   3. 모바일 닫기 버튼 JavaScript 추가\n")
    
    print("📝 파일 수정 중...\n")
    fixed_count = 0
    
    for file in SUB_FILES:
        if fix_sub_file_header(file):
            print(f"  ✅ {file} - 헤더 수정 완료")
            fixed_count += 1
        else:
            print(f"  ℹ️ {file} - 변경사항 없음")
    
    print(f"\n✅ 총 {fixed_count}개 파일 수정 완료!")
    print("=" * 60)


if __name__ == "__main__":
    main()

