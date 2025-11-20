import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

print("=" * 70)
print("📰 news-main.html 재작성 (기존 스타일 적용)")
print("=" * 70)

# sub 페이지와 동일한 스타일로 news-main.html 생성
with open('sub-hypertension.html', 'r', encoding='utf-8') as f:
    template = f.read()

# 타이틀 변경
template = template.replace('<title>고혈압', '<title>건강News')
template = template.replace('고혈압', '건강News')
template = template.replace('sub-hypertension', 'news-main')

# 뒤로가기 링크 변경
template = template.replace('href="category-cardiovascular.html"', 'href="index-v3.html"')

# JavaScript 매핑 부분을 건강news 카테고리로 변경
import re

# loadPosts 함수 호출 부분을 찾아서 수정
template = re.sub(
    r"loadPosts\(\[?.*?\]?, '.*?'\);",
    "loadPosts(['news', '건강news', '건강-news', 'health-news'], '건강News');",
    template
)

# pageToCategory 매핑 제거 (필요없음)
template = re.sub(
    r"const pageToCategory = \{[\s\S]*?\};",
    "// news-main.html - 건강news 카테고리만 표시",
    template
)

# 페이지 타이틀 찾기 로직 제거
template = re.sub(
    r"const pageTitle = document\.querySelector.*?\n.*?\n.*?;",
    "const pageTitle = '건강News';",
    template
)

# 현재 페이지 로직 제거  
template = re.sub(
    r"let currentPage = window\.location\.pathname.*?\n.*?if \(!currentPage.*?[\s\S]*?\}",
    "// news-main.html에서는 건강news 카테고리만 표시",
    template
)

# categorySlug 직접 설정
template = re.sub(
    r"let categorySlug = pageToCategory\[currentPage\];",
    "let categorySlug = ['news', '건강news', '건강-news', 'health-news'];",
    template
)

# findCategoryByPageTitle 호출 제거
template = re.sub(
    r"if \(!categorySlug\) \{[\s\S]*?try \{[\s\S]*?findCategoryByPageTitle[\s\S]*?\} catch[\s\S]*?\}[\s\S]*?\}",
    "",
    template
)

# news-grid를 3열로 변경
template = re.sub(
    r"grid-template-columns: repeat\(2, 1fr\);",
    "grid-template-columns: repeat(3, 1fr);",
    template
)

# 페이징 CSS 추가
pagination_css = """
        
        /* 페이징 스타일 */
        .pagination {
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 10px;
            margin: 50px auto 30px;
            padding: 0 20px;
        }
        
        .pagination-btn {
            padding: 12px 20px;
            background: white;
            color: #667eea;
            border: 2px solid #667eea;
            border-radius: 12px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
            text-decoration: none;
            display: inline-block;
        }
        
        .pagination-btn:hover:not(:disabled) {
            background: #667eea;
            color: white;
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
        }
        
        .pagination-btn:disabled {
            opacity: 0.3;
            cursor: not-allowed;
        }
        
        .pagination-btn.active {
            background: #667eea;
            color: white;
        }
        
        .pagination-info {
            font-size: 16px;
            color: #718096;
            margin: 0 15px;
        }
"""

# CSS 마지막에 페이징 스타일 추가
template = template.replace('</style>', pagination_css + '\n    </style>', 1)

# JavaScript에 페이징 로직 추가
paging_js = """
        let currentPage = 1;
        const postsPerPage = 12;
        let totalPosts = [];
        
        async function loadPosts(categorySlug, pageTitle) {
            try {
                console.log('카테고리 슬러그:', categorySlug);
                
                // 여러 카테고리 슬러그 시도
                let allPosts = [];
                
                for (const slug of categorySlug) {
                    try {
                        // 카테고리 ID 가져오기
                        const catResponse = await fetch(`https://health9988234.mycafe24.com/wp-json/wp/v2/categories?slug=${slug}`);
                        if (catResponse.ok) {
                            const categories = await catResponse.json();
                            if (categories.length > 0) {
                                const categoryId = categories[0].id;
                                console.log(`카테고리 "${slug}" ID:`, categoryId);
                                
                                // 해당 카테고리의 모든 글 가져오기
                                const postsResponse = await fetch(`https://health9988234.mycafe24.com/wp-json/wp/v2/posts?categories=${categoryId}&per_page=100&orderby=date&order=desc&_embed`);
                                if (postsResponse.ok) {
                                    const posts = await postsResponse.json();
                                    allPosts = allPosts.concat(posts);
                                    console.log(`"${slug}" 카테고리에서 ${posts.length}개 글 로드`);
                                    break; // 성공하면 종료
                                }
                            }
                        }
                    } catch (err) {
                        console.log(`"${slug}" 카테고리 시도 실패:`, err);
                    }
                }
                
                if (allPosts.length === 0) {
                    console.log('카테고리에서 글을 찾지 못함, 모든 글 로드 시도');
                    // 카테고리 없으면 모든 글 가져오기
                    const response = await fetch('https://health9988234.mycafe24.com/wp-json/wp/v2/posts?per_page=100&orderby=date&order=desc&_embed');
                    if (response.ok) {
                        allPosts = await response.json();
                    }
                }
                
                totalPosts = allPosts;
                displayPage(1);
                
            } catch (error) {
                console.error('글 로드 오류:', error);
                document.getElementById('newsGrid').innerHTML = '<p style="text-align:center; padding:60px 20px; color:#999;">글을 불러오는 중 오류가 발생했습니다.</p>';
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
        }
"""

# 기존 loadPosts 함수를 새로운 것으로 교체
template = re.sub(
    r"async function loadPosts\(categorySlug, pageTitle\) \{[\s\S]*?\n        \}",
    paging_js.strip(),
    template
)

# newsGrid div 추가 (기존 news-grid를 id 추가)
template = template.replace('<div class="news-grid">', '<div class="news-grid" id="newsGrid">')

# 페이징 컨테이너 추가 (news-grid 다음에)
template = template.replace('</div>\n\n    <script>', '</div>\n        <div class="pagination" id="pagination"></div>\n\n    <script>')

# 파일 저장
with open('news-main.html', 'w', encoding='utf-8') as f:
    f.write(template)

print("\n✅ news-main.html 생성 완료!")
print("\n특징:")
print("  ✅ 기존 sub 페이지와 동일한 스타일")
print("  ✅ 1:1 썸네일 + 제목")
print("  ✅ 3열 그리드 레이아웃")
print("  ✅ 12개씩 페이징 (3열 × 4행)")
print("  ✅ '건강news' 카테고리만 표시")
print("  ✅ 최신순 정렬")
print("  ✅ 뒤로가기 버튼 스타일 통일")

import os
size = os.path.getsize('news-main.html') / 1024
print(f"\n파일 크기: {size:.1f} KB")

print("\n" + "=" * 70)
print("🎉 완료!")
print("=" * 70)

