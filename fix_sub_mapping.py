import os
import re
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 서브 카테고리별 WordPress 카테고리 매핑
SUBCATEGORY_MAPPING = {
    # 심혈관 질환
    'sub-고혈압.html': ['고혈압', 'cardiovascular', '심혈관-질환'],
    'sub-고지혈증.html': ['고지혈증', 'hyperlipidemia', 'cardiovascular', '심혈관-질환'],
    'sub-협심증심근경색.html': ['협심증', '심근경색', 'cardiovascular', '심혈관-질환'],
    'sub-동맥경화.html': ['동맥경화', 'cardiovascular', '심혈관-질환'],
    'sub-뇌졸중.html': ['뇌졸중', 'stroke', 'cardiovascular', '심혈관-질환'],
    
    # 당뇨병
    'sub-당뇨.html': ['당뇨', 'diabetes', '당뇨병'],
    'sub-공복혈당장애.html': ['공복혈당', 'diabetes', '당뇨병'],
    'sub-당뇨병합병증.html': ['당뇨병합병증', 'diabetes', '당뇨병'],
    
    # 관절/근골격계
    'sub-관절염.html': ['관절염', 'musculoskeletal', '관절-근골격계-질환'],
    'sub-퇴행성관절염.html': ['퇴행성관절염', 'musculoskeletal', '관절-근골격계-질환'],
    'sub-허리디스크.html': ['허리디스크', 'musculoskeletal', '관절-근골격계-질환'],
    'sub-허리디스크목디스크.html': ['허리디스크', '목디스크', 'musculoskeletal', '관절-근골격계-질환'],
    'sub-골다공증.html': ['골다공증', 'musculoskeletal', '관절-근골격계-질환'],
    'sub-오십견.html': ['오십견', 'musculoskeletal', '관절-근골격계-질환'],
    
    # 호르몬/내분비
    'sub-갱년기.html': ['갱년기', 'endocrine', '호르몬-내분비-질환'],
    'sub-갱년기증후군.html': ['갱년기', 'endocrine', '호르몬-내분비-질환'],
    'sub-갑상선.html': ['갑상선', 'endocrine', '호르몬-내분비-질환'],
    'sub-대사증후군.html': ['대사증후군', 'endocrine', '호르몬-내분비-질환'],
    
    # 정신건강/신경계
    'sub-우울증.html': ['우울증', 'neuroscience', '정신-건강-신경계'],
    'sub-우울증번아웃.html': ['우울증', '번아웃', 'neuroscience', '정신-건강-신경계'],
    'sub-치매.html': ['치매', 'neuroscience', '정신-건강-신경계'],
    'sub-치매경도인지장애.html': ['치매', '인지장애', 'neuroscience', '정신-건강-신경계'],
    'sub-수면장애.html': ['수면장애', 'neuroscience', '정신-건강-신경계'],
    'sub-수면장애불면증.html': ['수면장애', '불면증', 'neuroscience', '정신-건강-신경계'],
    'sub-불안장애.html': ['불안장애', 'neuroscience', '정신-건강-신경계'],
    
    # 소화기 질환
    'sub-위염.html': ['위염', 'digestive', '소화기-질환'],
    'sub-위염위궤양.html': ['위염', '위궤양', 'digestive', '소화기-질환'],
    'sub-위염역류식.html': ['위염', '역류성식도염', 'digestive', '소화기-질환'],
    'sub-역류성식도염.html': ['역류성식도염', 'digestive', '소화기-질환'],
    'sub-지방간.html': ['지방간', 'digestive', '소화기-질환'],
    'sub-과민성대장증후군.html': ['과민성대장증후군', 'digestive', '소화기-질환'],
    'sub-대장암.html': ['대장암', 'digestive', '소화기-질환'],
    
    # 안과/치과/기타
    'sub-백내장.html': ['백내장', 'eyes-dental', '안과-치과-기타'],
    'sub-녹내장.html': ['녹내장', 'eyes-dental', '안과-치과-기타'],
    'sub-백내장녹내장.html': ['백내장', '녹내장', 'eyes-dental', '안과-치과-기타'],
    'sub-치주질환.html': ['치주질환', 'eyes-dental', '안과-치과-기타'],
    'sub-치주염치아손실.html': ['치주염', '치아손실', 'eyes-dental', '안과-치과-기타'],
    'sub-이명현훈.html': ['이명', '현훈', 'eyes-dental', '안과-치과-기타'],
    'sub-이명어지럼증.html': ['이명', '어지럼증', 'eyes-dental', '안과-치과-기타'],
    'sub-비만.html': ['비만', 'eyes-dental', '안과-치과-기타'],
    'sub-비만체형변화.html': ['비만', '체형변화', 'eyes-dental', '안과-치과-기타'],
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
        
        # pageToCategory 매핑 찾기 및 업데이트
        category_slugs = SUBCATEGORY_MAPPING[filename]
        
        # 패턴: const pageToCategory = { ... };
        pattern = r'const pageToCategory = \{([^}]+)\};'
        
        # 새로운 매핑 생성
        mapping_items = []
        for slug in category_slugs:
            # 파일명을 키로 사용
            mapping_items.append(f"'{filename}': '{slug}'")
        
        new_mapping = f"const pageToCategory = {{\n                    {',  // '.join(mapping_items)}\n                }};"
        
        if re.search(pattern, content):
            # 기존 매핑 교체
            content = re.sub(pattern, new_mapping, content, flags=re.DOTALL)
        else:
            # 매핑이 없으면 추가 (if (!categorySlug) { 다음에)
            pattern2 = r'(if \(!categorySlug\) \{[^}]*const pageToCategory = )\{[^}]+\}([^}]*\})'
            if re.search(pattern2, content):
                content = re.sub(pattern2, r'\1' + new_mapping + r'\2', content, flags=re.DOTALL)
            else:
                # 다른 위치에 추가
                pattern3 = r'(if \(!categorySlug\) \{[\s\S]*?)(const pageToCategory = \{[\s\S]*?\};)'
                if re.search(pattern3, content):
                    content = re.sub(pattern3, r'\1' + new_mapping, content)
        
        # loadPosts 호출 시 배열로 전달되도록 수정
        pattern4 = r"loadPosts\(\[categorySlug\], pageTitle\);"
        if re.search(pattern4, content):
            # 이미 배열로 되어 있음
            pass
        else:
            pattern5 = r"loadPosts\(categorySlug, pageTitle\);"
            if re.search(pattern5, content):
                content = re.sub(pattern5, "loadPosts([categorySlug], pageTitle);", content)
        
        # categorySlug를 배열로 변경
        # loadPosts 호출 전에 categorySlug를 배열로 변환
        pattern6 = r'(console\.log\([\'"]매칭된 카테고리[\'"], categorySlug\);\s*\n\s*)loadPosts'
        if re.search(pattern6, content):
            replacement = r'\1if (categorySlug && !Array.isArray(categorySlug)) {\n                categorySlug = [categorySlug];\n            }\n            loadPosts'
            content = re.sub(pattern6, replacement, content)
        
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
    print("🔧 서브 카테고리 파일 글 매핑 업데이트")
    print("=" * 60)
    print(f"\n📝 총 {len(SUBCATEGORY_MAPPING)}개 파일 처리 중...\n")
    
    updated_count = 0
    
    for filename in SUBCATEGORY_MAPPING.keys():
        if update_sub_file(filename):
            print(f"  ✅ {filename} - 업데이트 완료")
            updated_count += 1
        else:
            print(f"  ℹ️ {filename} - 변경사항 없음 또는 파일 없음")
    
    print(f"\n✅ 총 {updated_count}개 파일 업데이트 완료!")
    print("=" * 60)

if __name__ == "__main__":
    main()

