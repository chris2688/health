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


def fix_mobile_menu_btn_visibility(filepath):
    """모바일 햄버거 버튼이 보이도록 수정"""
    if not os.path.exists(filepath):
        print(f"  ⚠️ 파일 없음: {filepath}")
        return False
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 1. 기본 mobile-menu-btn 스타일 확인 (display: none이어야 함)
        # 이미 올바르게 설정되어 있을 수 있음
        
        # 2. 모바일 미디어 쿼리에서 mobile-menu-btn이 display: block인지 확인
        # @media (max-width: 768px) 안에 .mobile-menu-btn { display: block; }가 있어야 함
        
        # 모바일 미디어 쿼리 패턴 찾기
        mobile_media_pattern = r'@media\s*\(max-width:\s*768px\)\s*\{([^}]+)\}'
        
        # 모바일 미디어 쿼리 안에 mobile-menu-btn display: block이 있는지 확인
        if '@media (max-width: 768px)' in content:
            # mobile-menu-btn이 모바일에서 display: block이 되도록 보장
            if '.mobile-menu-btn' in content:
                # 모바일 미디어 쿼리 안에 mobile-menu-btn 스타일이 있는지 확인
                # 없으면 추가
                if not re.search(r'@media\s*\(max-width:\s*768px\)[^}]*\.mobile-menu-btn\s*\{[^}]*display:\s*block;', content, re.DOTALL):
                    # 모바일 미디어 쿼리 안에 추가
                    content = re.sub(
                        r'(@media\s*\(max-width:\s*768px\)\s*\{[^}]*)(\.main-nav\s*\{)',
                        r'\1            .mobile-menu-btn {\n                display: block;\n            }\n            \n            \2',
                        content,
                        flags=re.DOTALL
                    )
        
        # 3. 기본 mobile-menu-btn 스타일이 display: none인지 확인
        if '.mobile-menu-btn {' in content:
            # display 속성이 없거나 잘못된 경우 수정
            content = re.sub(
                r'\.mobile-menu-btn\s*\{[^}]*display:\s*[^;]+;',
                '.mobile-menu-btn {\n            display: none;',
                content,
                flags=re.DOTALL
            )
            # display 속성이 아예 없는 경우 추가
            if 'display:' not in re.search(r'\.mobile-menu-btn\s*\{[^}]*\}', content, re.DOTALL).group(0):
                content = re.sub(
                    r'(\.mobile-menu-btn\s*\{)',
                    r'\1\n            display: none;',
                    content
                )
        
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  ✅ {filepath} - 햄버거 버튼 표시 수정 완료")
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
    print("🔧 모바일 햄버거 버튼 표시 수정")
    print("=" * 60)
    print("\n💡 모바일 화면에서 햄버거 버튼이 보이도록 수정\n")
    
    print("📝 파일 수정 중...\n")
    fixed_files = []
    
    for file in ALL_FILES:
        if fix_mobile_menu_btn_visibility(file):
            fixed_files.append(file)
    
    print(f"\n✅ 총 {len(fixed_files)}개 파일 수정 완료!")
    print("=" * 60)


if __name__ == "__main__":
    main()

