import os
import glob
import sys
import io
import shutil

# UTF-8 인코딩 설정
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

def update_file(filepath):
    """파일을 sub-역류성식도염.html과 동일하게 수정"""
    print(f"Processing: {filepath}")
    
    try:
        # sub-역류성식도염.html에서 개선된 스크립트 복사
        with open('sub-역류성식도염.html', 'r', encoding='utf-8') as f:
            reference_content = f.read()
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 이미 수정되었는지 확인
        if 'async function loadPosts(categorySlugs)' in content and 'categorySlugs.length > 0' in content:
            print(f"  ⏭️  이미 수정됨, 스킵")
            return False
        
        # findCategoryByPageTitle 함수 추출
        ref_start = reference_content.find('// 페이지 제목 기반 카테고리 자동 매핑')
        ref_end = reference_content.find('// 페이지 로드 시 실행', ref_start)
        new_find_category = reference_content[ref_start:ref_end]
        
        # loadPosts 함수 추출
        ref_start2 = reference_content.find('// 워드프레스 REST API로 포스트 목록 가져오기 (여러 카테고리 지원)')
        ref_end2 = reference_content.find('// 페이지 제목 기반 카테고리 자동 매핑', ref_start2)
        new_load_posts = reference_content[ref_start2:ref_end2]
        
        # DOMContentLoaded 부분 추출
        ref_start3 = reference_content.find('// 페이지 로드 시 실행')
        ref_end3 = reference_content.find('</script>', ref_start3)
        new_dom_ready = reference_content[ref_start3:ref_end3]
        
        # 기존 함수들 교체
        # 1. findCategoryByPageTitle
        old_find = r'// 페이지 제목 기반 카테고리 자동 매핑.*?return null;[\s\S]*?\}'
        if re.search(old_find, content, re.DOTALL):
            content = re.sub(old_find, new_find_category, content, flags=re.DOTALL)
        
        # 2. loadPosts
        old_load = r'// 워드프레스 REST API로 포스트 목록 가져오기.*?async function loadPosts\(categorySlug\) \{.*?if \(categorySlug\) \{[\s\S]*?apiUrl \+= `&categories=\$\{categories\[0\]\.id\}`;[\s\S]*?\}'
        if re.search(old_load, content, re.DOTALL):
            content = re.sub(old_load, new_load_posts, content, flags=re.DOTALL)
        
        # 3. DOMContentLoaded
        old_dom = r'// 페이지 로드 시 실행.*?loadPosts\(categorySlug\);'
        if re.search(old_dom, content, re.DOTALL):
            content = re.sub(old_dom, new_dom_ready, content, flags=re.DOTALL)
        
        # 파일 저장
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"  ✅ 완료!")
        return True
        
    except Exception as e:
        print(f"  ❌ 오류: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    import re
    
    print("=" * 60)
    print("🔍 모든 페이지에 여러 카테고리 동시 검색 적용")
    print("=" * 60)
    
    # sub-역류성식도염.html 제외 (이미 수정됨)
    target_files = ['news-main.html'] + [f for f in glob.glob("sub-*.html") if f != 'sub-역류성식도염.html']
    
    print(f"\n📁 총 {len(target_files)}개 파일")
    
    success_count = 0
    for file in target_files:
        if update_file(file):
            success_count += 1
    
    print("\n" + "=" * 60)
    print(f"✅ 완료: {success_count}/{len(target_files)}개 파일")
    print("=" * 60)

if __name__ == "__main__":
    main()

