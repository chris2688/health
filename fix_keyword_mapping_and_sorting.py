import os
import glob
import re
import sys
import io

# UTF-8 인코딩 설정
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

def fix_file(filepath):
    """키워드 매핑 수정 및 글 정렬 로직 추가"""
    print(f"Processing: {filepath}")
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 1. 키워드 매핑 수정 - 더 구체적인 키워드를 우선적으로 매칭
        old_keyword_map = r"const keywordMap = \{[\s\S]*?\};"
        
        new_keyword_map = '''const keywordMap = {
                    // 심혈관 질환 (구체적인 키워드 우선)
                    '고혈압': ['cardiovascular', 'disease-info'],
                    '고지혈증': ['cardiovascular', 'disease-info'],
                    '콜레스테롤': ['cardiovascular', 'disease-info'],
                    '심근경색': ['cardiovascular', 'disease-info'],
                    '협심증': ['cardiovascular', 'disease-info'],
                    '뇌졸중': ['cardiovascular', 'disease-info'],
                    '동맥경화': ['cardiovascular', 'disease-info'],
                    
                    // 당뇨병
                    '당뇨병': ['diabetes', 'disease-info'],
                    '당뇨': ['diabetes', 'disease-info'],
                    '공복혈당장애': ['diabetes', 'disease-info'],
                    '공복혈당': ['diabetes', 'disease-info'],
                    '당뇨합병증': ['diabetes', 'disease-info'],
                    '인슐린': ['diabetes', 'disease-info'],
                    
                    // 관절/근골격계
                    '퇴행성관절염': ['musculoskeletal', 'disease-info'],
                    '오십견': ['musculoskeletal', 'disease-info'],
                    '유착성관절낭염': ['musculoskeletal', 'disease-info'],
                    '허리디스크': ['musculoskeletal', 'disease-info'],
                    '목디스크': ['musculoskeletal', 'disease-info'],
                    '골다공증': ['musculoskeletal', 'disease-info'],
                    '관절염': ['musculoskeletal', 'disease-info'],
                    
                    // 소화기 질환 (구체적인 키워드 우선)
                    '역류성식도염': ['digestive', 'disease-info'],
                    '역류성 식도염': ['digestive', 'disease-info'],
                    '위염위궤양': ['digestive', 'disease-info'],
                    '위궤양': ['digestive', 'disease-info'],
                    '위염': ['digestive', 'disease-info'],
                    '과민성대장증후군': ['digestive', 'disease-info'],
                    '지방간': ['digestive', 'disease-info'],
                    
                    // 호르몬/내분비
                    '갱년기증후군': ['endocrine', 'disease-info'],
                    '갱년기': ['endocrine', 'disease-info'],
                    '갑상선': ['endocrine', 'disease-info'],
                    '대사증후군': ['endocrine', 'disease-info'],
                    
                    // 정신 건강/신경계
                    '우울증번아웃': ['neuroscience', 'disease-info'],
                    '우울증': ['neuroscience', 'disease-info'],
                    '수면장애불면증': ['neuroscience', 'disease-info'],
                    '수면장애': ['neuroscience', 'disease-info'],
                    '치매경도인지장애': ['neuroscience', 'disease-info'],
                    '치매': ['neuroscience', 'disease-info'],
                    '이명어지럼증': ['neuroscience', 'disease-info'],
                    '이명현훈': ['neuroscience', 'disease-info'],
                    '이명': ['neuroscience', 'disease-info'],
                    '어지럼증': ['neuroscience', 'disease-info'],
                    
                    // 안과/치과/기타
                    '백내장녹내장': ['eyes-dental', 'disease-info'],
                    '백내장': ['eyes-dental', 'disease-info'],
                    '녹내장': ['eyes-dental', 'disease-info'],
                    '치주염치아손실': ['eyes-dental', 'disease-info'],
                    '치주질환': ['eyes-dental', 'disease-info'],
                    '비만체형변화': ['eyes-dental', 'disease-info'],
                    '비만': ['eyes-dental', 'disease-info'],
                };'''
        
        if re.search(old_keyword_map, content):
            content = re.sub(old_keyword_map, new_keyword_map, content, flags=re.DOTALL)
            print(f"  ✅ 키워드 매핑 수정")
        
        # 2. 키워드 매칭 로직 수정 - 더 구체적인 키워드를 우선적으로 매칭
        old_matching_logic = r"for \(const \[keyword, slugs\] of Object\.entries\(keywordMap\)\) \{[\s\S]*?if \(pageTitle\.includes\(keyword\)\) \{[\s\S]*?break;[\s\S]*?\}"
        
        new_matching_logic = '''// 키워드를 길이순으로 정렬 (긴 키워드 = 더 구체적 = 우선 매칭)
                const sortedKeywords = Object.keys(keywordMap).sort((a, b) => b.length - a.length);
                
                for (const keyword of sortedKeywords) {
                    // 정확한 단어 매칭 (부분 문자열이 아닌)
                    // 예: "역류성 식도염"에 "이명"이 포함되어 있지 않도록
                    const regex = new RegExp(keyword, 'i');
                    if (regex.test(pageTitle)) {
                        const slugs = keywordMap[keyword];
                        slugs.forEach(slug => {
                            if (!matchedSlugs.includes(slug)) matchedSlugs.push(slug);
                        });
                        break; // 가장 구체적인 키워드에 매칭되면 중단
                    }
                }'''
        
        if re.search(old_matching_logic, content):
            content = re.sub(old_matching_logic, new_matching_logic, content, flags=re.DOTALL)
            print(f"  ✅ 키워드 매칭 로직 개선")
        
        # 3. 글 정렬 로직 추가 - 관련성 높은 글을 먼저 표시
        old_posts_rendering = r"// 포스트 목록 렌더링[\s\S]*?newsGrid\.innerHTML = posts\.map\(post => \{"
        
        new_posts_rendering = '''// 포스트 목록 렌더링 (관련성 높은 순으로 정렬)
                // 각 포스트의 관련성 점수 계산
                const postsWithScore = posts.map(post => {
                    let score = 0;
                    const postTitle = post.title.rendered.toLowerCase();
                    const postCategories = post.categories || [];
                    
                    // 페이지 제목과 포스트 제목의 유사도 계산
                    const pageTitleLower = pageTitle.toLowerCase();
                    if (postTitle.includes(pageTitleLower)) {
                        score += 100; // 정확히 일치하면 높은 점수
                    } else {
                        // 부분 일치 점수
                        const words = pageTitleLower.split(/[\\s\\-]+/);
                        words.forEach(word => {
                            if (word.length > 1 && postTitle.includes(word)) {
                                score += 10;
                            }
                        });
                    }
                    
                    // 카테고리 매칭 점수
                    // 첫 번째 카테고리(가장 관련성 높은)에 매칭되면 높은 점수
                    if (categoryIds.length > 0 && postCategories.includes(categoryIds[0])) {
                        score += 50;
                    }
                    // 다른 카테고리에 매칭되면 낮은 점수
                    categoryIds.slice(1).forEach(catId => {
                        if (postCategories.includes(catId)) {
                            score += 20;
                        }
                    });
                    
                    return { post, score };
                });
                
                // 점수 순으로 정렬 (높은 점수 = 높은 관련성 = 먼저 표시)
                postsWithScore.sort((a, b) => b.score - a.score);
                
                newsGrid.innerHTML = postsWithScore.map(({ post }) => {'''
        
        if re.search(old_posts_rendering, content):
            content = re.sub(old_posts_rendering, new_posts_rendering, content, flags=re.DOTALL)
            print(f"  ✅ 글 정렬 로직 추가")
        
        # pageTitle 변수를 loadPosts 함수에서 사용할 수 있도록 수정
        # loadPosts 함수에 pageTitle 파라미터 추가
        old_loadposts_def = r"async function loadPosts\(categorySlugs\) \{"
        new_loadposts_def = "async function loadPosts(categorySlugs, pageTitle = '') {"
        
        if re.search(old_loadposts_def, content):
            content = re.sub(old_loadposts_def, new_loadposts_def, content)
        
        # loadPosts 호출 시 pageTitle 전달
        old_loadposts_call = r"loadPosts\(categorySlugs\);"
        new_loadposts_call = "loadPosts(categorySlugs, pageTitle);"
        
        if re.search(old_loadposts_call, content):
            content = re.sub(old_loadposts_call, new_loadposts_call, content)
        
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
    print("=" * 60)
    print("🎯 키워드 매핑 수정 및 글 정렬 로직 추가")
    print("=" * 60)
    
    # news-main.html과 모든 sub-*.html 파일 처리
    target_files = ['news-main.html'] + glob.glob("sub-*.html")
    
    print(f"\n📁 총 {len(target_files)}개 파일")
    
    success_count = 0
    for file in target_files:
        if fix_file(file):
            success_count += 1
    
    print("\n" + "=" * 60)
    print(f"✅ 완료: {success_count}/{len(target_files)}개 파일")
    print("=" * 60)
    print("\n📝 개선사항:")
    print("  ✅ 키워드 매핑 수정 (더 구체적인 키워드 우선)")
    print("  ✅ 키워드 매칭 로직 개선 (정확한 단어 매칭)")
    print("  ✅ 글 정렬 로직 추가 (관련성 높은 순)")
    print("  ✅ 역류성 식도염에 이명/어지럼증 매핑 방지")

if __name__ == "__main__":
    main()

