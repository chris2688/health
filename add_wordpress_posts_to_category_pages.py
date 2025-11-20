import os
import re
import sys
import io
from ftplib import FTP

# UTF-8 인코딩 설정
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

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

# WordPress API로 글을 불러오는 JavaScript 코드
WORDPRESS_POSTS_SCRIPT = """
    <style>
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
        function getThumbnailUrl(post) {
            if (post._embedded && post._embedded['wp:featuredmedia'] && post._embedded['wp:featuredmedia'][0]) {
                const media = post._embedded['wp:featuredmedia'][0];
                if (media.media_details && media.media_details.sizes) {
                    const sizes = media.media_details.sizes;
                    if (sizes.medium_large) return sizes.medium_large.source_url;
                    if (sizes.medium) return sizes.medium.source_url;
                    if (sizes.large) return sizes.large.source_url;
                    if (sizes.full) return sizes.full.source_url;
                }
                if (media.source_url) return media.source_url;
            }
            return null;
        }
        
        // WordPress API로 글 불러오기
        async function loadCategoryPosts(categorySlugs) {
            const postsGrid = document.getElementById('postsGrid');
            
            try {
                let apiUrl = 'https://health9988234.mycafe24.com/wp-json/wp/v2/posts?per_page=12&_embed';
                const categoryIds = [];
                
                if (categorySlugs && categorySlugs.length > 0) {
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
                }
                
                const response = await fetch(apiUrl);
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                const posts = await response.json();
                
                if (posts.length === 0) {
                    postsGrid.innerHTML = `
                        <div class="no-posts-message" style="grid-column: 1 / -1;">
                            <p>📝 아직 작성된 글이 없습니다</p>
                            <p style="font-size: 14px; margin-top: 10px; color: #ccc;">곧 업데이트될 예정입니다</p>
                        </div>
                    `;
                    return;
                }
                
                postsGrid.innerHTML = posts.map(post => {
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
                }).join('');
                
            } catch (error) {
                console.error('Error loading posts:', error);
                postsGrid.innerHTML = `
                    <div class="no-posts-message" style="grid-column: 1 / -1;">
                        <p>❌ 글을 불러오는데 실패했습니다</p>
                        <p style="font-size: 14px; margin-top: 10px; color: #ccc;">잠시 후 다시 시도해주세요</p>
                    </div>
                `;
            }
        }
        
        // 페이지 로드 시 실행
        document.addEventListener('DOMContentLoaded', function() {
            const currentPage = window.location.pathname.split('/').pop();
            const mapping = CATEGORY_MAPPING[currentPage];
            
            if (mapping) {
                loadCategoryPosts(mapping.category_slugs);
            } else {
                // 기본값: 페이지 제목으로 카테고리 찾기
                const pageTitle = document.querySelector('.section-title h2')?.textContent?.trim() || '';
                loadCategoryPosts([pageTitle]);
            }
        });
    </script>
"""

# 카테고리 매핑을 JavaScript에 주입
CATEGORY_MAPPING_JS = """
        const CATEGORY_MAPPING = {
            "category-심혈관질환.html": ["심혈관-질환", "cardiovascular"],
            "category-당뇨병.html": ["당뇨병", "diabetes"],
            "category-관절근골격계.html": ["관절-근골격계-질환", "musculoskeletal"],
            "category-호르몬내분비.html": ["호르몬-내분비-질환", "endocrine"],
            "category-정신건강신경계.html": ["정신-건강-신경계", "neuroscience"],
            "category-소화기질환.html": ["소화기-질환", "digestive"],
            "category-안과치과기타.html": ["안과-치과-기타", "eyes-dental"],
        };
"""


def add_wordpress_posts_to_category_file(filepath):
    """카테고리 파일에 WordPress 글 목록 기능 추가"""
    if not os.path.exists(filepath):
        print(f"  ⚠️ 파일 없음: {filepath}")
        return False
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 이미 추가되어 있는지 확인
        if 'posts-section' in content or 'loadCategoryPosts' in content:
            print(f"  ℹ️ {filepath} - 이미 WordPress 글 기능이 추가되어 있습니다")
            return False
        
        # </div> 태그 (health-cards-grid 닫는 태그) 뒤에 글 목록 섹션 추가
        # 여러 패턴 시도
        patterns = [
            r'(</div>\s*</div>\s*</div>\s*<script>)',  # 기본 패턴
            r'(</div>\s*</div>\s*<script>)',  # 간단한 패턴
            r'(</div>\s*<script>)',  # 더 간단한 패턴
        ]
        
        # 카테고리 매핑 가져오기
        filename = os.path.basename(filepath)
        mapping = CATEGORY_MAPPING.get(filename, {})
        
        # JavaScript에 카테고리 매핑 추가
        script_with_mapping = WORDPRESS_POSTS_SCRIPT.replace(
            'const mapping = CATEGORY_MAPPING[currentPage];',
            CATEGORY_MAPPING_JS + '\n        const mapping = CATEGORY_MAPPING[currentPage];'
        )
        
        new_content = content
        for pattern in patterns:
            replacement = script_with_mapping + r'\1'
            new_content = re.sub(pattern, replacement, new_content)
            if new_content != content:
                break
        
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
        return False


def upload_files_via_ftp(files):
    """FTP를 통해 수정된 파일들 업로드"""
    print("\n" + "=" * 60)
    print("📤 FTP 파일 업로드")
    print("=" * 60)
    
    FTP_HOST = "health9988234.mycafe24.com"
    FTP_USER = "health9988234"
    FTP_PASS = "ssurlf7904!"
    FTP_PORT = 21
    
    try:
        print(f"\n🔗 FTP 서버 연결 중...")
        ftp = FTP()
        ftp.encoding = 'utf-8'
        ftp.connect(FTP_HOST, FTP_PORT, timeout=10)
        print("✅ 연결 성공!")
        
        print(f"🔐 로그인 중...")
        ftp.login(FTP_USER, FTP_PASS)
        print("✅ 로그인 성공!")
        
        uploaded_count = 0
        print(f"\n📤 파일 업로드 시작...\n")
        
        for file in files:
            if os.path.exists(file):
                try:
                    print(f"  업로드 중: {file}...", end=" ")
                    with open(file, "rb") as f:
                        ftp.storbinary(f"STOR {file}", f)
                    print("✅ 완료")
                    uploaded_count += 1
                except Exception as e:
                    print(f"❌ 실패: {str(e)[:50]}")
        
        ftp.quit()
        print(f"\n✅ 총 {uploaded_count}개 파일 업로드 완료!")
        return True
            
    except Exception as e:
        print(f"\n❌ FTP 업로드 오류: {e}")
        return False


def main():
    """메인 실행"""
    print("=" * 60)
    print("📝 카테고리 페이지에 WordPress 글 목록 추가")
    print("=" * 60)
    
    category_files = list(CATEGORY_MAPPING.keys())
    
    print("\n📝 파일 수정 중...\n")
    fixed_files = []
    
    for file in category_files:
        if add_wordpress_posts_to_category_file(file):
            fixed_files.append(file)
    
    print(f"\n✅ 총 {len(fixed_files)}개 파일 수정 완료!")
    
    if fixed_files:
        print("\n📤 수정된 파일을 FTP로 업로드합니다...")
        upload_files_via_ftp(fixed_files)
    
    print("\n" + "=" * 60)
    print("✅ 작업 완료!")
    print("=" * 60)


if __name__ == "__main__":
    main()

