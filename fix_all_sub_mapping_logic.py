import os
import re
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 모든 서브 카테고리 매핑
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

def generate_page_to_category_mapping():
    """pageToCategory 매핑 객체 생성"""
    lines = []
    for filename, slugs in SUBCATEGORY_MAPPING.items():
        slugs_str = ', '.join([f"'{slug}'" for slug in slugs])
        lines.append(f"                '{filename}': [{slugs_str}],")
    return '\n'.join(lines)

def update_sub_file(filepath):
    """서브 카테고리 파일의 매핑 로직 수정"""
    if not os.path.exists(filepath):
        return False
    
    filename = os.path.basename(filepath)
    if filename not in SUBCATEGORY_MAPPING:
        return False
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # DOMContentLoaded 이벤트 핸들러 찾기
        pattern = r'(// 페이지 로드 시 실행\s+document\.addEventListener\([\'"]DOMContentLoaded[\'"], async function\(\) \{[\s\S]*?)(loadPosts\([^)]+\);[\s\S]*?\}\);[\s\S]*?</script>)'
        
        # 새로운 로직 생성
        new_logic = f'''        // 페이지 로드 시 실행
        document.addEventListener('DOMContentLoaded', async function() {{
            // 페이지 제목 가져오기
            const pageTitle = document.querySelector('.page-title')?.textContent?.trim() || 
                             document.querySelector('h1')?.textContent?.trim() || '';
            
            // 하드코딩된 매핑 사용 (우선순위)
            const pageToCategory = {{
{generate_page_to_category_mapping()}
            }};
            
            // 현재 페이지 파일명 가져오기
            let currentPage = window.location.pathname.split('/').pop() || window.location.href.split('/').pop();
            if (!currentPage || !currentPage.endsWith('.html')) {{
                currentPage = '{filename}'; // 기본값
            }}
            
            // 매핑에서 카테고리 가져오기
            let categorySlug = pageToCategory[currentPage];
            
            // 매핑에 없으면 페이지 제목으로 자동 찾기 시도
            if (!categorySlug) {{
                try {{
                    const foundSlug = await findCategoryByPageTitle(pageTitle);
                    if (foundSlug) {{
                        categorySlug = [foundSlug];
                    }}
                }} catch (error) {{
                    console.warn('자동 매핑 실패, 기본값 사용:', error);
                }}
            }}
            
            // 배열이 아니면 배열로 변환
            if (categorySlug && !Array.isArray(categorySlug)) {{
                categorySlug = [categorySlug];
            }}
            
            console.log('페이지 제목:', pageTitle);
            console.log('현재 페이지:', currentPage);
            console.log('매칭된 카테고리:', categorySlug);
            
            loadPosts(categorySlug || [], pageTitle);
        }});'''
        
        if re.search(pattern, content):
            content = re.sub(pattern, new_logic + r'\2', content, flags=re.DOTALL)
        else:
            # 다른 패턴 시도
            pattern2 = r'(document\.addEventListener\([\'"]DOMContentLoaded[\'"], async function\(\) \{[\s\S]*?)(loadPosts\([^)]+\);[\s\S]*?\}\);[\s\S]*?</script>)'
            if re.search(pattern2, content):
                content = re.sub(pattern2, new_logic + r'\2', content, flags=re.DOTALL)
        
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
    print("🔧 모든 서브 카테고리 파일 매핑 로직 수정")
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

