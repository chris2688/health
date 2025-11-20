import os
import glob
import re
import sys
import io

# UTF-8 인코딩 설정
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 워드프레스 포스트 로딩 스크립트
WP_POST_LOADER_SCRIPT = '''
    <script>
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
                    const catResponse = await fetch(`https://health9988234.mycafe24.com/wp-json/wp/v2/categories?slug=${categorySlug}`);
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
                
                // 포스트 목록 렌더링
                newsGrid.innerHTML = posts.map(post => {
                    const thumbnail = post._embedded?.['wp:featuredmedia']?.[0]?.source_url || '';
                    const title = post.title.rendered;
                    const date = new Date(post.date).toLocaleDateString('ko-KR');
                    const backUrl = encodeURIComponent(window.location.pathname.split('/').pop());
                    
                    return `
                        <a href="post-detail.html?id=${post.id}&back=${backUrl}" class="news-item">
                            <div class="news-thumbnail">
                                ${thumbnail ? 
                                    `<img src="${thumbnail}" alt="${title}" loading="lazy">` :
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
                newsGrid.innerHTML = `
                    <div class="no-posts-message" style="grid-column: 1 / -1;">
                        <p>❌ 글을 불러오는데 실패했습니다</p>
                        <p style="font-size: 14px; margin-top: 10px; color: #ccc;">잠시 후 다시 시도해주세요</p>
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

def add_wp_loader_to_file(filepath):
    """파일에 워드프레스 포스트 로더 스크립트 추가"""
    print(f"Processing: {filepath}")
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 이미 스크립트가 있으면 스킵
        if 'loadPosts(categorySlug)' in content:
            print(f"  ⏭️  이미 스크립트가 있음, 스킵")
            return False
        
        # </body> 전에 스크립트 삽입
        if '</body>' in content:
            content = content.replace('</body>', WP_POST_LOADER_SCRIPT + '\n</body>')
        else:
            print(f"  ⚠️  </body> 태그를 찾을 수 없음")
            return False
        
        # 파일 저장
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"  ✅ 스크립트 추가 완료!")
        return True
        
    except Exception as e:
        print(f"  ❌ 오류: {e}")
        return False

def main():
    print("=" * 60)
    print("🔌 워드프레스 포스트 연동 스크립트 추가")
    print("=" * 60)
    
    # news-main.html과 모든 sub-*.html 파일 처리
    target_files = ['news-main.html'] + glob.glob("sub-*.html")
    
    print(f"\n📁 총 {len(target_files)}개 파일")
    
    success_count = 0
    for file in target_files:
        if add_wp_loader_to_file(file):
            success_count += 1
    
    print("\n" + "=" * 60)
    print(f"✅ 완료: {success_count}/{len(target_files)}개 파일")
    print("=" * 60)
    print("\n📝 추가된 기능:")
    print("  - 워드프레스 REST API 연동")
    print("  - 자동 포스트 로딩")
    print("  - 썸네일 이미지 표시")
    print("  - post-detail.html 연결")
    print("  - 로딩 스피너")
    print("  - 에러 처리")

if __name__ == "__main__":
    main()

