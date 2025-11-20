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


def fix_mobile_menu_javascript(filepath):
    """모바일 메뉴 JavaScript 수정"""
    if not os.path.exists(filepath):
        print(f"  ⚠️ 파일 없음: {filepath}")
        return False
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # mobileCloseBtn 이벤트 리스너가 없으면 추가
        if 'mobileCloseBtn' not in content or 'getElementById(\'mobileCloseBtn\')' not in content:
            # mobileMenuBtn 이벤트 리스너 뒤에 추가
            script_pattern = r'(<script>\s*document\.getElementById\(\'mobileMenuBtn\'\)\.addEventListener\(\'click\',\s*function\(\)\s*\{[^}]+\}\);?\s*)'
            
            close_btn_script = """
        document.getElementById('mobileCloseBtn').addEventListener('click', function() {
            document.getElementById('mainNav').classList.remove('active');
        });
"""
            
            if re.search(script_pattern, content, re.DOTALL):
                content = re.sub(
                    script_pattern,
                    r'\1' + close_btn_script,
                    content,
                    flags=re.DOTALL
                )
            else:
                # script 태그가 없으면 추가
                if '</body>' in content:
                    content = content.replace(
                        '</body>',
                        f'<script>{close_btn_script}\n    </script>\n</body>'
                    )
        
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  ✅ {filepath} - 모바일 메뉴 JavaScript 수정 완료")
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
    print("🔧 모바일 메뉴 JavaScript 수정")
    print("=" * 60)
    print("\n💡 모바일 메뉴 X 버튼 클릭 이벤트 추가\n")
    
    print("📝 파일 수정 중...\n")
    fixed_files = []
    
    for file in ALL_FILES:
        if fix_mobile_menu_javascript(file):
            fixed_files.append(file)
    
    print(f"\n✅ 총 {len(fixed_files)}개 파일 수정 완료!")
    print("=" * 60)


if __name__ == "__main__":
    main()

