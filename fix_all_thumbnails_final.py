import os
import glob
import sys
import io

# UTF-8 인코딩 설정
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

def fix_file(filepath):
    """파일의 썸네일 로딩 로직 개선"""
    print(f"Processing: {filepath}")
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 이미 개선된 버전이 있으면 스킵
        if 'function getThumbnailUrl(post)' in content:
            print(f"  ⏭️  이미 개선됨, 스킵")
            return False
        
        # 1. getThumbnailUrl 함수 추가 (loadPosts 함수 앞에)
        old_loadposts = '        // 워드프레스 REST API로 포스트 목록 가져오기\n        async function loadPosts(categorySlug) {'
        new_loadposts = '''        // 썸네일 이미지 가져오기 (개선된 버전)
        function getThumbnailUrl(post) {
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
            
            // 방법 2: 본문에서 첫 번째 이미지 추출
            if (post.content && post.content.rendered) {
                const imgMatch = post.content.rendered.match(/<img[^>]+src=["\']([^"\']+)["\']/i);
                if (imgMatch && imgMatch[1]) {
                    // 상대 경로를 절대 경로로 변환
                    let imgUrl = imgMatch[1];
                    if (imgUrl.startsWith('/')) {
                        imgUrl = 'https://health9988234.mycafe24.com' + imgUrl;
                    } else if (!imgUrl.startsWith('http')) {
                        imgUrl = 'https://health9988234.mycafe24.com/' + imgUrl;
                    }
                    return imgUrl;
                }
            }
            
            return null;
        }
        
        // 워드프레스 REST API로 포스트 목록 가져오기
        async function loadPosts(categorySlug) {'''
        
        if old_loadposts in content:
            content = content.replace(old_loadposts, new_loadposts)
        else:
            print(f"  ⚠️  loadPosts 함수를 찾을 수 없음")
            return False
        
        # 2. 썸네일 가져오기 부분 수정
        old_thumbnail = "                    const thumbnail = post._embedded?.['wp:featuredmedia']?.[0]?.source_url || '';"
        new_thumbnail = "                    const thumbnail = getThumbnailUrl(post);"
        content = content.replace(old_thumbnail, new_thumbnail)
        
        # 3. 이미지 태그에 onerror 추가
        old_img = '                                    `<img src="${thumbnail}" alt="${title}" loading="lazy">` :'
        new_img = '                                    `<img src="${thumbnail}" alt="${title}" loading="lazy" onerror="this.parentElement.innerHTML=\'<div class=\\\'news-thumbnail-placeholder\\\'>📄</div>\'">` :'
        content = content.replace(old_img, new_img)
        
        # 4. 카테고리 슬러그 인코딩
        old_cat = '                    const catResponse = await fetch(`https://health9988234.mycafe24.com/wp-json/wp/v2/categories?slug=${categorySlug}`);'
        new_cat = '                    const catResponse = await fetch(`https://health9988234.mycafe24.com/wp-json/wp/v2/categories?slug=${encodeURIComponent(categorySlug)}`);'
        content = content.replace(old_cat, new_cat)
        
        # 5. 에러 메시지 개선
        old_error = '                        <p style="font-size: 14px; margin-top: 10px; color: #ccc;">잠시 후 다시 시도해주세요</p>\n                    </div>'
        new_error = '                        <p style="font-size: 14px; margin-top: 10px; color: #ccc;">잠시 후 다시 시도해주세요</p>\n                        <p style="font-size: 12px; margin-top: 5px; color: #999;">에러: ${error.message}</p>\n                    </div>'
        content = content.replace(old_error, new_error)
        
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
    print("🖼️  모든 서브 페이지 썸네일 로딩 개선 (최종)")
    print("=" * 60)
    
    # sub-고혈압.html과 news-main.html 제외 (이미 수정됨)
    target_files = [f for f in glob.glob("sub-*.html") if f not in ['sub-고혈압.html']]
    
    print(f"\n📁 총 {len(target_files)}개 파일")
    
    success_count = 0
    for file in target_files:
        if fix_file(file):
            success_count += 1
    
    print("\n" + "=" * 60)
    print(f"✅ 완료: {success_count}/{len(target_files)}개 파일")
    print("=" * 60)
    print("\n📝 개선사항:")
    print("  ✅ 방법 1: _embedded에서 썸네일 가져오기 (여러 크기 시도)")
    print("  ✅ 방법 2: 본문에서 첫 번째 이미지 추출")
    print("  ✅ 상대 경로를 절대 경로로 자동 변환")
    print("  ✅ 이미지 로딩 실패 시 자동 fallback")
    print("  ✅ 카테고리 슬러그 URL 인코딩")

if __name__ == "__main__":
    main()

