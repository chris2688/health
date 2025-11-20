import os
import glob
import re
import sys
import io

# UTF-8 인코딩 설정
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

def fix_file(filepath):
    """파일의 카테고리 매핑 수정"""
    print(f"Processing: {filepath}")
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 1. 키워드 매핑에서 'disease-info' 제거
        # 'disease-info'가 포함된 배열을 찾아서 제거
        content = re.sub(
            r"(\['[^']+',\s*)'disease-info'(\])",
            r'\1\2',
            content
        )
        content = re.sub(
            r"(\['disease-info',\s*'[^']+'\])",
            r"['\1']",
            content
        )
        # 더 간단하게: 배열에서 'disease-info' 제거
        content = re.sub(
            r"\[('[^']+'),\s*'disease-info'\]",
            r"[\1]",
            content
        )
        content = re.sub(
            r"\['disease-info',\s*('[^']+')\]",
            r"[\1]",
            content
        )
        
        # 2. 상위 카테고리 제외 로직 추가
        # 정확히 일치하는 카테고리 찾기 부분 수정
        old_exact_match = r"let matched = categories\.find\(cat => cat\.name === pageTitle\);"
        new_exact_match = r"let matched = categories.find(cat => cat.name === pageTitle && cat.slug !== 'disease-info');"
        if re.search(old_exact_match, content):
            content = re.sub(old_exact_match, new_exact_match, content)
        
        # 상위 카테고리 추가 부분 제거
        old_parent_add = r"// 상위 카테고리도 추가[\s\S]*?if \(matched\.parent > 0\) \{[\s\S]*?matchedSlugs\.push\(parent\.slug\);[\s\S]*?\}"
        new_parent_comment = r"// 상위 카테고리는 추가하지 않음 (너무 광범위함)"
        if re.search(old_parent_add, content):
            content = re.sub(old_parent_add, new_parent_comment, content, flags=re.DOTALL)
        
        # 부분 일치 찾기 부분 수정
        old_partial_match = r"matched = categories\.find\(cat =>[\s\S]*?!matchedSlugs\.includes\(cat\.slug\)[\s\S]*?\);"
        if re.search(old_partial_match, content):
            # disease-info 제외 추가
            content = re.sub(
                r"(!matchedSlugs\.includes\(cat\.slug\))",
                r"\1 && cat.slug !== 'disease-info'",
                content
            )
        
        # 3. 글 필터링 로직 추가 (이미 있으면 스킵)
        if 'const filteredPosts = postsWithScore.filter' not in content:
            # postsWithScore.sort 바로 앞에 필터링 추가
            old_sort = r"// 점수 순으로 정렬[\s\S]*?postsWithScore\.sort\(\(a, b\) => b\.score - a\.score\);"
            new_filter_sort = '''// 관련성 점수가 너무 낮은 글 필터링 (최소 20점 이상)
                const filteredPosts = postsWithScore.filter(({ score }) => score >= 20);
                
                // 점수 순으로 정렬 (높은 점수 = 높은 관련성 = 먼저 표시)
                filteredPosts.sort((a, b) => b.score - a.score);
                
                console.log(`Filtered posts: ${filteredPosts.length} out of ${posts.length} (min score: 20)`);
                
                // 필터링된 포스트가 없으면 메시지 표시
                if (filteredPosts.length === 0) {
                    newsGrid.innerHTML = `
                        <div class="no-posts-message" style="grid-column: 1 / -1;">
                            <p>📝 관련된 글이 없습니다</p>
                            <p style="font-size: 14px; margin-top: 10px; color: #ccc;">곧 업데이트될 예정입니다</p>
                        </div>
                    `;
                    return;
                }'''
            
            if re.search(old_sort, content):
                content = re.sub(old_sort, new_filter_sort, content, flags=re.DOTALL)
                # postsWithScore를 filteredPosts로 변경
                content = re.sub(
                    r"newsGrid\.innerHTML = postsWithScore\.map",
                    "newsGrid.innerHTML = filteredPosts.map",
                    content
                )
        
        # 4. 관련성 점수 계산 로직 개선 (이미 있으면 스킵)
        if 'pageTitleWords.forEach' not in content:
            # pageTitleLower 정의 바로 다음에 pageTitleWords 추가
            old_title_lower = r"const pageTitleLower = pageTitle\.toLowerCase\(\);"
            new_title_words = r"const pageTitleLower = pageTitle.toLowerCase();\n                const pageTitleWords = pageTitleLower.split(/[\\s\\-\\(\\)]+/).filter(w => w.length > 1);"
            if re.search(old_title_lower, content):
                content = re.sub(old_title_lower, new_title_words, content)
            
            # 점수 계산 로직 개선
            old_score_calc = r"// 부분 일치 점수[\s\S]*?words\.forEach\(word => \{[\s\S]*?score \+= 10;[\s\S]*?\}\);"
            new_score_calc = '''// 핵심 키워드가 모두 포함되어야 점수 부여
                        let matchedWords = 0;
                        pageTitleWords.forEach(word => {
                            if (word.length > 1 && postTitle.includes(word)) {
                                matchedWords++;
                                score += 15; // 단어별 점수 증가
                            }
                        });
                        
                        // 핵심 키워드의 50% 이상이 매칭되어야 최소 점수 부여
                        if (matchedWords < pageTitleWords.length * 0.5) {
                            score = 0; // 관련성 너무 낮으면 0점
                        }'''
            
            if re.search(old_score_calc, content):
                content = re.sub(old_score_calc, new_score_calc, content, flags=re.DOTALL)
        
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
    print("🎯 모든 페이지의 카테고리 매핑 수정 (관련 없는 글 제거)")
    print("=" * 60)
    
    # sub-역류성식도염.html 제외 (이미 수정됨)
    target_files = ['news-main.html'] + [f for f in glob.glob("sub-*.html") if f != 'sub-역류성식도염.html']
    
    print(f"\n📁 총 {len(target_files)}개 파일")
    
    success_count = 0
    for file in target_files:
        if fix_file(file):
            success_count += 1
    
    print("\n" + "=" * 60)
    print(f"✅ 완료: {success_count}/{len(target_files)}개 파일")
    print("=" * 60)
    print("\n📝 개선사항:")
    print("  ✅ 상위 카테고리 'disease-info' 제거")
    print("  ✅ 구체적인 하위 카테고리만 사용")
    print("  ✅ 관련성 점수 필터링 (최소 20점 이상)")
    print("  ✅ 핵심 키워드 50% 이상 매칭 필수")

if __name__ == "__main__":
    main()

