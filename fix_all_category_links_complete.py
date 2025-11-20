import os
import re
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 카테고리 매핑 (URL 경로 -> 슬러그)
CATEGORY_MAPPING = {
    '고혈압': '고혈압',
    '고지혈증-콜레스테롤': '고지혈증-콜레스테롤',
    '협심증-심근경색': '협심증-심근경색',
    '동맥경화': '동맥경화',
    '뇌졸중': '뇌졸중',
}

# 수정할 파일 목록
ALL_FILES = [
    "category-심혈관질환.html",
    "category-당뇨병.html",
    "category-관절근골격계.html",
    "category-호르몬내분비.html",
    "category-정신건강신경계.html",
    "category-소화기질환.html",
    "category-안과치과기타.html",
]

def fix_category_links_complete(filepath):
    """카테고리 링크 완전 수정"""
    if not os.path.exists(filepath):
        print(f"  ⚠️ 파일 없음: {filepath}")
        return False
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 모든 WordPress 카테고리 URL을 찾아서 수정
        # 패턴: href="https://health9988234.mycafe24.com/category/..."
        pattern = r'href="https://health9988234\.mycafe24\.com/category/([^"]+)"'
        
        def replace_link(match):
            category_path = match.group(1)
            # 카테고리 경로에서 마지막 부분 추출
            # 예: 질환별-정보/심혈관-질환/고혈압 -> 고혈압
            parts = category_path.rstrip('/').split('/')
            category_slug = parts[-1] if parts else category_path
            
            return f'href="#" data-category="{category_slug}" onclick="loadCategoryPosts(\'{category_slug}\'); return false;"'
        
        content = re.sub(pattern, replace_link, content)
        
        # REST API URL도 수정
        content = re.sub(
            r'href="https://health9988234\.mycafe24\.com/wp-json/wp/v2/posts\?categories=([^"]+)"',
            r'href="#" data-category="\1" onclick="loadCategoryPosts(\'\1\'); return false;"',
            content
        )
        
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
    print("🔧 모든 파일 카테고리 링크 완전 수정")
    print("=" * 60)
    print("\n💡 수정 사항:")
    print("   1. WordPress 카테고리 URL을 JavaScript 이벤트로 변경")
    print("   2. 카테고리 슬러그 올바르게 설정\n")
    
    print("📝 파일 수정 중...\n")
    fixed_files = []
    
    for file in ALL_FILES:
        if fix_category_links_complete(file):
            fixed_files.append(file)
    
    print(f"\n✅ 총 {len(fixed_files)}개 파일 수정 완료!")
    print("=" * 60)


if __name__ == "__main__":
    main()

