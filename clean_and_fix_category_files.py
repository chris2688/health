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


def clean_and_fix_file(filepath):
    """파일을 깔끔하게 정리하고 올바른 구조로 수정"""
    if not os.path.exists(filepath):
        print(f"  ⚠️ 파일 없음: {filepath}")
        return False
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        filename = os.path.basename(filepath)
        mapping = CATEGORY_MAPPING.get(filename, {})
        category_slugs = mapping.get("category_slugs", [])
        page_title = mapping.get("page_title", "")
        
        # 1. </head> 태그 앞의 중복된 스타일 제거 (posts-section 스타일만 남기고 나머지 제거)
        # </head> 태그를 찾아서 그 앞의 중복된 스타일 제거
        head_end_pos = content.find('</head>')
        if head_end_pos > 0:
            head_section = content[:head_end_pos]
            body_section = content[head_end_pos:]
            
            # head 섹션에서 중복된 posts-section 스타일 제거 (첫 번째 것만 남김)
            # 첫 번째 posts-section 스타일 찾기
            first_style_match = re.search(r'(/\* 글 목록 스타일 \*/.*?@media.*?})', head_section, re.DOTALL)
            if first_style_match:
                # 첫 번째 스타일 이후의 중복 제거
                head_section = head_section[:first_style_match.end()] + '\n    </head>'
                content = head_section + body_section
        
        # 2. body 섹션에서 중복된 posts-section HTML 제거
        # health-cards-grid 닫는 태그 뒤에 posts-section이 하나만 있도록
        pattern = r'(</div>\s*</div>\s*</div>)\s*(<style>.*?</style>)?\s*(<div class="posts-section">.*?</div>\s*</div>)\s*(<div class="posts-section">.*?</div>\s*</div>)?'
        content = re.sub(pattern, r'\1\n        </div>\n    </div>\n    \n    <div class="posts-section">\n        <h3>📝 관련 글</h3>\n        <div class="news-grid" id="postsGrid">\n            <div class="no-posts-message">\n                <div class="spinner"></div>\n                <p>글을 불러오는 중...</p>\n            </div>\n        </div>\n    </div>', content, flags=re.DOTALL)
        
        # 3. 중복된 스크립트 제거 (마지막 것만 남김)
        # getThumbnailUrl와 loadCategoryPosts 함수가 여러 번 정의되어 있으면 마지막 것만 남김
        scripts = re.findall(r'(<script>.*?</script>)', content, re.DOTALL)
        if len(scripts) > 2:  # 모바일 메뉴 스크립트 + 글 로딩 스크립트 = 2개
            # 마지막 2개만 남기고 나머지 제거
            mobile_script = None
            posts_script = None
            
            for script in scripts:
                if 'mobileMenuBtn' in script:
                    mobile_script = script
                elif 'loadCategoryPosts' in script:
                    posts_script = script
            
            # 모든 스크립트 제거
            content = re.sub(r'<script>.*?</script>', '', content, flags=re.DOTALL)
            
            # 올바른 스크립트 추가
            if mobile_script:
                content = content.replace('</body>', mobile_script + '\n\n    ' + (posts_script or '') + '\n</body>')
            elif posts_script:
                content = content.replace('</body>', posts_script + '\n</body>')
        
        # 4. 올바른 스크립트가 없으면 추가
        if 'loadCategoryPosts' not in content:
            posts_script = f"""
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
"""
            content = content.replace('</body>', posts_script + '\n</body>')
        
        # 5. 올바른 posts-section HTML이 없으면 추가
        if 'id="postsGrid"' not in content or content.count('id="postsGrid"') > 1:
            # health-cards-grid 닫는 태그 뒤에 posts-section 추가
            pattern = r'(</div>\s*</div>\s*</div>\s*)(<script>|</body>)'
            replacement = r'\1\n    <div class="posts-section">\n        <h3>📝 관련 글</h3>\n        <div class="news-grid" id="postsGrid">\n            <div class="no-posts-message">\n                <div class="spinner"></div>\n                <p>글을 불러오는 중...</p>\n            </div>\n        </div>\n    </div>\n    \n    \2'
            content = re.sub(pattern, replacement, content)
        
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  ✅ {filepath} - 파일 정리 완료")
            return True
        else:
            print(f"  ℹ️ {filepath} - 변경사항 없음")
            return False
            
    except Exception as e:
        print(f"  ❌ {filepath} - 오류: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """메인 실행"""
    print("=" * 60)
    print("🧹 카테고리 파일 정리 및 수정")
    print("=" * 60)
    print("\n💡 중복된 스타일, 스크립트, HTML 섹션을 제거하고")
    print("   올바른 구조로 정리합니다.\n")
    
    print("📝 파일 정리 중...\n")
    fixed_files = []
    
    for file in CATEGORY_FILES:
        if clean_and_fix_file(file):
            fixed_files.append(file)
    
    print(f"\n✅ 총 {len(fixed_files)}개 파일 정리 완료!")
    
    print("\n" + "=" * 60)
    print("✅ 정리 완료!")
    print("=" * 60)


if __name__ == "__main__":
    main()

