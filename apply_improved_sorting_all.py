import os
import glob
import re
import sys
import io

# UTF-8 인코딩 설정
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

def get_improved_code():
    """개선된 코드 반환"""
    return '''                // 포스트 목록 렌더링 (관련성 높은 순으로 정렬)
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
                });
                
                console.log(`Filtered posts: ${filteredPosts.length} out of ${posts.length} (min score: 50)`);
                console.log(`Core keywords: ${coreKeywords.join(', ')}`);
                console.log(`Category names: ${categoryNames.join(', ')}`);
                console.log(`📊 정렬 기준: 카테고리 이름 유사도 > 페이지 제목 유사도 > 점수`);
                
                // 필터링된 포스트가 없으면 메시지 표시
                if (filteredPosts.length === 0) {
                    newsGrid.innerHTML = `
                        <div class="no-posts-message" style="grid-column: 1 / -1;">
                            <p>📝 관련된 글이 없습니다</p>
                            <p style="font-size: 14px; margin-top: 10px; color: #ccc;">곧 업데이트될 예정입니다</p>
                        </div>
                    `;
                    return;
                }
                
                newsGrid.innerHTML = filteredPosts.map(({ post }) => {
                    const thumbnail = getThumbnailUrl(post);
                    const title = post.title.rendered;
                    const date = new Date(post.date).toLocaleDateString('ko-KR');
                    const backUrl = encodeURIComponent(window.location.pathname.split('/').pop());
                    
                    return `
                        <a href="post-detail.html?id=${post.id}&back=${backUrl}" class="news-item">
                            <div class="news-thumbnail">
                                ${thumbnail ? 
                                    `<img src="${thumbnail}" alt="${title}" loading="lazy" onerror="this.parentElement.innerHTML='<div class=\\'news-thumbnail-placeholder\\'>📄</div>'">` :
                                    `<div class="news-thumbnail-placeholder">📄</div>`
                                }
                            </div>
                            <h3 class="news-title">${title}</h3>
                            <p class="news-date">${date}</p>
                        </a>
                    `;
                }).join('');'''

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
        
        # loadPosts 함수가 categorySlug를 받는 경우 (간단한 버전)
        if 'async function loadPosts(categorySlug)' in content:
            # categorySlug를 categorySlugs 배열로 변경하고, categoryIds를 사용하도록 수정
            # 먼저 loadPosts 함수 시그니처 변경
            content = content.replace(
                'async function loadPosts(categorySlug)',
                'async function loadPosts(categorySlugs, pageTitle = \'\')'
            )
            
            # categorySlug를 categorySlugs 배열로 변환
            old_category_logic = r"// 카테고리 ID 가져오기 \(슬러그로\)[\s\S]*?let apiUrl = 'https://health9988234\.mycafe24\.com/wp-json/wp/v2/posts\?per_page=20&_embed';[\s\S]*?if \(categorySlug\) \{[\s\S]*?const catResponse = await fetch\(`https://health9988234\.mycafe24\.com/wp-json/wp/v2/categories\?slug=\$\{encodeURIComponent\(categorySlug\)\}`\);[\s\S]*?const categories = await catResponse\.json\(\);[\s\S]*?if \(categories\.length > 0\) \{[\s\S]*?apiUrl \+= `&categories=\$\{categories\[0\]\.id\}`;[\s\S]*?\}[\s\S]*?\}"
            
            new_category_logic = '''// 카테고리 ID 가져오기 (여러 슬러그 지원)
                let apiUrl = 'https://health9988234.mycafe24.com/wp-json/wp/v2/posts?per_page=20&_embed';
                const categoryIds = [];
                
                if (typeof categorySlugs === 'string') {
                    categorySlugs = [categorySlugs];
                } else if (!categorySlugs || !Array.isArray(categorySlugs)) {
                    categorySlugs = [];
                }
                
                if (categorySlugs.length > 0) {
                    for (const slug of categorySlugs) {
                        try {
                            const catUrl = `https://health9988234.mycafe24.com/wp-json/wp/v2/categories?slug=${encodeURIComponent(slug)}`;
                            const catResponse = await fetch(catUrl);
                            const categories = await catResponse.json();
                            if (categories.length > 0) {
                                categoryIds.push(categories[0].id);
                            }
                        } catch (e) {
                            console.error(`Category fetch error for ${slug}:`, e);
                        }
                    }
                    
                    if (categoryIds.length > 0) {
                        apiUrl += `&categories=${categoryIds.join(',')}`;
                    }
                }'''
            
            if re.search(old_category_logic, content):
                content = re.sub(old_category_logic, new_category_logic, content)
                print(f"  ✅ 카테고리 로직 업데이트")
            
            # 포스트 목록 렌더링 부분 교체
            old_rendering = r"// 포스트 목록 렌더링[\s\S]*?newsGrid\.innerHTML = posts\.map\(post => \{[\s\S]*?const thumbnail = getThumbnailUrl\(post\);[\s\S]*?const title = post\.title\.rendered;[\s\S]*?const date = new Date\(post\.date\)\.toLocaleDateString\('ko-KR'\);[\s\S]*?const backUrl = encodeURIComponent\(window\.location\.pathname\.split\('/'\)\.pop\(\)\);[\s\S]*?return `[\s\S]*?<a href=\"post-detail\.html\?id=\$\{post\.id\}&back=\$\{backUrl\}\" class=\"news-item\">[\s\S]*?<div class=\"news-thumbnail\">[\s\S]*?\$\{thumbnail \?[\s\S]*?`<img src=\"\$\{thumbnail\}\" alt=\"\$\{title\}\" loading=\"lazy\" onerror=\"this\.parentElement\.innerHTML='<div class=\\\\'news-thumbnail-placeholder\\\\'>📄</div>'\">` :[\s\S]*?`<div class=\"news-thumbnail-placeholder\">📄</div>`[\s\S]*?\}[\s\S]*?</div>[\s\S]*?<h3 class=\"news-title\">\$\{title\}</h3>[\s\S]*?<p class=\"news-date\">\$\{date\}</p>[\s\S]*?</a>[\s\S]*?`;[\s\S]*?\}\)\.join\(''\);"
            
            improved_code = get_improved_code()
            
            if re.search(old_rendering, content):
                content = re.sub(old_rendering, improved_code, content, flags=re.DOTALL)
                print(f"  ✅ 포스트 렌더링 로직 개선")
            else:
                # 다른 형식일 수 있음
                print(f"  ⚠️  포스트 렌더링 부분을 찾을 수 없음")
                return False
            
            # DOMContentLoaded에서 loadPosts 호출 부분 수정
            old_call = r"loadPosts\(categorySlug\);"
            new_call = "loadPosts([categorySlug], pageTitle);"
            if re.search(old_call, content):
                content = re.sub(old_call, new_call, content)
                print(f"  ✅ loadPosts 호출 업데이트")
        
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
    print("🚀 자동 매핑 및 정렬 개선 - 모든 파일 적용")
    print("=" * 60)
    
    # news-main.html과 모든 sub-*.html 파일 처리 (sub-역류성식도염.html 제외)
    target_files = ['news-main.html'] + [f for f in glob.glob("sub-*.html") if f != 'sub-역류성식도염.html']
    
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

