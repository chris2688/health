import os
import glob
import re
import sys
import io

# UTF-8 인코딩 설정
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 개선된 카테고리 매핑 (여러 카테고리 동시 검색 가능)
IMPROVED_CATEGORY_MAPPING = {
    # 심혈관 질환 관련
    '고혈압': ['cardiovascular', 'disease-info'],
    '고지혈증': ['cardiovascular', 'disease-info'],
    '콜레스테롤': ['cardiovascular', 'disease-info'],
    '심근경색': ['cardiovascular', 'disease-info'],
    '협심증': ['cardiovascular', 'disease-info'],
    '뇌졸중': ['cardiovascular', 'disease-info'],
    '동맥경화': ['cardiovascular', 'disease-info'],
    
    # 당뇨병 관련
    '당뇨': ['diabetes', 'disease-info'],
    '공복혈당': ['diabetes', 'disease-info'],
    '인슐린': ['diabetes', 'disease-info'],
    '혈당': ['diabetes', 'disease-info'],
    '당뇨병': ['diabetes', 'disease-info'],
    '당뇨합병증': ['diabetes', 'disease-info'],
    
    # 관절/근골격계 관련
    '관절염': ['musculoskeletal', 'disease-info'],
    '퇴행성관절염': ['musculoskeletal', 'disease-info'],
    '오십견': ['musculoskeletal', 'disease-info'],
    '허리디스크': ['musculoskeletal', 'disease-info'],
    '골다공증': ['musculoskeletal', 'disease-info'],
    
    # 소화기 질환 관련 (여러 카테고리 동시 검색)
    '위염': ['digestive', 'disease-info'],
    '위궤양': ['digestive', 'disease-info'],
    '역류성식도염': ['digestive', 'disease-info'],  # 소화기 + 질환별 정보
    '역류': ['digestive', 'disease-info'],
    '식도염': ['digestive', 'disease-info'],
    '과민성대장증후군': ['digestive', 'disease-info'],
    '지방간': ['digestive', 'disease-info'],
    
    # 호르몬/내분비 관련
    '갑상선': ['endocrine', 'disease-info'],
    '갱년기': ['endocrine', 'disease-info'],
    '대사증후군': ['endocrine', 'disease-info'],
    
    # 정신 건강/신경계 관련
    '우울증': ['neuroscience', 'disease-info'],
    '수면장애': ['neuroscience', 'disease-info'],
    '치매': ['neuroscience', 'disease-info'],
    '이명': ['neuroscience', 'disease-info'],
    
    # 안과/치과/기타 관련
    '백내장': ['eyes-dental', 'disease-info'],
    '녹내장': ['eyes-dental', 'disease-info'],
    '치주염': ['eyes-dental', 'disease-info'],
    '비만': ['eyes-dental', 'disease-info'],
}

def update_load_posts_function(filepath):
    """loadPosts 함수를 여러 카테고리 동시 검색으로 수정"""
    print(f"Processing: {filepath}")
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # loadPosts 함수 수정 (여러 카테고리 ID 지원)
        old_loadposts = r'async function loadPosts\(categorySlug\) \{'
        
        if not re.search(old_loadposts, content):
            print(f"  ⚠️  loadPosts 함수를 찾을 수 없음")
            return False
        
        # 여러 카테고리 슬러그를 받도록 수정
        new_loadposts_start = '''async function loadPosts(categorySlugs) {
            // categorySlugs는 문자열(단일) 또는 배열(다중) 가능
            if (typeof categorySlugs === 'string') {
                categorySlugs = [categorySlugs];
            } else if (!categorySlugs) {
                categorySlugs = [];
            }'''
        
        # 기존 loadPosts 함수의 카테고리 처리 부분 찾기
        old_cat_processing = r'if \(categorySlug\) \{[\s\S]*?apiUrl \+= `&categories=\$\{categories\[0\]\.id\}`;[\s\S]*?\}'
        
        new_cat_processing = '''if (categorySlugs.length > 0) {
                // 여러 카테고리 ID 가져오기
                const categoryIds = [];
                for (const slug of categorySlugs) {
                    try {
                        const catResponse = await fetch(`https://health9988234.mycafe24.com/wp-json/wp/v2/categories?slug=${encodeURIComponent(slug)}`);
                        const categories = await catResponse.json();
                        if (categories.length > 0) {
                            categoryIds.push(categories[0].id);
                        }
                    } catch (e) {
                        console.error(`Category fetch error for ${slug}:`, e);
                    }
                }
                
                if (categoryIds.length > 0) {
                    // 여러 카테고리 ID를 쉼표로 구분하여 전달
                    apiUrl += `&categories=${categoryIds.join(',')}`;
                }
            }'''
        
        # 함수 시작 부분 교체
        content = re.sub(old_loadposts, new_loadposts_start, content)
        
        # 카테고리 처리 부분 교체
        content = re.sub(old_cat_processing, new_cat_processing, content, flags=re.DOTALL)
        
        # findCategoryByPageTitle 함수 수정 (여러 카테고리 반환)
        old_find_category = r'async function findCategoryByPageTitle\(pageTitle\) \{[\s\S]*?return null;[\s\S]*?\}'
        
        new_find_category = '''async function findCategoryByPageTitle(pageTitle) {
            if (!pageTitle) return [];
            
            try {
                // 워드프레스에서 모든 카테고리 가져오기
                const response = await fetch('https://health9988234.mycafe24.com/wp-json/wp/v2/categories?per_page=100');
                const categories = await response.json();
                
                const matchedSlugs = [];
                
                // 정확히 일치하는 카테고리 찾기
                let matched = categories.find(cat => cat.name === pageTitle);
                if (matched) {
                    matchedSlugs.push(matched.slug);
                    // 상위 카테고리도 추가
                    if (matched.parent > 0) {
                        const parent = categories.find(cat => cat.id === matched.parent);
                        if (parent && !matchedSlugs.includes(parent.slug)) {
                            matchedSlugs.push(parent.slug);
                        }
                    }
                }
                
                // 부분 일치 찾기
                matched = categories.find(cat => 
                    (cat.name.includes(pageTitle) || pageTitle.includes(cat.name)) && 
                    !matchedSlugs.includes(cat.slug)
                );
                if (matched) {
                    matchedSlugs.push(matched.slug);
                    if (matched.parent > 0) {
                        const parent = categories.find(cat => cat.id === matched.parent);
                        if (parent && !matchedSlugs.includes(parent.slug)) {
                            matchedSlugs.push(parent.slug);
                        }
                    }
                }
                
                // 키워드 기반 매핑 (여러 카테고리 반환)
                const keywordMap = {
                    '고혈압': ['cardiovascular', 'disease-info'],
                    '고지혈증': ['cardiovascular', 'disease-info'],
                    '당뇨': ['diabetes', 'disease-info'],
                    '관절염': ['musculoskeletal', 'disease-info'],
                    '위염': ['digestive', 'disease-info'],
                    '역류성식도염': ['digestive', 'disease-info'],
                    '역류': ['digestive', 'disease-info'],
                    '식도염': ['digestive', 'disease-info'],
                    '갑상선': ['endocrine', 'disease-info'],
                    '우울증': ['neuroscience', 'disease-info'],
                    '백내장': ['eyes-dental', 'disease-info'],
                    // ... 기존 키워드들도 유지
                };
                
                for (const [keyword, slugs] of Object.entries(keywordMap)) {
                    if (pageTitle.includes(keyword)) {
                        slugs.forEach(slug => {
                            if (!matchedSlugs.includes(slug)) {
                                matchedSlugs.push(slug);
                            }
                        });
                        break;
                    }
                }
                
                return matchedSlugs.length > 0 ? matchedSlugs : [];
            } catch (error) {
                console.error('Category mapping error:', error);
                return [];
            }
        }'''
        
        # findCategoryByPageTitle 함수 교체
        content = re.sub(old_find_category, new_find_category, content, flags=re.DOTALL)
        
        # DOMContentLoaded에서 loadPosts 호출 부분 수정
        old_loadposts_call = r'let categorySlug = await findCategoryByPageTitle\(pageTitle\);[\s\S]*?loadPosts\(categorySlug\);'
        
        new_loadposts_call = '''let categorySlugs = await findCategoryByPageTitle(pageTitle);
            
            // 찾지 못하면 하드코딩된 매핑 사용 (백업)
            if (categorySlugs.length === 0) {
                const pageToCategory = {
                    'news-main.html': ['health-news'],
                    'sub-고혈압.html': ['cardiovascular', 'disease-info'],
                    'sub-당뇨.html': ['diabetes', 'disease-info'],
                    'sub-역류성식도염.html': ['digestive', 'disease-info'],
                };
                
                const currentPage = window.location.pathname.split('/').pop();
                categorySlugs = pageToCategory[currentPage] || [];
            }
            
            console.log('페이지 제목:', pageTitle);
            console.log('매칭된 카테고리:', categorySlugs);
            
            loadPosts(categorySlugs);'''
        
        content = re.sub(old_loadposts_call, new_loadposts_call, content, flags=re.DOTALL)
        
        # 파일 저장
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"  ✅ 여러 카테고리 동시 검색으로 수정 완료!")
        return True
        
    except Exception as e:
        print(f"  ❌ 오류: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("=" * 60)
    print("🔍 여러 카테고리 동시 검색 기능 추가")
    print("=" * 60)
    
    # news-main.html과 모든 sub-*.html 파일 처리
    target_files = ['news-main.html'] + glob.glob("sub-*.html")
    
    print(f"\n📁 총 {len(target_files)}개 파일")
    
    success_count = 0
    for file in target_files:
        if update_load_posts_function(file):
            success_count += 1
    
    print("\n" + "=" * 60)
    print(f"✅ 완료: {success_count}/{len(target_files)}개 파일")
    print("=" * 60)
    print("\n📝 개선사항:")
    print("  ✅ 여러 카테고리 동시 검색 지원")
    print("  ✅ 역류성 식도염 → digestive + disease-info 동시 검색")
    print("  ✅ 연관된 모든 글 표시 (중복 허용)")

if __name__ == "__main__":
    main()

