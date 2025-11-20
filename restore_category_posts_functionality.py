import os
import re
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 카테고리 파일 목록
CATEGORY_FILES = [
    "category-심혈관질환.html",
    "category-당뇨병.html",
    "category-관절근골격계.html",
    "category-호르몬내분비.html",
    "category-정신건강신경계.html",
    "category-소화기질환.html",
    "category-안과치과기타.html",
]

# 카테고리별 매핑
CATEGORY_MAPPING = {
    "category-심혈관질환.html": {
        "category_slugs": ["심혈관-질환", "cardiovascular"],
        "page_title": "심혈관 질환"
    },
    "category-당뇨병.html": {
        "category_slugs": ["당뇨병", "diabetes"],
        "page_title": "당뇨병"
    },
    "category-관절근골격계.html": {
        "category_slugs": ["관절-근골격계-질환", "musculoskeletal"],
        "page_title": "관절/근골격계 질환"
    },
    "category-호르몬내분비.html": {
        "category_slugs": ["호르몬-내분비-질환", "endocrine"],
        "page_title": "호르몬/내분비 질환"
    },
    "category-정신건강신경계.html": {
        "category_slugs": ["정신-건강-신경계", "neuroscience"],
        "page_title": "정신 건강/신경계"
    },
    "category-소화기질환.html": {
        "category_slugs": ["소화기-질환", "digestive"],
        "page_title": "소화기 질환"
    },
    "category-안과치과기타.html": {
        "category_slugs": ["안과-치과-기타", "eyes-dental"],
        "page_title": "안과/치과/기타"
    },
}


def add_wordpress_posts_section(filepath):
    """카테고리 파일에 WordPress 글 목록 기능 추가"""
    if not os.path.exists(filepath):
        print(f"  ⚠️ 파일 없음: {filepath}")
        return False
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 이미 추가되어 있는지 확인
        if 'news-grid' in content and 'loadPosts' in content:
            print(f"  ℹ️ {filepath} - 이미 WordPress 글 기능이 있습니다")
            return False
        
        # 카테고리 매핑 가져오기
        filename = os.path.basename(filepath)
        mapping = CATEGORY_MAPPING.get(filename, {})
        category_slugs = mapping.get("category_slugs", [])
        page_title = mapping.get("page_title", "")
        
        # 서브카테고리 그리드 닫는 태그 뒤에 글 목록 섹션 추가
        posts_section = f"""
    <style>
        /* 글 목록 스타일 */
        .posts-section {{
            margin-top: 60px;
            padding: 40px 20px;
        }}
        
        .posts-section h3 {{
            font-size: 32px;
            font-weight: 800;
            text-align: center;
            margin-bottom: 40px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}
        
        .news-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 25px;
            max-width: 1200px;
            margin: 0 auto;
        }}
        
        .news-item {{
            background: white;
            border-radius: 16px;
            overflow: hidden;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            transition: all 0.3s;
            text-decoration: none;
            display: block;
        }}
        
        .news-item:hover {{
            transform: translateY(-5px);
            box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        }}
        
        .news-thumbnail {{
            width: 100%;
            height: 180px;
            overflow: hidden;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        
        .news-thumbnail img {{
            width: 100%;
            height: 100%;
            object-fit: cover;
        }}
        
        .news-thumbnail-placeholder {{
            font-size: 48px;
            color: #ccc;
        }}
        
        .news-title {{
            padding: 20px;
            font-size: 18px;
            font-weight: 700;
            color: #333;
            line-height: 1.5;
            margin: 0;
            display: -webkit-box;
            -webkit-line-clamp: 2;
            -webkit-box-orient: vertical;
            overflow: hidden;
        }}
        
        .news-date {{
            padding: 0 20px 20px;
            font-size: 14px;
            color: #999;
            margin: 0;
        }}
        
        .no-posts-message {{
            text-align: center;
            padding: 60px 20px;
            color: #999;
        }}
        
        .spinner {{
            border: 4px solid #f3f3f3;
            border-top: 4px solid #667eea;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 0 auto 20px;
        }}
        
        @keyframes spin {{
            0% {{ transform: rotate(0deg); }}
            100% {{ transform: rotate(360deg); }}
        }}
        
        @media (max-width: 768px) {{
            .news-grid {{
                grid-template-columns: 1fr;
            }}
            
            .posts-section h3 {{
                font-size: 24px;
            }}
        }}
    </style>
    
    <div class="posts-section">
        <h3>📝 관련 글</h3>
        <div class="news-grid" id="postsGrid">
            <div class="no-posts-message">
                <div class="spinner"></div>
                <p>글을 불러오는 중...</p>
            </div>
        </div>
    </div>
    
    <script>
        // 썸네일 URL 가져오기
        function getThumbnailUrl(post) {{
            if (post._embedded && post._embedded['wp:featuredmedia'] && post._embedded['wp:featuredmedia'][0]) {{
                const media = post._embedded['wp:featuredmedia'][0];
                if (media.media_details && media.media_details.sizes) {{
                    const sizes = media.media_details.sizes;
                    if (sizes.medium_large) return sizes.medium_large.source_url;
                    if (sizes.medium) return sizes.medium.source_url;
                    if (sizes.large) return sizes.large.source_url;
                    if (sizes.full) return sizes.full.source_url;
                }}
                if (media.source_url) return media.source_url;
            }}
            return null;
        }}
        
        // WordPress API로 글 불러오기
        async function loadCategoryPosts(categorySlugs, pageTitle = '') {{
            const postsGrid = document.getElementById('postsGrid');
            
            // 로딩 메시지
            postsGrid.innerHTML = `
                <div class="no-posts-message" style="grid-column: 1 / -1;">
                    <div class="spinner"></div>
                    <p>글을 불러오는 중...</p>
                </div>
            `;
            
            try {{
                // categorySlugs는 배열 또는 문자열 가능
                if (typeof categorySlugs === 'string') {{
                    categorySlugs = [categorySlugs];
                }} else if (!categorySlugs || !Array.isArray(categorySlugs)) {{
                    categorySlugs = [];
                }}
                
                // 카테고리 ID 가져오기
                let apiUrl = 'https://health9988234.mycafe24.com/wp-json/wp/v2/posts?per_page=20&_embed';
                const categoryIds = [];
                
                if (categorySlugs.length > 0) {{
                    console.log('Looking up categories for slugs:', categorySlugs);
                    for (const slug of categorySlugs) {{
                        try {{
                            const catUrl = `https://health9988234.mycafe24.com/wp-json/wp/v2/categories?slug=${{encodeURIComponent(slug)}}`;
                            const catResponse = await fetch(catUrl);
                            const categories = await catResponse.json();
                            if (categories.length > 0) {{
                                categoryIds.push(categories[0].id);
                                console.log(`Added category ID ${{categories[0].id}} for slug ${{slug}}`);
                            }}
                        }} catch (e) {{
                            console.error(`Category fetch error for ${{slug}}:`, e);
                        }}
                    }}
                    
                    if (categoryIds.length > 0) {{
                        apiUrl += `&categories=${{categoryIds.join(',')}}`;
                    }}
                }}
                
                console.log('Final API URL:', apiUrl);
                
                const response = await fetch(apiUrl);
                if (!response.ok) {{
                    throw new Error(`HTTP error! status: ${{response.status}}`);
                }}
                const posts = await response.json();
                
                console.log('Fetched posts:', posts.length);
                
                if (posts.length === 0) {{
                    postsGrid.innerHTML = `
                        <div class="no-posts-message" style="grid-column: 1 / -1;">
                            <p>📝 아직 작성된 글이 없습니다</p>
                            <p style="font-size: 14px; margin-top: 10px; color: #ccc;">곧 업데이트될 예정입니다</p>
                        </div>
                    `;
                    return;
                }}
                
                // 최대 12개만 표시
                const displayPosts = posts.slice(0, 12);
                
                postsGrid.innerHTML = displayPosts.map(post => {{
                    const thumbnail = getThumbnailUrl(post);
                    const title = post.title.rendered;
                    const date = new Date(post.date).toLocaleDateString('ko-KR');
                    const backUrl = encodeURIComponent(window.location.pathname.split('/').pop());
                    
                    return `
                        <a href="post-detail.html?id=${{post.id}}&back=${{backUrl}}" class="news-item">
                            <div class="news-thumbnail">
                                ${{thumbnail ? 
                                    `<img src="${{thumbnail}}" alt="${{title}}" loading="lazy" onerror="this.parentElement.innerHTML='<div class='news-thumbnail-placeholder'>📄</div>'">` :
                                    `<div class="news-thumbnail-placeholder">📄</div>`
                                }}
                            </div>
                            <h3 class="news-title">${{title}}</h3>
                            <p class="news-date">${{date}}</p>
                        </a>
                    `;
                }}).join('');
                
            }} catch (error) {{
                console.error('Error loading posts:', error);
                postsGrid.innerHTML = `
                    <div class="no-posts-message" style="grid-column: 1 / -1;">
                        <p>❌ 글을 불러오는데 실패했습니다</p>
                        <p style="font-size: 14px; margin-top: 10px; color: #ccc;">잠시 후 다시 시도해주세요</p>
                    </div>
                `;
            }}
        }}
        
        // 페이지 로드 시 실행
        document.addEventListener('DOMContentLoaded', function() {{
            const currentPage = window.location.pathname.split('/').pop();
            const categorySlugs = {category_slugs};
            const pageTitle = "{page_title}";
            
            loadCategoryPosts(categorySlugs, pageTitle);
        }});
    </script>
"""
        
        # 서브카테고리 그리드 닫는 태그 뒤에 추가
        # 패턴: </div> (health-cards-grid 닫는 태그) 뒤에 추가
        pattern = r'(</div>\s*</div>\s*</div>\s*<script>)'
        
        replacement = posts_section + r'\1'
        
        new_content = re.sub(pattern, replacement, content)
        
        if new_content != content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"  ✅ {filepath} - WordPress 글 기능 추가 완료")
            return True
        else:
            print(f"  ⚠️ {filepath} - 패턴을 찾을 수 없습니다")
            return False
            
    except Exception as e:
        print(f"  ❌ {filepath} - 오류: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """메인 실행"""
    print("=" * 60)
    print("🔄 카테고리 페이지에 WordPress 글 기능 복구")
    print("=" * 60)
    print("\n💡 sub-*.html 파일과 동일한 방식으로")
    print("   WordPress API로 글을 불러오는 기능을 추가합니다.\n")
    
    print("📝 파일 수정 중...\n")
    fixed_files = []
    
    for file in CATEGORY_FILES:
        if add_wordpress_posts_section(file):
            fixed_files.append(file)
    
    print(f"\n✅ 총 {len(fixed_files)}개 파일 수정 완료!")
    
    print("\n" + "=" * 60)
    print("✅ 복구 완료!")
    print("=" * 60)
    print("\n💡 이제 로컬에서 index-v2.html을 열면")
    print("   카테고리 페이지에서 WordPress 글 목록이 표시됩니다.")
    print("=" * 60)


if __name__ == "__main__":
    main()

