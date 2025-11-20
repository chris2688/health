import requests
import json
import sys
import io

# UTF-8 인코딩 설정
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

WP_BASE_URL = "https://health9988234.mycafe24.com"

def get_all_categories():
    """워드프레스의 모든 카테고리 가져오기"""
    print("=" * 60)
    print("📋 워드프레스 카테고리 목록 가져오기")
    print("=" * 60)
    
    try:
        url = f"{WP_BASE_URL}/wp-json/wp/v2/categories?per_page=100"
        response = requests.get(url)
        response.raise_for_status()
        
        categories = response.json()
        
        print(f"\n✅ 총 {len(categories)}개 카테고리 발견\n")
        
        print("카테고리 목록:")
        print("-" * 60)
        for cat in categories:
            print(f"ID: {cat['id']:3d} | 슬러그: {cat['slug']:30s} | 이름: {cat['name']}")
        
        # JSON 파일로 저장
        with open('wordpress_categories.json', 'w', encoding='utf-8') as f:
            json.dump(categories, f, ensure_ascii=False, indent=2)
        
        print("\n" + "=" * 60)
        print("✅ 카테고리 목록이 'wordpress_categories.json'에 저장되었습니다")
        print("=" * 60)
        
        return categories
        
    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
        return None

if __name__ == "__main__":
    get_all_categories()

