import os
import re
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 심혈관 질환 서브 카테고리 파일 목록
SUBCATEGORY_FILES = [
    'sub-고혈압.html',
    'sub-고지혈증.html',
    'sub-협심증심근경색.html',
    'sub-동맥경화.html',
    'sub-뇌졸중.html',
]

def fix_loadposts_call(filepath):
    """loadPosts 호출 부분 수정"""
    if not os.path.exists(filepath):
        return False
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 패턴: loadPosts([categorySlug], pageTitle);
        pattern = r'loadPosts\(\[categorySlug\], pageTitle\);'
        
        # 새로운 코드로 교체
        replacement = """// categorySlug가 배열이면 그대로, 아니면 배열로 변환
            if (categorySlug && !Array.isArray(categorySlug)) {
                categorySlug = [categorySlug];
            }
            
            loadPosts(categorySlug || [], pageTitle);"""
        
        if re.search(pattern, content):
            content = re.sub(pattern, replacement, content)
        
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
    print("🔧 서브 카테고리 파일 loadPosts 호출 수정")
    print("=" * 60)
    print(f"\n📝 총 {len(SUBCATEGORY_FILES)}개 파일 처리 중...\n")
    
    updated_count = 0
    
    for filename in SUBCATEGORY_FILES:
        if fix_loadposts_call(filename):
            print(f"  ✅ {filename} - 업데이트 완료")
            updated_count += 1
        else:
            print(f"  ℹ️ {filename} - 변경사항 없음 또는 파일 없음")
    
    print(f"\n✅ 총 {updated_count}개 파일 업데이트 완료!")
    print("=" * 60)

if __name__ == "__main__":
    main()

