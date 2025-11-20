import re
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

print("=" * 70)
print("🔧 news-main.html 카테고리 로직 수정")
print("=" * 70)

with open('news-main.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 새로운 loadPosts 함수 (건강news 카테고리 자동 찾기)
new_load_posts = """
        let currentPage = 1;
        const postsPerPage = 12;
        let totalPosts = [];
        
        async function loadPosts() {
            try {
                console.log('건강news 카테고리 검색 중...');
                
                // 모든 카테고리 가져오기
                const categoriesResponse = await fetch('https://health9988234.mycafe24.com/wp-json/wp/v2/categories?per_page=100');
                
                if (!categoriesResponse.ok) {
                    throw new Error('카테고리를 불러올 수 없습니다');
                }
                
                const allCategories = await categoriesResponse.json();
                console.log('전체 카테고리:', allCategories.map(cat => cat.name));
                
                // '건강news', 'news', '건강News' 등의 이름을 가진 카테고리 찾기
                const newsCategory = allCategories.find(cat => 
                    cat.name.toLowerCase().includes('news') || 
                    cat.name.includes('뉴스') ||
                    cat.name.includes('건강news') ||
                    cat.slug.includes('news')
                );
                
                if (!newsCategory) {
                    console.log('건강news 카테고리를 찾지 못했습니다. 모든 글을 표시합니다.');
                    // 카테고리 없으면 모든 글 표시
                    const postsResponse = await fetch('https://health9988234.mycafe24.com/wp-json/wp/v2/posts?per_page=100&orderby=date&order=desc&_embed');
                    if (postsResponse.ok) {
                        totalPosts = await postsResponse.json();
                    }
                } else {
                    console.log('찾은 카테고리:', newsCategory.name, '(ID:', newsCategory.id, ')');
                    
                    // 해당 카테고리의 모든 글 가져오기
                    const postsResponse = await fetch(`https://health9988234.mycafe24.com/wp-json/wp/v2/posts?categories=${newsCategory.id}&per_page=100&orderby=date&order=desc&_embed`);
                    
                    if (!postsResponse.ok) {
                        throw new Error('글을 불러올 수 없습니다');
                    }
                    
                    totalPosts = await postsResponse.json();
                    console.log(`"${newsCategory.name}" 카테고리에서 ${totalPosts.length}개 글 로드`);
                }
                
                if (totalPosts.length === 0) {
                    document.getElementById('newsGrid').innerHTML = '<p style="text-align:center; padding:60px 20px; color:#999; grid-column: 1/-1;">등록된 글이 없습니다.</p>';
                    document.getElementById('pagination').innerHTML = '';
                    return;
                }
                
                displayPage(1);
                
            } catch (error) {
                console.error('글 로드 오류:', error);
                document.getElementById('newsGrid').innerHTML = '<p style="text-align:center; padding:60px 20px; color:#e53e3e; grid-column: 1/-1;">❌ 글을 불러오는 중 오류가 발생했습니다.</p>';
            }
        }
        
        function displayPage(page) {
            currentPage = page;
            const start = (page - 1) * postsPerPage;
            const end = start + postsPerPage;
            const postsToShow = totalPosts.slice(start, end);
            
            const newsGrid = document.getElementById('newsGrid');
            
            if (postsToShow.length === 0) {
                newsGrid.innerHTML = '<p style="text-align:center; padding:60px 20px; color:#999; grid-column: 1/-1;">등록된 글이 없습니다.</p>';
                document.getElementById('pagination').innerHTML = '';
                return;
            }
            
            newsGrid.innerHTML = postsToShow.map(post => {
                const title = post.title.rendered;
                const link = post.link;
                const thumbnail = post._embedded?.['wp:featuredmedia']?.[0]?.source_url || 
                                post.featured_media_url || 
                                'https://health9988234.mycafe24.com/wp-content/uploads/2025/11/cropped-1-1.png';
                
                return `
                    <a href="${link}" class="news-item" target="_blank">
                        <div class="news-thumbnail">
                            <img src="${thumbnail}" alt="${title}" style="width:100%; height:100%; object-fit:cover;" onerror="this.src='https://health9988234.mycafe24.com/wp-content/uploads/2025/11/cropped-1-1.png'">
                        </div>
                        <h3 class="news-title">${title}</h3>
                    </a>
                `;
            }).join('');
            
            // 페이징 버튼 생성
            const totalPages = Math.ceil(totalPosts.length / postsPerPage);
            
            if (totalPages > 1) {
                const paginationHtml = `
                    <button class="pagination-btn" onclick="displayPage(${page - 1})" ${page === 1 ? 'disabled' : ''}>
                        ← 이전
                    </button>
                    <span class="pagination-info">${page} / ${totalPages}</span>
                    <button class="pagination-btn" onclick="displayPage(${page + 1})" ${page === totalPages ? 'disabled' : ''}>
                        다음 →
                    </button>
                `;
                document.getElementById('pagination').innerHTML = paginationHtml;
            } else {
                document.getElementById('pagination').innerHTML = '';
            }
            
            // 페이지 상단으로 스크롤
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }
"""

# 기존 loadPosts 함수를 새로운 것으로 교체
content = re.sub(
    r"let currentPage = 1;[\s\S]*?function displayPage\(page\) \{[\s\S]*?\n        \}",
    new_load_posts.strip(),
    content
)

# DOMContentLoaded 이벤트에서 loadPosts 호출 (매개변수 없이)
content = re.sub(
    r"document\.addEventListener\('DOMContentLoaded',.*?loadPosts\(.*?\).*?\);",
    "document.addEventListener('DOMContentLoaded', () => {\n            loadPosts();\n        });",
    content
)

# 파일 저장
with open('news-main.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("\n✅ news-main.html 수정 완료!")
print("\n특징:")
print("  ✅ WordPress 카테고리 자동 검색")
print("  ✅ '건강news', 'news', '뉴스' 등의 이름 자동 감지")
print("  ✅ 카테고리 ID 자동 매칭")
print("  ✅ 해당 카테고리의 모든 글 표시")
print("  ✅ 최신순 정렬")
print("  ✅ 12개씩 페이징")
print("  ✅ 콘솔에 디버그 정보 출력")

import os
size = os.path.getsize('news-main.html') / 1024
print(f"\n파일 크기: {size:.1f} KB")

print("\n" + "=" * 70)
print("🎉 완료!")
print("=" * 70)

