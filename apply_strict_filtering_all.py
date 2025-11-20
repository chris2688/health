import os
import glob
import re
import sys
import io

# UTF-8 인코딩 설정
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

def fix_file(filepath):
    """파일의 필터링 로직을 더 엄격하게 수정"""
    print(f"Processing: {filepath}")
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 이미 강화된 필터링이 있으면 스킵
        if 'coreKeywords' in content and 'score >= 70' in content:
            print(f"  ⏭️  이미 강화된 필터링이 있음, 스킵")
            return False
        
        # 1. pageTitleWords 분리자에 '/' 추가
        old_split = r"pageTitleWords = pageTitleLower\.split\(/\[\\s\\-\\(\\)\]\+/\)"
        new_split = r"pageTitleWords = pageTitleLower.split(/[\\s\\-\\(\\)\\/]+/)"
        if re.search(old_split, content):
            content = re.sub(old_split, new_split, content)
        
        # 2. 핵심 키워드 추출 로직 추가
        old_title_words = r"const pageTitleWords = pageTitleLower\.split\(/\[\\s\\-\\(\\)\]\+/\)\.filter\(w => w\.length > 1\);"
        new_title_words = r"const pageTitleWords = pageTitleLower.split(/[\\s\\-\\(\\)\\/]+/).filter(w => w.length > 1);\n                \n                // 핵심 키워드 추출 (페이지 제목의 주요 단어, 3글자 이상)\n                const coreKeywords = pageTitleWords.filter(w => w.length > 2);"
        if re.search(old_title_words, content):
            content = re.sub(old_title_words, new_title_words, content)
        
        # 3. 핵심 키워드 체크 로직 추가 (posts.map 내부)
        old_map_start = r"const postsWithScore = posts\.map\(post => \{[\s\S]*?let score = 0;"
        new_map_start = r"const postsWithScore = posts.map(post => {\n                    let score = 0;\n                    const postTitle = post.title.rendered.toLowerCase();\n                    const postCategories = post.categories || [];\n                    \n                    // 핵심 키워드가 하나도 없으면 0점 (완전 차단)\n                    if (coreKeywords.length > 0) {\n                        const hasCoreKeyword = coreKeywords.some(keyword => postTitle.includes(keyword));\n                        if (!hasCoreKeyword) {\n                            return { post, score: 0 }; // 핵심 키워드가 없으면 즉시 제외\n                        }\n                    }"
        
        if re.search(old_map_start, content):
            content = re.sub(old_map_start, new_map_start, content, flags=re.DOTALL)
        
        # 4. 점수 계산 로직 개선
        old_score_calc = r"// 핵심 키워드가 모두 포함되어야 점수 부여[\s\S]*?let matchedWords = 0;[\s\S]*?pageTitleWords\.forEach\(word => \{[\s\S]*?score \+= 15;[\s\S]*?\}\);[\s\S]*?// 핵심 키워드의.*?매칭되어야 최소 점수 부여[\s\S]*?if \(matchedWords < pageTitleWords\.length \* 0\.[0-9]+\) \{[\s\S]*?score = 0;"
        
        new_score_calc = '''// 핵심 키워드 매칭 점수
                        let matchedCoreKeywords = 0;
                        coreKeywords.forEach(keyword => {
                            if (postTitle.includes(keyword)) {
                                matchedCoreKeywords++;
                                score += 30; // 핵심 키워드 매칭 시 높은 점수
                            }
                        });
                        
                        // 일반 키워드 매칭 점수
                        let matchedWords = 0;
                        pageTitleWords.forEach(word => {
                            if (word.length > 1 && postTitle.includes(word)) {
                                matchedWords++;
                                score += 10; // 일반 키워드 매칭 시 낮은 점수
                            }
                        });
                        
                        // 핵심 키워드의 80% 이상이 매칭되어야 최소 점수 부여
                        if (coreKeywords.length > 0 && matchedCoreKeywords < coreKeywords.length * 0.8) {
                            score = Math.max(0, score - 50); // 점수 대폭 감소
                        }
                        
                        // 전체 키워드의 70% 이상이 매칭되어야 함
                        if (matchedWords < pageTitleWords.length * 0.7) {
                            score = Math.max(0, score - 30); // 점수 추가 감소
                        }'''
        
        if re.search(old_score_calc, content):
            content = re.sub(old_score_calc, new_score_calc, content, flags=re.DOTALL)
        
        # 5. 카테고리 점수 상향
        old_cat_score1 = r"score \+= 50;"
        new_cat_score1 = "score += 60; // 점수 상향"
        if re.search(old_cat_score1, content):
            content = re.sub(old_cat_score1, new_cat_score1, content, count=1)  # 첫 번째만
        
        # 6. 최소 점수 기준 상향
        old_min_score = r"score >= [0-9]+"
        new_min_score = "score >= 70"
        if re.search(old_min_score, content):
            content = re.sub(old_min_score, new_min_score, content)
        
        # 7. 필터링 메시지 업데이트
        old_msg = r"min score: [0-9]+"
        new_msg = "min score: 70"
        if re.search(old_msg, content):
            content = re.sub(old_msg, new_msg, content)
        
        # 8. 핵심 키워드 로그 추가
        old_log = r"console\.log\(`Filtered posts:"
        new_log = r"console.log(`Core keywords: ${coreKeywords.join(', ')}`);\n                console.log(`Filtered posts:"
        if re.search(old_log, content):
            content = re.sub(old_log, new_log, content)
        
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
    print("🔒 모든 페이지에 강화된 필터링 적용")
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
    print("  ✅ 핵심 키워드 체크 (없으면 즉시 제외)")
    print("  ✅ 최소 점수 기준 상향 (70점 이상)")
    print("  ✅ 핵심 키워드 80% 이상 매칭 필수")
    print("  ✅ 전체 키워드 70% 이상 매칭 필수")

if __name__ == "__main__":
    main()

