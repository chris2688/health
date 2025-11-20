import requests
import json
import sys
import io

# UTF-8 인코딩 설정
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

WP_BASE_URL = "https://health9988234.mycafe24.com"

def check_posts_in_category(category_slug, search_term):
    """특정 카테고리에서 검색어가 포함된 글 찾기"""
    print(f"\n🔍 '{search_term}' 관련 글 검색 (카테고리: {category_slug})")
    
    try:
        # 카테고리 ID 가져오기
        cat_response = requests.get(f"{WP_BASE_URL}/wp-json/wp/v2/categories?slug={category_slug}")
        categories = cat_response.json()
        
        if not categories:
            print(f"  ❌ 카테고리 '{category_slug}'를 찾을 수 없습니다")
            return []
        
        category_id = categories[0]['id']
        print(f"  카테고리 ID: {category_id}, 이름: {categories[0]['name']}")
        
        # 해당 카테고리의 글 가져오기
        posts_response = requests.get(f"{WP_BASE_URL}/wp-json/wp/v2/posts?categories={category_id}&per_page=20&search={search_term}")
        posts = posts_response.json()
        
        print(f"  📝 발견된 글: {len(posts)}개")
        for post in posts:
            print(f"    - {post['title']['rendered']}")
        
        return posts
        
    except Exception as e:
        print(f"  ❌ 오류: {e}")
        return []

def main():
    print("=" * 60)
    print("🔍 역류성 식도염 관련 글 카테고리 확인")
    print("=" * 60)
    
    # 여러 카테고리에서 검색
    categories_to_check = [
        ('digestive', '소화기 질환'),
        ('cardiovascular', '심혈관 질환'),
        ('disease-info', '질환별 정보'),
    ]
    
    search_terms = ['역류성 식도염', '역류', '식도염']
    
    for category_slug, category_name in categories_to_check:
        print(f"\n{'='*60}")
        print(f"카테고리: {category_name} ({category_slug})")
        print('='*60)
        
        for term in search_terms:
            posts = check_posts_in_category(category_slug, term)
            if posts:
                print(f"  ✅ '{term}' 관련 글이 '{category_name}' 카테고리에 있습니다!")
                break

if __name__ == "__main__":
    main()

