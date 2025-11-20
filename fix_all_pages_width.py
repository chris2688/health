import os
import re
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 수정할 파일 목록
CATEGORY_FILES = [
    "category-심혈관질환.html",
    "category-당뇨병.html",
    "category-관절근골격계.html",
    "category-호르몬내분비.html",
    "category-정신건강신경계.html",
    "category-소화기질환.html",
    "category-안과치과기타.html",
]

MAIN_FILES = [
    "food-main.html",
    "exercise-main.html",
    "lifestyle-main.html",
    "news-main.html",
]

SUBCATEGORY_FILES = [
    "food-피해야할과일.html",
    "food-질환별식단.html",
    "food-모르면독이된다.html",
    "exercise-질환별운동가이드.html",
    "exercise-운동팁.html",
    "lifestyle-생활습관.html",
    "lifestyle-생활습관바꾸기팁.html",
]

ALL_FILES = CATEGORY_FILES + MAIN_FILES + SUBCATEGORY_FILES


def fix_page_width(filepath):
    """페이지의 가로폭을 메인 화면과 동일하게 수정"""
    if not os.path.exists(filepath):
        print(f"  ⚠️ 파일 없음: {filepath}")
        return False
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 1. container-content의 max-width를 1200px -> 1400px로 변경
        content = re.sub(
            r'\.container-content\s*\{[^}]*max-width:\s*1200px;',
            '.container-content {\n            padding: 0 20px 60px;\n            max-width: 1400px;',
            content,
            flags=re.DOTALL
        )
        
        # 2. health-cards-grid의 max-width를 1200px -> 1400px로 변경
        content = re.sub(
            r'\.health-cards-grid\s*\{[^}]*max-width:\s*1200px;',
            '.health-cards-grid {\n            display: grid;\n            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));\n            gap: 30px;\n            max-width: 1400px;',
            content,
            flags=re.DOTALL
        )
        
        # 3. health-card의 크기를 메인 화면과 동일하게 (padding, min-height)
        # minmax(250px -> 300px로 변경)
        content = re.sub(
            r'grid-template-columns:\s*repeat\(auto-fit,\s*minmax\(250px,\s*1fr\)\);',
            'grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));',
            content
        )
        
        # 4. health-card의 padding과 min-height를 메인 화면과 동일하게
        content = re.sub(
            r'\.health-card\s*\{[^}]*padding:\s*40px\s+30px;',
            '.health-card {\n            position: relative;\n            padding: 45px 35px;',
            content,
            flags=re.DOTALL
        )
        
        content = re.sub(
            r'min-height:\s*200px;',
            'min-height: 240px;',
            content
        )
        
        # 5. health-card-icon 크기 조정 (56px -> 메인과 동일하게 유지하거나 조정)
        # card-icon과 동일하게 맞추기
        content = re.sub(
            r'\.health-card-icon\s*\{[^}]*font-size:\s*56px;',
            '.health-card-icon {\n            font-size: 56px;\n            margin-bottom: 20px;',
            content,
            flags=re.DOTALL
        )
        
        # 6. health-card h3 크기 조정 (22px -> 26px)
        content = re.sub(
            r'\.health-card\s+h3\s*\{[^}]*font-size:\s*22px;',
            '.health-card h3 {\n            font-size: 26px;',
            content,
            flags=re.DOTALL
        )
        
        # 7. health-card-container의 padding 조정 (메인과 동일하게)
        # 메인 화면은 hero-section이 있고, 카테고리 페이지는 health-card-container가 있음
        # padding은 유지하되, 전체적인 레이아웃을 맞춤
        
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  ✅ {filepath} - 가로폭 수정 완료")
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
    print("🔧 모든 페이지의 가로폭을 메인 화면과 동일하게 수정")
    print("=" * 60)
    print("\n💡 메인 화면(index-v2.html)의 가로폭(max-width: 1400px)을")
    print("   기준으로 모든 페이지를 통일합니다.\n")
    
    print("📝 파일 수정 중...\n")
    fixed_files = []
    
    for file in ALL_FILES:
        if fix_page_width(file):
            fixed_files.append(file)
    
    print(f"\n✅ 총 {len(fixed_files)}개 파일 수정 완료!")
    
    print("\n" + "=" * 60)
    print("✅ 수정 완료!")
    print("=" * 60)
    print("\n💡 수정된 내용:")
    print("   - container-content: max-width 1200px -> 1400px")
    print("   - health-cards-grid: max-width 1200px -> 1400px")
    print("   - 카드 최소 너비: 250px -> 300px")
    print("   - 카드 padding: 40px 30px -> 45px 35px")
    print("   - 카드 min-height: 200px -> 240px")
    print("   - 카드 제목 크기: 22px -> 26px")
    print("=" * 60)


if __name__ == "__main__":
    main()

