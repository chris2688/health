import os
import re
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 서브 카테고리별 WordPress 카테고리 매핑 (배열로)
SUBCATEGORY_MAPPING = {
    # 심혈관 질환
    'sub-고혈압.html': ['고혈압', 'cardiovascular', '심혈관-질환'],
    'sub-고지혈증.html': ['고지혈증', 'hyperlipidemia', 'cardiovascular', '심혈관-질환'],
    'sub-협심증심근경색.html': ['협심증', '심근경색', 'cardiovascular', '심혈관-질환'],
    'sub-동맥경화.html': ['동맥경화', 'cardiovascular', '심혈관-질환'],
    'sub-뇌졸중.html': ['뇌졸중', 'stroke', 'cardiovascular', '심혈관-질환'],
}

def update_sub_file(filepath):
    """서브 카테고리 파일의 매핑 업데이트"""
    if not os.path.exists(filepath):
        return False
    
    filename = os.path.basename(filepath)
    if filename not in SUBCATEGORY_MAPPING:
        return False
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # categorySlugs 배열 가져오기
        category_slugs = SUBCATEGORY_MAPPING[filename]
        
        # pageToCategory 매핑을 배열로 변경
        # 패턴: const pageToCategory = { ... };
        pattern = r'const pageToCategory = \{([^}]+)\};'
        
        # 새로운 매핑 생성 (배열로)
        mapping_value = '[' + ', '.join([f"'{slug}'" for slug in category_slugs]) + ']'
        new_mapping = f"const pageToCategory = {{\n                    '{filename}': {mapping_value}\n                }};"
        
        if re.search(pattern, content):
            # 기존 매핑 교체
            content = re.sub(pattern, new_mapping, content, flags=re.DOTALL)
        
        # categorySlug를 배열로 처리하도록 수정
        # 패턴: categorySlug = pageToCategory[currentPage] || null;
        pattern2 = r"categorySlug = pageToCategory\[currentPage\] \|\| null;"
        replacement = """categorySlug = pageToCategory[currentPage] || null;
                // 배열이면 그대로, 문자열이면 배열로 변환
                if (categorySlug && !Array.isArray(categorySlug)) {
                    categorySlug = [categorySlug];
                }"""
        
        if re.search(pattern2, content):
            content = re.sub(pattern2, replacement, content)
        
        # loadPosts 호출 시 배열로 전달
        pattern3 = r"loadPosts\(\[categorySlug\], pageTitle\);"
        if not re.search(pattern3, content):
            pattern4 = r"loadPosts\(categorySlug, pageTitle\);"
            if re.search(pattern4, content):
                content = re.sub(pattern4, "loadPosts(categorySlug || [], pageTitle);", content)
        
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
        
    except Exception as e:
        print(f"  ❌ {filepath} - 오류: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """메인 실행"""
    print("=" * 60)
    print("🔧 심혈관 질환 서브 카테고리 파일 글 매핑 최종 수정")
    print("=" * 60)
    print(f"\n📝 총 {len(SUBCATEGORY_MAPPING)}개 파일 처리 중...\n")
    
    updated_count = 0
    
    for filename in SUBCATEGORY_MAPPING.keys():
        if update_sub_file(filename):
            print(f"  ✅ {filename} - 업데이트 완료")
            updated_count += 1
        else:
            print(f"  ℹ️ {filename} - 변경사항 없음")
    
    print(f"\n✅ 총 {updated_count}개 파일 업데이트 완료!")
    print("=" * 60)

if __name__ == "__main__":
    main()

