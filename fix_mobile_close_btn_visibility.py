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


def fix_close_btn_visibility(filepath):
    """모바일 닫기 버튼이 메뉴가 열렸을 때만 보이도록 수정"""
    if not os.path.exists(filepath):
        print(f"  ⚠️ 파일 없음: {filepath}")
        return False
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 모바일 미디어 쿼리에서 닫기 버튼 표시 로직 수정
        content = re.sub(
            r'(@media\s*\(max-width:\s*768px\)\s*\{[^}]*\.mobile-close-btn\s*\{[^}]*display:\s*block;[^}]*\}[^}]*\.main-nav\s*\{[^}]*position:\s*relative;[^}]*\})',
            '@media (max-width: 768px) {\n            .mobile-close-btn {\n                display: none;\n            }\n            \n            .main-nav.active .mobile-close-btn {\n                display: block;\n            }\n            \n            .main-nav {\n                position: relative;\n            }\n        }',
            content,
            flags=re.DOTALL
        )
        
        # 다른 패턴도 시도
        content = re.sub(
            r'\.mobile-close-btn\s*\{[^}]*display:\s*block;[^}]*\}',
            '.mobile-close-btn {\n            display: none;\n        }\n        \n        .main-nav.active .mobile-close-btn {',
            content,
            flags=re.DOTALL
        )
        
        # main-nav.active .mobile-close-btn 스타일이 없으면 추가
        if '.main-nav.active .mobile-close-btn' not in content:
            # @media 안에 추가
            content = re.sub(
                r'(@media\s*\(max-width:\s*768px\)\s*\{)',
                r'\1\n            .main-nav.active .mobile-close-btn {\n                display: block;\n            }',
                content
            )
        
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  ✅ {filepath} - 닫기 버튼 표시 로직 수정 완료")
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
    print("🔧 모바일 닫기 버튼 표시 로직 수정")
    print("=" * 60)
    print("\n💡 모바일 메뉴가 열렸을 때만 X 버튼이 보이도록 수정\n")
    
    print("📝 파일 수정 중...\n")
    fixed_files = []
    
    for file in ALL_FILES:
        if fix_close_btn_visibility(file):
            fixed_files.append(file)
    
    print(f"\n✅ 총 {len(fixed_files)}개 파일 수정 완료!")
    print("=" * 60)


if __name__ == "__main__":
    main()

