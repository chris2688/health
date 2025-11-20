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
]

def fix_category_links(filepath):
    """카테고리 링크 수정 - WordPress REST API로 변경"""
    if not os.path.exists(filepath):
        print(f"  ⚠️ 파일 없음: {filepath}")
        return False
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # WordPress 카테고리 URL을 REST API URL로 변경
        # 패턴: https://health9988234.mycafe24.com/category/...
        # 이 링크들은 JavaScript로 동적으로 처리되어야 하므로
        # 일단 REST API 엔드포인트로 변경하거나, 클릭 이벤트로 처리
        
        # 모든 카테고리 링크를 찾아서 처리
        # 하지만 이 링크들은 실제로는 JavaScript로 동적으로 로드되어야 함
        # 따라서 일단은 그대로 두고, JavaScript에서 처리하도록 함
        
        # 대신 href를 #으로 변경하고 data-category 속성 추가
        pattern = r'href="https://health9988234\.mycafe24\.com/category/([^"]+)"'
        
        def replace_link(match):
            category_path = match.group(1)
            # 카테고리 경로에서 카테고리 ID나 슬러그 추출
            # 예: 질환별-정보/심혈관-질환/고혈압 -> 고혈압
            parts = category_path.split('/')
            category_slug = parts[-1] if parts else category_path
            
            return f'href="#" data-category="{category_slug}" onclick="loadCategoryPosts(\'{category_slug}\'); return false;"'
        
        content = re.sub(pattern, replace_link, content)
        
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  ✅ {filepath} - 카테고리 링크 수정 완료")
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
    print("🔧 모든 파일 카테고리 링크 수정")
    print("=" * 60)
    print("\n💡 수정 사항:")
    print("   1. WordPress 카테고리 URL을 JavaScript 이벤트로 변경")
    print("   2. data-category 속성 추가\n")
    
    print("📝 파일 수정 중...\n")
    fixed_files = []
    
    for file in ALL_FILES:
        if fix_category_links(file):
            fixed_files.append(file)
    
    print(f"\n✅ 총 {len(fixed_files)}개 파일 수정 완료!")
    print("=" * 60)


if __name__ == "__main__":
    main()

