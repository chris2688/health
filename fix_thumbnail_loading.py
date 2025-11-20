import os
import glob
import re
import sys
import io

# UTF-8 인코딩 설정
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 개선된 썸네일 로딩 스크립트
IMPROVED_THUMBNAIL_SCRIPT = '''
    <script>
        // 썸네일 이미지 가져오기 (개선된 버전)
        async function getThumbnailUrl(post) {
            // 방법 1: _embedded에서 가져오기
            if (post._embedded && post._embedded['wp:featuredmedia'] && post._embedded['wp:featuredmedia'][0]) {
                const media = post._embedded['wp:featuredmedia'][0];
                if (media.source_url) {
                    return media.source_url;
                }
                if (media.media_details && media.media_details.sizes) {
                    // 큰 이미지부터 시도
                    const sizes = ['large', 'medium_large', 'medium', 'full'];
                    for (const size of sizes) {
                        if (media.media_details.sizes[size] && media.media_details.sizes[size].source_url) {
                            return media.media_details.sizes[size].source_url;
                        }
                    }
                }
            }
            
            // 방법 2: featured_media ID로 직접 가져오기
            if (post.featured_media && post.featured_media > 0) {
                try {
                    const mediaResponse = await fetch(`https://health9988234.mycafe24.com/wp-json/wp/v2/media/${post.featured_media}`);
                    if (mediaResponse.ok) {
                        const media = await mediaResponse.json();
                        if (media.source_url) {
                            return media.source_url;
                        }
                    }
                } catch (e) {
                    console.log('Media fetch error:', e);
                }
            }
            
            // 방법 3: 본문에서 첫 번째 이미지 추출
            if (post.content && post.content.rendered) {
                const imgMatch = post.content.rendered.match(/<img[^>]+src=["\']([^"\']+)["\']/i);
                if (imgMatch && imgMatch[1]) {
                    // 상대 경로를 절대 경로로 변환
                    let imgUrl = imgMatch[1];
                    if (imgUrl.startsWith('/')) {
                        imgUrl = 'https://health9988234.mycafe24.com' + imgUrl;
                    }
                    return imgUrl;
                }
            }
            
            return null;
        }
        
        // 워드프레스 REST API로 포스트 목록 가져오기
        async function loadPosts(categorySlug) {
            const newsGrid = document.querySelector('.news-grid');
            
            // 로딩 메시지
            newsGrid.innerHTML = `
                <div class="no-posts-message" style="grid-column: 1 / -1;">
                    <div class="spinner"></div>
                    <p>글을 불러오는 중...</p>
                </div>
            `;
            
            try {
                // 카테고리 ID 가져오기 (슬러그로)
                let apiUrl = 'https://health9988234.mycafe24.com/wp-json/wp/v2/posts?per_page=20&_embed';
                
                if (categorySlug) {
                    const catResponse = await fetch(`https://health9988234.mycafe24.com/wp-json/wp/v2/categories?slug=${encodeURIComponent(categorySlug)}`);
                    const categories = await catResponse.json();
                    
                    if (categories.length > 0) {
                        apiUrl += `&categories=${categories[0].id}`;
                    }
                }
                
                const response = await fetch(apiUrl);
                const posts = await response.json();
                
                if (posts.length === 0) {
                    newsGrid.innerHTML = `
                        <div class="no-posts-message" style="grid-column: 1 / -1;">
                            <p>📝 아직 작성된 글이 없습니다</p>
                            <p style="font-size: 14px; margin-top: 10px; color: #ccc;">곧 업데이트될 예정입니다</p>
                        </div>
                    `;
                    return;
                }
                
                // 각 포스트의 썸네일을 가져와서 렌더링
                const postItems = await Promise.all(posts.map(async (post) => {
                    const thumbnail = await getThumbnailUrl(post);
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
                }));
                
                newsGrid.innerHTML = postItems.join('');
                
            } catch (error) {
                console.error('Error loading posts:', error);
                newsGrid.innerHTML = `
                    <div class="no-posts-message" style="grid-column: 1 / -1;">
                        <p>❌ 글을 불러오는데 실패했습니다</p>
                        <p style="font-size: 14px; margin-top: 10px; color: #ccc;">잠시 후 다시 시도해주세요</p>
                        <p style="font-size: 12px; margin-top: 5px; color: #999;">에러: ${error.message}</p>
                    </div>
                `;
            }
        }
        
        // 페이지 로드 시 실행
        document.addEventListener('DOMContentLoaded', function() {
            // 페이지별 카테고리 슬러그 매핑
            const pageToCategory = {
                'news-main.html': 'health-news',  // 건강News 카테고리 슬러그
                'sub-고혈압.html': 'hypertension',
                'sub-당뇨.html': 'diabetes',
                'sub-고지혈증.html': 'hyperlipidemia',
                // 필요한 매핑 추가...
            };
            
            const currentPage = window.location.pathname.split('/').pop();
            const categorySlug = pageToCategory[currentPage] || null;
            
            loadPosts(categorySlug);
        });
    </script>
    
    <style>
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
    </style>
'''

def update_file_thumbnail_script(filepath):
    """파일의 썸네일 로딩 스크립트를 개선된 버전으로 교체"""
    print(f"Updating: {filepath}")
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 기존 스크립트 부분 찾기 (loadPosts 함수부터 </script>까지)
        pattern = r'<script>\s*// 워드프레스 REST API로 포스트 목록 가져오기.*?</script>\s*<style>\s*\.spinner'
        
        if re.search(pattern, content, re.DOTALL):
            # 기존 스크립트 교체
            content = re.sub(pattern, IMPROVED_THUMBNAIL_SCRIPT.replace('<script>', '<script>').replace('</script>', '</script>'), content, flags=re.DOTALL)
        else:
            # 스크립트가 없으면 추가
            if '</body>' in content:
                content = content.replace('</body>', IMPROVED_THUMBNAIL_SCRIPT + '\n</body>')
            else:
                print(f"  ⚠️  </body> 태그를 찾을 수 없음")
                return False
        
        # 파일 저장
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"  ✅ 썸네일 로딩 스크립트 개선 완료!")
        return True
        
    except Exception as e:
        print(f"  ❌ 오류: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("=" * 60)
    print("🖼️  썸네일 로딩 개선 - 다중 방법 시도")
    print("=" * 60)
    
    # news-main.html과 모든 sub-*.html 파일 처리
    target_files = ['news-main.html'] + glob.glob("sub-*.html")
    
    print(f"\n📁 총 {len(target_files)}개 파일")
    
    success_count = 0
    for file in target_files:
        if update_file_thumbnail_script(file):
            success_count += 1
    
    print("\n" + "=" * 60)
    print(f"✅ 완료: {success_count}/{len(target_files)}개 파일")
    print("=" * 60)
    print("\n📝 개선사항:")
    print("  - 방법 1: _embedded에서 썸네일 가져오기")
    print("  - 방법 2: featured_media ID로 직접 API 호출")
    print("  - 방법 3: 본문에서 첫 번째 이미지 추출")
    print("  - 이미지 로딩 실패 시 자동 fallback")
    print("  - 상대 경로를 절대 경로로 자동 변환")

if __name__ == "__main__":
    main()

