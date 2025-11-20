import os
import re
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

CATEGORY_FILES = [
    "category-심혈관질환.html",
    "category-당뇨병.html",
    "category-관절근골격계.html",
    "category-호르몬내분비.html",
    "category-정신건강신경계.html",
    "category-소화기질환.html",
    "category-안과치과기타.html",
]

CATEGORY_MAPPING = {
    "category-심혈관질환.html": {
        "category_slugs": ["심혈관-질환", "cardiovascular"],
        "page_title": "심혈관 질환",
        "icon": "❤️"
    },
    "category-당뇨병.html": {
        "category_slugs": ["당뇨병", "diabetes"],
        "page_title": "당뇨병",
        "icon": "💉"
    },
    "category-관절근골격계.html": {
        "category_slugs": ["관절-근골격계-질환", "musculoskeletal"],
        "page_title": "관절/근골격계 질환",
        "icon": "🦴"
    },
    "category-호르몬내분비.html": {
        "category_slugs": ["호르몬-내분비-질환", "endocrine"],
        "page_title": "호르몬/내분비 질환",
        "icon": "⚖️"
    },
    "category-정신건강신경계.html": {
        "category_slugs": ["정신-건강-신경계", "neuroscience"],
        "page_title": "정신 건강/신경계",
        "icon": "🧠"
    },
    "category-소화기질환.html": {
        "category_slugs": ["소화기-질환", "digestive"],
        "page_title": "소화기 질환",
        "icon": "🫀"
    },
    "category-안과치과기타.html": {
        "category_slugs": ["안과-치과-기타", "eyes-dental"],
        "page_title": "안과/치과/기타",
        "icon": "👁️"
    },
}


def extract_health_cards(content):
    """health-cards-grid 내용 추출"""
    match = re.search(r'<div class="health-cards-grid">(.*?)</div>\s*</div>', content, re.DOTALL)
    if match:
        return match.group(1)
    return ""


def rebuild_file(filepath):
    """파일을 올바른 구조로 재작성"""
    if not os.path.exists(filepath):
        print(f"  ⚠️ 파일 없음: {filepath}")
        return False
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        filename = os.path.basename(filepath)
        mapping = CATEGORY_MAPPING.get(filename, {})
        category_slugs = mapping.get("category_slugs", [])
        page_title = mapping.get("page_title", "")
        icon = mapping.get("icon", "📋")
        
        # health-cards-grid 내용 추출
        health_cards = extract_health_cards(content)
        
        # 헤더 부분 추출
        header_match = re.search(r'(<header class="main-header">.*?</header>)', content, re.DOTALL)
        header = header_match.group(1) if header_match else ""
        
        # 스타일 부분 추출 (기본 스타일만)
        style_match = re.search(r'(<style>.*?</style>)', content, re.DOTALL)
        base_style = style_match.group(1) if style_match else ""
        
        # posts-section 스타일 추가
        posts_style = """
        /* 글 목록 스타일 */
        .posts-section {
            margin-top: 60px;
            padding: 40px 20px;
        }
        
        .posts-section h3 {
            font-size: 32px;
            font-weight: 800;
            text-align: center;
            margin-bottom: 40px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .news-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 25px;
            max-width: 1200px;
            margin: 0 auto;
        }
        
        .news-item {
            background: white;
            border-radius: 16px;
            overflow: hidden;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            transition: all 0.3s;
            text-decoration: none;
            display: block;
        }
        
        .news-item:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        }
        
        .news-thumbnail {
            width: 100%;
            height: 180px;
            overflow: hidden;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        .news-thumbnail img {
            width: 100%;
            height: 100%;
            object-fit: cover;
        }
        
        .news-thumbnail-placeholder {
            font-size: 48px;
            color: #ccc;
        }
        
        .news-title {
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
        }
        
        .news-date {
            padding: 0 20px 20px;
            font-size: 14px;
            color: #999;
            margin: 0;
        }
        
        .no-posts-message {
            text-align: center;
            padding: 60px 20px;
            color: #999;
        }
        
        .spinner {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #667eea;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 0 auto 20px;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        @media (max-width: 768px) {
            .news-grid {
                grid-template-columns: 1fr;
            }
            
            .posts-section h3 {
                font-size: 24px;
            }
        }
"""
        
        # 스타일 합치기
        if base_style:
            # </style> 태그 앞에 posts_style 추가
            full_style = base_style.replace('</style>', posts_style + '\n    </style>')
        else:
            full_style = f"<style>{posts_style}\n    </style>"
        
        # 새 파일 내용 생성
        new_content = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{page_title} - 9988 건강정보</title>
    {full_style}
</head>
<body>
    {header}

    <div class="health-card-container">
        <div class="container-content">
            <a href="index-v2.html" class="back-button">뒤로가기</a>

            <div class="section-title">
                <div class="main-icon">{icon}</div>
                <h2>{page_title}</h2>
                <p class="subtitle">관심있는 주제를 선택하세요</p>
            </div>
            
            <div class="health-cards-grid">
{health_cards}
            </div>
        </div>
    </div>
    
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
        document.getElementById('mobileMenuBtn').addEventListener('click', function() {{
            document.getElementById('mainNav').classList.toggle('active');
        }});
    </script>

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
            
            if (!postsGrid) {{
                console.error('postsGrid element not found');
                return;
            }}
            
            postsGrid.innerHTML = `
                <div class="no-posts-message" style="grid-column: 1 / -1;">
                    <div class="spinner"></div>
                    <p>글을 불러오는 중...</p>
                </div>
            `;
            
            try {{
                if (typeof categorySlugs === 'string') {{
                    categorySlugs = [categorySlugs];
                }} else if (!categorySlugs || !Array.isArray(categorySlugs)) {{
                    categorySlugs = [];
                }}
                
                let apiUrl = 'https://health9988234.mycafe24.com/wp-json/wp/v2/posts?per_page=20&_embed';
                const categoryIds = [];
                
                if (categorySlugs.length > 0) {{
                    for (const slug of categorySlugs) {{
                        try {{
                            const catUrl = `https://health9988234.mycafe24.com/wp-json/wp/v2/categories?slug=${{encodeURIComponent(slug)}}`;
                            const catResponse = await fetch(catUrl);
                            const categories = await catResponse.json();
                            if (categories.length > 0) {{
                                categoryIds.push(categories[0].id);
                            }}
                        }} catch (e) {{
                            console.error(`Category fetch error for ${{slug}}:`, e);
                        }}
                    }}
                    
                    if (categoryIds.length > 0) {{
                        apiUrl += `&categories=${{categoryIds.join(',')}}`;
                    }}
                }}
                
                const response = await fetch(apiUrl);
                if (!response.ok) {{
                    throw new Error(`HTTP error! status: ${{response.status}}`);
                }}
                const posts = await response.json();
                
                if (posts.length === 0) {{
                    postsGrid.innerHTML = `
                        <div class="no-posts-message" style="grid-column: 1 / -1;">
                            <p>📝 아직 작성된 글이 없습니다</p>
                            <p style="font-size: 14px; margin-top: 10px; color: #ccc;">곧 업데이트될 예정입니다</p>
                        </div>
                    `;
                    return;
                }}
                
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
        
        document.addEventListener('DOMContentLoaded', function() {{
            const categorySlugs = {category_slugs};
            const pageTitle = "{page_title}";
            loadCategoryPosts(categorySlugs, pageTitle);
        }});
    </script>
</body>
</html>
"""
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"  ✅ {filepath} - 파일 재작성 완료")
        return True
            
    except Exception as e:
        print(f"  ❌ {filepath} - 오류: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """메인 실행"""
    print("=" * 60)
    print("🔨 카테고리 파일 재작성")
    print("=" * 60)
    print("\n💡 올바른 구조로 파일을 완전히 재작성합니다.\n")
    
    print("📝 파일 재작성 중...\n")
    fixed_files = []
    
    for file in CATEGORY_FILES:
        if rebuild_file(file):
            fixed_files.append(file)
    
    print(f"\n✅ 총 {len(fixed_files)}개 파일 재작성 완료!")
    
    print("\n" + "=" * 60)
    print("✅ 재작성 완료!")
    print("=" * 60)
    print("\n💡 이제 로컬에서 index-v2.html을 열면")
    print("   카테고리 페이지에서 WordPress 글 목록이 표시됩니다.")
    print("=" * 60)


if __name__ == "__main__":
    main()

