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


def fix_hamburger_display(filepath):
    """모바일 미디어 쿼리 안에서 햄버거 버튼이 display: block이 되도록 수정"""
    if not os.path.exists(filepath):
        print(f"  ⚠️ 파일 없음: {filepath}")
        return False
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 모바일 미디어 쿼리 안의 .mobile-menu-btn 스타일을 display: block으로 변경
        # 패턴: @media (max-width: 768px) { ... .mobile-menu-btn { display: none; ... } ... }
        content = re.sub(
            r'(@media\s*\(max-width:\s*768px\)[^}]*\.mobile-menu-btn\s*\{[^}]*?)display:\s*none;',
            r'\1display: block;',
            content,
            flags=re.DOTALL
        )
        
        # 다른 패턴도 시도 (들여쓰기가 다른 경우)
        content = re.sub(
            r'(\.mobile-menu-btn\s*\{[^}]*?display:\s*)none;',
            r'\1block;',
            content,
            flags=re.DOTALL
        )
        
        # 모바일 미디어 쿼리 안에서만 적용되도록 다시 확인
        # @media 안의 .mobile-menu-btn을 찾아서 display: block으로 설정
        if '@media (max-width: 768px)' in content:
            # 모바일 미디어 쿼리 안의 .mobile-menu-btn { display: none; }을 display: block으로 변경
            pattern = r'(@media\s*\(max-width:\s*768px\)[^}]*?\.mobile-menu-btn\s*\{[^}]*?display:\s*)none([^}]*?\})'
            replacement = r'\1block\2'
            content = re.sub(pattern, replacement, content, flags=re.DOTALL)
        
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
    print("\n💡 모바일 미디어 쿼리에서 햄버거 버튼이")
    print("   display: block이 되도록 수정\n")
    
    print("📝 파일 수정 중...\n")
    fixed_files = []
    
    for file in ALL_FILES:
        if fix_hamburger_display(file):
            fixed_files.append(file)
    
    print(f"\n✅ 총 {len(fixed_files)}개 파일 수정 완료!")
    print("=" * 60)


if __name__ == "__main__":
    main()

