import os
import glob
import re
import json
import sys
import io

# UTF-8 인코딩 설정
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 워드프레스 카테고리 데이터 로드
with open('wordpress_categories.json', 'r', encoding='utf-8') as f:
    wp_categories = json.load(f)

def get_page_title(filepath):
    """HTML 파일에서 페이지 제목 추출"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # <h1 class="page-title">제목</h1> 찾기
        match = re.search(r'<h1 class="page-title">(.*?)</h1>', content)
        if match:
            return match.group(1).strip()
        
        # <title>제목</title> 찾기
        match = re.search(r'<title>(.*?)(?:\s*-\s*9988.*?)?</title>', content)
        if match:
            return match.group(1).strip()
        
        return None
    except:
        return None

def find_matching_category(page_title):
    """페이지 제목과 워드프레스 카테고리 매칭"""
    if not page_title:
        return None
    
    # 정확히 일치하는 카테고리 찾기
    for cat in wp_categories:
        if cat['name'] == page_title:
            return cat['slug']
    
    # 부분 일치 찾기 (예: "고혈압"이 "고혈압 관리"에 포함)
    for cat in wp_categories:
        if page_title in cat['name'] or cat['name'] in page_title:
            return cat['slug']
    
    # 키워드 매칭 (예: "고혈압" → "cardiovascular" 검색)
    keywords = {
        '고혈압': 'cardiovascular',
        '당뇨': 'diabetes',
        '고지혈증': 'cardiovascular',
        '심근경색': 'cardiovascular',
        '협심증': 'cardiovascular',
        '뇌졸중': 'cardiovascular',
        '동맥경화': 'cardiovascular',
        '관절염': 'musculoskeletal',
        '퇴행성관절염': 'musculoskeletal',
        '오십견': 'musculoskeletal',
        '허리디스크': 'musculoskeletal',
        '골다공증': 'musculoskeletal',
        '위염': 'digestive',
        '역류성식도염': 'digestive',
        '과민성대장증후군': 'digestive',
        '지방간': 'digestive',
        '갑상선': 'endocrine',
        '갱년기': 'endocrine',
        '대사증후군': 'endocrine',
        '우울증': 'neuroscience',
        '수면장애': 'neuroscience',
        '치매': 'neuroscience',
        '이명': 'neuroscience',
        '백내장': 'eyes-dental',
        '녹내장': 'eyes-dental',
        '치주염': 'eyes-dental',
        '비만': 'eyes-dental',
    }
    
    for keyword, slug in keywords.items():
        if keyword in page_title:
            return slug
    
    return None

def update_page_with_smart_mapping(filepath):
    """페이지에 스마트 카테고리 매핑 추가"""
    print(f"Processing: {filepath}")
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 페이지 제목 가져오기
        page_title = get_page_title(filepath)
        print(f"  페이지 제목: {page_title}")
        
        # 매칭되는 카테고리 찾기
        category_slug = find_matching_category(page_title)
        
        if category_slug:
            print(f"  ✅ 매칭된 카테고리: {category_slug}")
        else:
            print(f"  ⚠️  매칭되는 카테고리를 찾지 못했습니다")
            category_slug = None
        
        # 스마트 매핑 함수 추가
        smart_mapping_script = '''
        // 스마트 카테고리 매핑 함수
        async function findCategoryByPageTitle(pageTitle) {
            if (!pageTitle) return null;
            
            try {
                // 워드프레스에서 모든 카테고리 가져오기
                const response = await fetch('https://health9988234.mycafe24.com/wp-json/wp/v2/categories?per_page=100');
                const categories = await response.json();
                
                // 정확히 일치하는 카테고리 찾기
                let matched = categories.find(cat => cat.name === pageTitle);
                if (matched) return matched.slug;
                
                // 부분 일치 찾기
                matched = categories.find(cat => 
                    cat.name.includes(pageTitle) || pageTitle.includes(cat.name)
                );
                if (matched) return matched.slug;
                
                // 키워드 매칭
                const keywordMap = {
                    '고혈압': 'cardiovascular',
                    '당뇨': 'diabetes',
                    '고지혈증': 'cardiovascular',
                    '심근경색': 'cardiovascular',
                    '협심증': 'cardiovascular',
                    '뇌졸중': 'cardiovascular',
                    '동맥경화': 'cardiovascular',
                    '관절염': 'musculoskeletal',
                    '퇴행성관절염': 'musculoskeletal',
                    '오십견': 'musculoskeletal',
                    '허리디스크': 'musculoskeletal',
                    '골다공증': 'musculoskeletal',
                    '위염': 'digestive',
                    '역류성식도염': 'digestive',
                    '과민성대장증후군': 'digestive',
                    '지방간': 'digestive',
                    '갑상선': 'endocrine',
                    '갱년기': 'endocrine',
                    '대사증후군': 'endocrine',
                    '우울증': 'neuroscience',
                    '수면장애': 'neuroscience',
                    '치매': 'neuroscience',
                    '이명': 'neuroscience',
                    '백내장': 'eyes-dental',
                    '녹내장': 'eyes-dental',
                    '치주염': 'eyes-dental',
                    '비만': 'eyes-dental',
                };
                
                for (const [keyword, slug] of Object.entries(keywordMap)) {
                    if (pageTitle.includes(keyword)) {
                        return slug;
                    }
                }
                
                return null;
            } catch (error) {
                console.error('Category mapping error:', error);
                return null;
            }
        }
        '''
        
        # 기존 pageToCategory 객체 찾기
        old_pattern = r'const pageToCategory = \{.*?\};'
        
        # 페이지 제목 기반 자동 매핑으로 변경
        new_mapping = f'''            // 페이지 제목 기반 자동 카테고리 매핑
            const pageTitle = document.querySelector('.page-title')?.textContent?.trim() || 
                             document.querySelector('h1')?.textContent?.trim() || '';
            
            // 먼저 페이지 제목으로 카테고리 찾기
            let categorySlug = await findCategoryByPageTitle(pageTitle);
            
            // 찾지 못하면 하드코딩된 매핑 사용
            if (!categorySlug) {{
                const pageToCategory = {{
                    'news-main.html': 'health-news',
                    'sub-고혈압.html': 'cardiovascular',
                    'sub-당뇨.html': 'diabetes',
                    'sub-고지혈증.html': 'cardiovascular',
                    // 필요한 매핑 추가...
                }};
                
                const currentPage = window.location.pathname.split('/').pop();
                categorySlug = pageToCategory[currentPage] || null;
            }}
            
            loadPosts(categorySlug);'''
        
        # 기존 DOMContentLoaded 이벤트 핸들러 수정
        old_domready = r'document\.addEventListener\(''DOMContentLoaded'', function\(\) \{.*?loadPosts\(categorySlug\);\s*\}\);'
        
        if re.search(old_domready, content, re.DOTALL):
            # 스마트 매핑 함수 추가
            if 'async function findCategoryByPageTitle' not in content:
                # </script> 전에 스마트 매핑 함수 추가
                content = re.sub(
                    r'(</script>)',
                    smart_mapping_script + r'\1',
                    content,
                    count=1
                )
            
            # DOMContentLoaded 이벤트 핸들러 교체
            content = re.sub(
                old_domready,
                'document.addEventListener(\'DOMContentLoaded\', async function() {' + new_mapping + '\n        });',
                content,
                flags=re.DOTALL
            )
            
            # 파일 저장
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"  ✅ 스마트 매핑 추가 완료!")
            return True
        else:
            print(f"  ⚠️  DOMContentLoaded 핸들러를 찾을 수 없음")
            return False
        
    except Exception as e:
        print(f"  ❌ 오류: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("=" * 60)
    print("🧠 스마트 카테고리 매핑 추가")
    print("=" * 60)
    
    # news-main.html과 모든 sub-*.html 파일 처리
    target_files = ['news-main.html'] + glob.glob("sub-*.html")
    
    print(f"\n📁 총 {len(target_files)}개 파일")
    
    success_count = 0
    for file in target_files:
        if update_page_with_smart_mapping(file):
            success_count += 1
    
    print("\n" + "=" * 60)
    print(f"✅ 완료: {success_count}/{len(target_files)}개 파일")
    print("=" * 60)
    print("\n📝 개선사항:")
    print("  ✅ 페이지 제목 기반 자동 카테고리 매핑")
    print("  ✅ 워드프레스 카테고리와 자동 매칭")
    print("  ✅ 키워드 기반 폴백 매핑")
    print("  ✅ 하드코딩된 매핑도 유지 (백업)")

if __name__ == "__main__":
    main()

