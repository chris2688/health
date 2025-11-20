import sys
import io
import requests
import json

# UTF-8 인코딩 설정
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

WP_BASE_URL = "https://health9988234.mycafe24.com"
WP_API_URL = f"{WP_BASE_URL}/wp-json/wp/v2"

def get_all_categories():
    """WordPress에서 모든 카테고리 가져오기"""
    print("=" * 60)
    print("📂 WordPress 카테고리 확인")
    print("=" * 60)
    
    try:
        # 카테고리 가져오기
        url = f"{WP_API_URL}/categories?per_page=100"
        print(f"\n🔗 API 호출: {url}\n")
        
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            categories = response.json()
            print(f"✅ 총 {len(categories)}개 카테고리 발견\n")
            
            # 카테고리 정보 출력
            print("-" * 60)
            print(f"{'ID':<5} {'이름':<30} {'슬러그':<40} {'URL'}")
            print("-" * 60)
            
            for cat in categories:
                cat_id = cat.get('id', '')
                name = cat.get('name', '')
                slug = cat.get('slug', '')
                link = cat.get('link', '')
                
                print(f"{cat_id:<5} {name:<30} {slug:<40} {link}")
            
            print("-" * 60)
            
            # 질환별 정보 관련 카테고리만 필터링
            print("\n📋 '질환별-정보' 관련 카테고리:")
            print("-" * 60)
            
            disease_categories = []
            for cat in categories:
                name = cat.get('name', '')
                slug = cat.get('slug', '')
                link = cat.get('link', '')
                
                # 질환 관련 키워드가 포함된 카테고리
                keywords = ['질환', '심혈관', '당뇨', '관절', '호르몬', '정신', '소화기', '안과', '치과']
                if any(keyword in name for keyword in keywords):
                    disease_categories.append({
                        'name': name,
                        'slug': slug,
                        'link': link
                    })
                    print(f"  {name:<30} → {slug:<40}")
                    print(f"    URL: {link}")
            
            print("-" * 60)
            
            # 매핑 정보 생성
            print("\n📝 권장 링크 매핑:")
            print("-" * 60)
            
            mapping = {
                "심혈관": None,
                "당뇨": None,
                "관절": None,
                "호르몬": None,
                "정신": None,
                "소화기": None,
                "안과": None,
                "치과": None,
            }
            
            for cat in categories:
                name = cat.get('name', '')
                slug = cat.get('slug', '')
                link = cat.get('link', '')
                
                for key in mapping.keys():
                    if key in name and mapping[key] is None:
                        mapping[key] = link
                        print(f"  '{key}' 관련 → {link}")
            
            print("-" * 60)
            
            # JSON 파일로 저장
            with open('wordpress_categories.json', 'w', encoding='utf-8') as f:
                json.dump(categories, f, ensure_ascii=False, indent=2)
            print(f"\n✅ 카테고리 정보를 'wordpress_categories.json'에 저장했습니다.")
            
            return categories
            
        else:
            print(f"❌ API 호출 실패: {response.status_code}")
            print(f"   응답: {response.text[:200]}")
            return None
            
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        return None


if __name__ == "__main__":
    categories = get_all_categories()
    
    if categories:
        print("\n" + "=" * 60)
        print("💡 다음 단계:")
        print("   1. 위의 카테고리 정보를 확인하세요")
        print("   2. 실제 카테고리 URL로 HTML 링크를 수정하세요")
        print("=" * 60)

