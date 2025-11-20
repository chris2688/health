import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

print("=" * 70)
print("📰 news-main.html 완전 재작성")
print("=" * 70)

news_html = '''<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>건강News - 9988 건강정보</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, "Noto Sans KR", sans-serif;
            background: #f5f7fa;
            min-height: 100vh;
        }
        
        /* ========== 헤더 스타일 ========== */
        .main-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            box-shadow: 0 4px 20px rgba(102, 126, 234, 0.3);
            position: sticky;
            top: 0;
            z-index: 1000;
        }
        
        .header-content {
            max-width: 1400px;
            margin: 0 auto;
            padding: 0 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            min-height: 80px;
        }
        
        .logo-container {
            display: flex;
            align-items: center;
            gap: 15px;
            text-decoration: none;
            transition: transform 0.3s;
        }
        
        .logo-container:hover {
            transform: scale(1.05);
        }
        
        .logo-image {
            height: 50px;
            width: auto;
            border-radius: 8px;
            background: white;
            padding: 5px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        
        .main-nav {
            display: flex;
            gap: 0;
        }
        
        .nav-item {
            padding: 10px 24px;
            color: white;
            text-decoration: none;
            font-weight: 600;
            font-size: 16px;
            transition: all 0.3s;
            position: relative;
            border-radius: 8px;
        }
        
        .nav-item:hover {
            background: rgba(255,255,255,0.15);
        }
        
        .mobile-menu-btn {
            display: none;
            background: none;
            border: none;
            color: white;
            font-size: 28px;
            cursor: pointer;
            padding: 10px;
        }
        
        .mobile-close-btn {
            display: none;
        }
        
        /* ========== 콘텐츠 영역 ========== */
        .site-main {
            max-width: 1400px;
            margin: 0 auto;
            padding: 40px 20px;
        }
        
        .back-button {
            display: inline-block;
            padding: 12px 24px;
            background: white;
            color: #667eea;
            text-decoration: none;
            border-radius: 25px;
            font-weight: 600;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            transition: all 0.3s;
            margin: 0 0 30px 0;
        }
        
        .back-button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
            background: #667eea;
            color: white;
        }
        
        .page-title {
            font-size: 42px;
            color: #2d3748;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            gap: 15px;
        }
        
        .page-subtitle {
            font-size: 18px;
            color: #718096;
            margin-bottom: 50px;
        }
        
        /* ========== 뉴스 그리드 ========== */
        .posts-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 30px;
            margin-top: 30px;
        }
        
        .post-card {
            background: white;
            border-radius: 16px;
            overflow: hidden;
            box-shadow: 0 4px 15px rgba(0,0,0,0.08);
            transition: all 0.3s;
            cursor: pointer;
            text-decoration: none;
            color: inherit;
            display: block;
        }
        
        .post-card:hover {
            transform: translateY(-8px);
            box-shadow: 0 12px 30px rgba(102, 126, 234, 0.2);
        }
        
        .post-thumbnail {
            width: 100%;
            height: 220px;
            object-fit: cover;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }
        
        .post-content {
            padding: 25px;
        }
        
        .post-category {
            display: inline-block;
            padding: 6px 14px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 20px;
            font-size: 13px;
            font-weight: 600;
            margin-bottom: 12px;
        }
        
        .post-title {
            font-size: 22px;
            font-weight: 700;
            color: #2d3748;
            margin-bottom: 12px;
            line-height: 1.4;
        }
        
        .post-excerpt {
            font-size: 15px;
            color: #718096;
            line-height: 1.6;
            margin-bottom: 15px;
        }
        
        .post-meta {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding-top: 15px;
            border-top: 1px solid #e2e8f0;
            font-size: 14px;
            color: #a0aec0;
        }
        
        .loading-message {
            text-align: center;
            padding: 80px 20px;
            font-size: 18px;
            color: #718096;
        }
        
        .error-message {
            text-align: center;
            padding: 80px 20px;
            font-size: 18px;
            color: #e53e3e;
        }
        
        /* ========== 모바일 반응형 ========== */
        @media (max-width: 768px) {
            .main-nav {
                display: none;
            }
            
            .main-nav.active {
                display: flex;
                flex-direction: column;
                position: absolute;
                top: 80px;
                left: 0;
                right: 0;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                padding: 20px;
                box-shadow: 0 4px 20px rgba(0,0,0,0.2);
            }
            
            .mobile-menu-btn {
                display: block;
            }
            
            .mobile-close-btn {
                display: block;
                position: absolute;
                top: 15px;
                right: 15px;
                background: none;
                border: none;
                color: white;
                font-size: 24px;
                cursor: pointer;
            }
            
            .posts-grid {
                grid-template-columns: 1fr;
                gap: 20px;
            }
            
            .page-title {
                font-size: 32px;
            }
        }
    </style>
</head>
<body>
    <!-- 헤더 -->
    <header class="main-header">
        <div class="header-content">
            <a href="index-v3.html" class="logo-container">
                <img src="https://health9988234.mycafe24.com/wp-content/uploads/2025/11/cropped-1-1.png" 
                     alt="9988 건강 연구소" 
                     class="logo-image">
            </a>
            
            <nav class="main-nav" id="mainNav">
                <button class="mobile-close-btn" id="mobileCloseBtn">✕</button>
                <a href="index-v3.html" class="nav-item">질환별 정보</a>
                <a href="food-main.html" class="nav-item">식단/음식</a>
                <a href="exercise-main.html" class="nav-item">운동/활동</a>
                <a href="lifestyle-main.html" class="nav-item">생활습관</a>
                <a href="news-main.html" class="nav-item">건강News</a>
            </nav>
            
            <button class="mobile-menu-btn" id="mobileMenuBtn">☰</button>
        </div>
    </header>

    <!-- 메인 콘텐츠 -->
    <div class="site-main">
        <a href="index-v3.html" class="back-button">← 뒤로가기</a>
        
        <h1 class="page-title">📰 건강News</h1>
        <p class="page-subtitle">최신 건강 정보와 의학 뉴스를 확인하세요</p>
        
        <div class="posts-grid" id="postsGrid">
            <div class="loading-message">
                📰 최신 건강 뉴스를 불러오는 중...
            </div>
        </div>
    </div>

    <script>
        // 모바일 메뉴 토글
        document.getElementById('mobileMenuBtn').addEventListener('click', function() {
            document.getElementById('mainNav').classList.toggle('active');
        });
    
        document.getElementById('mobileCloseBtn').addEventListener('click', function() {
            document.getElementById('mainNav').classList.remove('active');
        });

        // WordPress REST API에서 최신 뉴스 불러오기
        async function loadNews() {
            const postsGrid = document.getElementById('postsGrid');
            
            try {
                // WordPress REST API - 카테고리 ID 또는 slug로 필터링
                // 'news', '건강news', '건강-news', 'health-news' 등의 슬러그 시도
                const possibleSlugs = ['news', '건강news', '건강-news', 'health-news', 'news-category'];
                let posts = [];
                
                // 카테고리 없이 모든 글을 최신순으로 가져오기 (임시)
                const response = await fetch('https://health9988234.mycafe24.com/wp-json/wp/v2/posts?per_page=20&orderby=date&order=desc');
                
                if (!response.ok) {
                    throw new Error('글을 불러올 수 없습니다');
                }
                
                posts = await response.json();
                
                if (posts.length === 0) {
                    postsGrid.innerHTML = '<div class="loading-message">📝 등록된 뉴스가 없습니다</div>';
                    return;
                }
                
                // 글 카드 생성
                postsGrid.innerHTML = posts.map(post => {
                    const title = post.title.rendered;
                    const excerpt = post.excerpt.rendered.replace(/<[^>]*>/g, '').substring(0, 120) + '...';
                    const link = post.link;
                    const date = new Date(post.date).toLocaleDateString('ko-KR');
                    const thumbnail = post.featured_media_url || 'https://via.placeholder.com/400x250/667eea/ffffff?text=9988+건강+연구소';
                    
                    return `
                        <a href="${link}" class="post-card" target="_blank">
                            <img src="${thumbnail}" alt="${title}" class="post-thumbnail" onerror="this.src='https://via.placeholder.com/400x250/667eea/ffffff?text=9988'">
                            <div class="post-content">
                                <span class="post-category">건강News</span>
                                <h3 class="post-title">${title}</h3>
                                <p class="post-excerpt">${excerpt}</p>
                                <div class="post-meta">
                                    <span>📅 ${date}</span>
                                    <span>자세히 보기 →</span>
                                </div>
                            </div>
                        </a>
                    `;
                }).join('');
                
            } catch (error) {
                console.error('뉴스 로드 오류:', error);
                postsGrid.innerHTML = '<div class="error-message">❌ 뉴스를 불러오는 중 오류가 발생했습니다</div>';
            }
        }
        
        // 페이지 로드 시 뉴스 불러오기
        document.addEventListener('DOMContentLoaded', loadNews);
    </script>
</body>
</html>'''

try:
    with open('news-main.html', 'w', encoding='utf-8') as f:
        f.write(news_html)
    
    print("\n✅ news-main.html 완전 재작성 완료!")
    print("\n특징:")
    print("  ✅ WordPress REST API 연동")
    print("  ✅ 최신글 20개를 최신순으로 표시")
    print("  ✅ 카드형 뉴스 레이아웃")
    print("  ✅ 썸네일 이미지 지원")
    print("  ✅ 날짜 및 메타 정보 표시")
    print("  ✅ 모바일 반응형 디자인")
    
    import os
    size = os.path.getsize('news-main.html') / 1024
    print(f"\n파일 크기: {size:.1f} KB")
    
    print("\n" + "=" * 70)
    print("🎉 완료!")
    print("=" * 70)
    
except Exception as e:
    print(f"\n❌ 오류: {e}")
    import traceback
    traceback.print_exc()

