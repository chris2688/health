import os
import re
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 수정할 파일 목록
ALL_FILES = [
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


def fix_absolute_links(filepath):
    """모든 절대 경로를 상대 경로로 변경"""
    if not os.path.exists(filepath):
        print(f"  ⚠️ 파일 없음: {filepath}")
        return False
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 모든 https://health9988234.mycafe24.com/ 절대 경로를 상대 경로로 변경
        # 단, 이미지나 외부 리소스는 제외
        
        # 1. HTML 파일 링크들
        content = re.sub(
            r'href="https://health9988234\.mycafe24\.com/([^"]+\.html)"',
            r'href="\1"',
            content
        )
        
        # 2. 카테고리 경로 링크들 (WordPress 카테고리 URL)
        # 이 링크들은 WordPress REST API를 통해 동적으로 로드되어야 하므로
        # 일단 그대로 두거나, 필요시 JavaScript로 처리
        
        # 3. index-v2.html 링크
        content = re.sub(
            r'href="https://health9988234\.mycafe24\.com/"',
            'href="index-v2.html"',
            content
        )
        content = re.sub(
            r'href="https://health9988234\.mycafe24\.com/index-v2\.html"',
            'href="index-v2.html"',
            content
        )
        
        # 4. food-main.html 링크
        content = re.sub(
            r'href="https://health9988234\.mycafe24\.com/food-main\.html"',
            'href="food-main.html"',
            content
        )
        
        # 5. exercise-main.html 링크
        content = re.sub(
            r'href="https://health9988234\.mycafe24\.com/exercise-main\.html"',
            'href="exercise-main.html"',
            content
        )
        
        # 6. lifestyle-main.html 링크
        content = re.sub(
            r'href="https://health9988234\.mycafe24\.com/lifestyle-main\.html"',
            'href="lifestyle-main.html"',
            content
        )
        
        # 7. news-main.html 링크
        content = re.sub(
            r'href="https://health9988234\.mycafe24\.com/news-main\.html"',
            'href="news-main.html"',
            content
        )
        
        # 8. 카테고리 파일 링크들
        content = re.sub(
            r'href="https://health9988234\.mycafe24\.com/category-([^"]+\.html)"',
            r'href="category-\1"',
            content
        )
        
        # 9. 서브카테고리 파일 링크들
        content = re.sub(
            r'href="https://health9988234\.mycafe24\.com/(food|exercise|lifestyle)-([^"]+\.html)"',
            r'href="\1-\2"',
            content
        )
        
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  ✅ {filepath} - 절대 경로 수정 완료")
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
    print("🔧 모든 파일 절대 경로를 상대 경로로 변경")
    print("=" * 60)
    print("\n💡 수정 사항:")
    print("   1. 모든 https://health9988234.mycafe24.com/ 절대 경로 제거")
    print("   2. HTML 파일 링크를 상대 경로로 변경\n")
    
    print("📝 파일 수정 중...\n")
    fixed_files = []
    
    for file in ALL_FILES:
        if fix_absolute_links(file):
            fixed_files.append(file)
    
    print(f"\n✅ 총 {len(fixed_files)}개 파일 수정 완료!")
    print("=" * 60)


if __name__ == "__main__":
    main()

