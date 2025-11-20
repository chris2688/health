import os
import re
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 수정할 카테고리 파일 목록
CATEGORY_FILES = [
    "category-심혈관질환.html",
    "category-당뇨병.html",
    "category-관절근골격계.html",
    "category-호르몬내분비.html",
    "category-정신건강신경계.html",
    "category-소화기질환.html",
    "category-안과치과기타.html",
]


def fix_top_margin(filepath):
    """카테고리 파일의 상단 여백 수정"""
    if not os.path.exists(filepath):
        print(f"  ⚠️ 파일 없음: {filepath}")
        return False
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 1. container-content의 padding-top을 줄이기 (20px -> 0 또는 작은 값)
        content = re.sub(
            r'\.container-content\s*\{[^}]*padding:\s*20px\s+20px\s+60px;',
            '.container-content {\n            padding: 0 20px 60px;',
            content
        )
        
        # 2. section-title의 margin-bottom을 줄이기 (50px -> 30px 정도)
        content = re.sub(
            r'\.section-title\s*\{[^}]*margin-bottom:\s*50px;',
            '.section-title {\n            text-align: center;\n            margin-bottom: 30px;',
            content
        )
        
        # 3. 뒤로가기 버튼의 margin-top을 줄이기
        content = re.sub(
            r'\.back-button\s*\{[^}]*margin:\s*20px\s+0\s+30px\s+0;',
            '.back-button {\n            display: inline-block;\n            margin: 10px 0 20px 0;',
            content
        )
        
        # 4. health-card-container에 padding-top 추가하여 전체적으로 조정
        # 이미 padding: 0이면 padding-top만 추가
        if '.health-card-container' in content:
            # padding-top을 추가하거나 수정
            content = re.sub(
                r'\.health-card-container\s*\{[^}]*padding:\s*0;',
                '.health-card-container {\n            padding: 20px 0 0 0;',
                content
            )
        
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  ✅ {filepath} - 상단 여백 수정 완료")
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
    print("🔧 카테고리 페이지 상단 여백 조정")
    print("=" * 60)
    print("\n💡 다른 페이지들(food-main.html 등)과 동일한")
    print("   상단 여백으로 맞춥니다.\n")
    
    print("📝 파일 수정 중...\n")
    fixed_files = []
    
    for file in CATEGORY_FILES:
        if fix_top_margin(file):
            fixed_files.append(file)
    
    print(f"\n✅ 총 {len(fixed_files)}개 파일 수정 완료!")
    
    print("\n" + "=" * 60)
    print("✅ 수정 완료!")
    print("=" * 60)
    print("\n💡 수정된 내용:")
    print("   - container-content의 padding-top 제거")
    print("   - section-title의 margin-bottom 감소 (50px -> 30px)")
    print("   - 뒤로가기 버튼의 margin-top 감소 (20px -> 10px)")
    print("   - health-card-container에 padding-top 추가 (20px)")
    print("=" * 60)


if __name__ == "__main__":
    main()

