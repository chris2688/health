import os
import glob
import re
import sys
import io

# UTF-8 인코딩 설정
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

def improve_file(filepath):
    """파일의 자동 매핑과 정렬 로직 개선"""
    print(f"Processing: {filepath}")
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 이미 개선된 코드가 있으면 스킵
        if 'calculateSimilarity' in content and 'categorySimilarity' in content:
            print(f"  ⏭️  이미 개선된 코드가 있음, 스킵")
            return False
        
        # 포스트 점수 계산 부분 찾기
        old_score_calc = r"// 포스트 목록 렌더링 \(관련성 높은 순으로 정렬\)[\s\S]*?// 각 포스트의 관련성 점수 계산[\s\S]*?const pageTitleLower = pageTitle\.toLowerCase\(\);[\s\S]*?const pageTitleWords = pageTitleLower\.split\(/\[\\s\\-\\(\\)\\/\]\+/\)\.filter\(w => w\.length > 1\);[\s\S]*?const coreKeywords = pageTitleWords\.filter\(w => w\.length > 2\);[\s\S]*?const postsWithScore = posts\.map\(post => \{[\s\S]*?let score = 0;[\s\S]*?const postTitle = post\.title\.rendered\.toLowerCase\(\);[\s\S]*?const postCategories = post\.categories \|\| \[\];[\s\S]*?// 핵심 키워드가 하나도 없으면 0점[\s\S]*?if \(coreKeywords\.length > 0\) \{[\s\S]*?const hasCoreKeyword = coreKeywords\.some\(keyword => postTitle\.includes\(keyword\)\);[\s\S]*?if \(!hasCoreKeyword\) \{[\s\S]*?return \{ post, score: 0 \};[\s\S]*?\}[\s\S]*?\}[\s\S]*?// 페이지 제목과 포스트 제목의 유사도 계산[\s\S]*?if \(postTitle\.includes\(pageTitleLower\)\) \{[\s\S]*?score \+= 100;[\s\S]*?\} else \{[\s\S]*?// 핵심 키워드 매칭 점수[\s\S]*?let matchedCoreKeywords = 0;[\s\S]*?coreKeywords\.forEach\(keyword => \{[\s\S]*?if \(postTitle\.includes\(keyword\)\) \{[\s\S]*?matchedCoreKeywords\+\+;[\s\S]*?score \+= 30;[\s\S]*?\}[\s\S]*?\}\);[\s\S]*?// 일반 키워드 매칭 점수[\s\S]*?let matchedWords = 0;[\s\S]*?pageTitleWords\.forEach\(word => \{[\s\S]*?if \(word\.length > 1 && postTitle\.includes\(word\)\) \{[\s\S]*?matchedWords\+\+;[\s\S]*?score \+= 10;[\s\S]*?\}[\s\S]*?\}\);[\s\S]*?// 핵심 키워드의 80% 이상이 매칭되어야 최소 점수 부여[\s\S]*?if \(coreKeywords\.length > 0 && matchedCoreKeywords < coreKeywords\.length \* 0\.8\) \{[\s\S]*?score = Math\.max\(0, score - 50\);[\s\S]*?\}[\s\S]*?// 전체 키워드의 70% 이상이 매칭되어야 함[\s\S]*?if \(matchedWords < pageTitleWords\.length \* 0\.7\) \{[\s\S]*?score = Math\.max\(0, score - 30\);[\s\S]*?\}[\s\S]*?\}[\s\S]*?// 카테고리 매칭 점수[\s\S]*?if \(categoryIds\.length > 0 && postCategories\.includes\(categoryIds\[0\]\)\) \{[\s\S]*?score \+= 60;[\s\S]*?\}[\s\S]*?categoryIds\.slice\(1\)\.forEach\(catId => \{[\s\S]*?if \(postCategories\.includes\(catId\)\) \{[\s\S]*?score \+= 5;[\s\S]*?\}[\s\S]*?\}\);[\s\S]*?return \{ post, score \};[\s\S]*?\}\);[\s\S]*?// 관련성 점수가 너무 낮은 글 필터링[\s\S]*?const filteredPosts = postsWithScore\.filter\(\(\{ score \}\) => score >= [0-9]+\);[\s\S]*?// 점수 순으로 정렬[\s\S]*?filteredPosts\.sort\(\(a, b\) => b\.score - a\.score\);"
        
        new_score_calc = '''// 포스트 목록 렌더링 (관련성 높은 순으로 정렬)
                // 카테고리 이름 가져오기 (제목 유사도 계산용)
                const categoryNames = [];
                if (categoryIds.length > 0) {
                    try {
                        for (const catId of categoryIds) {
                            const catResponse = await fetch(`https://health9988234.mycafe24.com/wp-json/wp/v2/categories/${catId}`);
                            const catData = await catResponse.json();
                            if (catData && catData.name) {
                                categoryNames.push(catData.name.toLowerCase());
                            }
                        }
                    } catch (e) {
                        console.warn('Failed to fetch category names:', e);
                    }
                }
                
                // 각 포스트의 관련성 점수 계산 (카테고리 이름과 제목 유사도 우선)
                const pageTitleLower = pageTitle.toLowerCase();
                const pageTitleWords = pageTitleLower.split(/[\\s\\-\\(\\)\\/]+/).filter(w => w.length > 1);
                
                // 핵심 키워드 추출 (페이지 제목의 주요 단어, 3글자 이상)
                const coreKeywords = pageTitleWords.filter(w => w.length > 2);
                
                // 문자열 유사도 계산 함수 (간단한 Levenshtein 거리 기반)
                function calculateSimilarity(str1, str2) {
                    const s1 = str1.toLowerCase().replace(/\\s+/g, '');
                    const s2 = str2.toLowerCase().replace(/\\s+/g, '');
                    if (s1 === s2) return 1.0;
                    if (s1.includes(s2) || s2.includes(s1)) return 0.8;
                    
                    // 공통 문자 비율 계산
                    const longer = s1.length > s2.length ? s1 : s2;
                    const shorter = s1.length > s2.length ? s2 : s1;
                    let matches = 0;
                    for (let i = 0; i < shorter.length; i++) {
                        if (longer.includes(shorter[i])) matches++;
                    }
                    return matches / longer.length;
                }
                
                const postsWithScore = posts.map(post => {
                    let score = 0;
                    const postTitle = post.title.rendered;
                    const postTitleLower = postTitle.toLowerCase();
                    const postCategories = post.categories || [];
                    
                    // 1. 카테고리 이름과 제목 유사도 (최우선) - 가장 높은 점수
                    let maxCategorySimilarity = 0;
                    categoryNames.forEach(catName => {
                        const similarity = calculateSimilarity(catName, postTitle);
                        if (similarity > maxCategorySimilarity) {
                            maxCategorySimilarity = similarity;
                        }
                    });
                    // 카테고리 이름과 제목이 유사할수록 높은 점수 (최대 200점)
                    score += maxCategorySimilarity * 200;
                    
                    // 2. 페이지 제목과 포스트 제목의 유사도 (두 번째 우선)
                    const titleSimilarity = calculateSimilarity(pageTitleLower, postTitleLower);
                    score += titleSimilarity * 150; // 최대 150점
                    
                    // 3. 페이지 제목 정확 일치 보너스
                    if (postTitleLower.includes(pageTitleLower) || pageTitleLower.includes(postTitleLower)) {
                        score += 100; // 정확히 일치하면 추가 점수
                    }
                    
                    // 4. 핵심 키워드 매칭 점수
                    let matchedCoreKeywords = 0;
                    coreKeywords.forEach(keyword => {
                        if (postTitleLower.includes(keyword)) {
                            matchedCoreKeywords++;
                            score += 30; // 핵심 키워드 매칭 시 높은 점수
                        }
                    });
                    
                    // 5. 일반 키워드 매칭 점수
                    let matchedWords = 0;
                    pageTitleWords.forEach(word => {
                        if (word.length > 1 && postTitleLower.includes(word)) {
                            matchedWords++;
                            score += 10; // 일반 키워드 매칭 시 낮은 점수
                        }
                    });
                    
                    // 6. 카테고리 ID 매칭 점수
                    if (categoryIds.length > 0 && postCategories.includes(categoryIds[0])) {
                        score += 50; // 첫 번째 카테고리 매칭
                    }
                    categoryIds.slice(1).forEach(catId => {
                        if (postCategories.includes(catId)) {
                            score += 10; // 다른 카테고리 매칭
                        }
                    });
                    
                    // 핵심 키워드가 하나도 없으면 점수 감소
                    if (coreKeywords.length > 0 && matchedCoreKeywords === 0) {
                        score = Math.max(0, score * 0.3); // 점수 대폭 감소
                    }
                    
                    return { post, score, categorySimilarity: maxCategorySimilarity, titleSimilarity };
                });
                
                // 관련성 점수가 너무 낮은 글 필터링 (최소 50점 이상)
                const filteredPosts = postsWithScore.filter(({ score }) => score >= 50);
                
                // 정렬: 카테고리 유사도 > 제목 유사도 > 점수 순
                filteredPosts.sort((a, b) => {
                    // 1순위: 카테고리 이름과 제목 유사도
                    if (Math.abs(a.categorySimilarity - b.categorySimilarity) > 0.1) {
                        return b.categorySimilarity - a.categorySimilarity;
                    }
                    // 2순위: 페이지 제목과 제목 유사도
                    if (Math.abs(a.titleSimilarity - b.titleSimilarity) > 0.1) {
                        return b.titleSimilarity - a.titleSimilarity;
                    }
                    // 3순위: 총 점수
                    return b.score - a.score;
                });'''
        
        if re.search(old_score_calc, content, flags=re.DOTALL):
            content = re.sub(old_score_calc, new_score_calc, content, flags=re.DOTALL)
            print(f"  ✅ 점수 계산 및 정렬 로직 개선")
        else:
            print(f"  ⚠️  점수 계산 부분을 찾을 수 없음")
            return False
        
        # 로그 메시지 업데이트
        old_log = r"console\.log\(`Filtered posts:.*?min score: [0-9]+`\);[\s\S]*?console\.log\(`Core keywords:.*?`\);"
        new_log = '''console.log(`Filtered posts: ${filteredPosts.length} out of ${posts.length} (min score: 50)`);
                console.log(`Core keywords: ${coreKeywords.join(', ')}`);
                console.log(`Category names: ${categoryNames.join(', ')}`);
                console.log(`📊 정렬 기준: 카테고리 이름 유사도 > 페이지 제목 유사도 > 점수`);'''
        
        if re.search(old_log, content, flags=re.DOTALL):
            content = re.sub(old_log, new_log, content, flags=re.DOTALL)
            print(f"  ✅ 로그 메시지 업데이트")
        
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
    print("🚀 자동 매핑 및 정렬 개선 - 카테고리 이름 유사도 우선")
    print("=" * 60)
    
    # news-main.html과 모든 sub-*.html 파일 처리
    target_files = ['news-main.html'] + glob.glob("sub-*.html")
    
    print(f"\n📁 총 {len(target_files)}개 파일")
    
    success_count = 0
    for file in target_files:
        if improve_file(file):
            success_count += 1
    
    print("\n" + "=" * 60)
    print(f"✅ 완료: {success_count}/{len(target_files)}개 파일")
    print("=" * 60)
    print("\n📝 개선사항:")
    print("  ✅ 카테고리 이름과 제목 유사도 계산 추가")
    print("  ✅ 정렬 기준: 카테고리 유사도 > 제목 유사도 > 점수")
    print("  ✅ 가장 유사한 글이 상단 좌측부터 표시")

if __name__ == "__main__":
    main()

