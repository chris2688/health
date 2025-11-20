import requests
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

WP_BASE_URL = "https://health9988234.mycafe24.com"

print("=" * 60)
print("🔍 REST API 응답 확인")
print("=" * 60)

url = f"{WP_BASE_URL}/wp-json/wp/v2/posts?per_page=1"
print(f"\n📡 URL: {url}\n")

try:
    response = requests.get(url, timeout=10)
    print(f"Status Code: {response.status_code}")
    print(f"Content-Type: {response.headers.get('Content-Type', 'N/A')}")
    print(f"\n응답 내용 (처음 500자):")
    print("-" * 60)
    print(response.text[:500])
    print("-" * 60)
    
    if response.status_code == 200:
        try:
            data = response.json()
            print(f"\n✅ JSON 파싱 성공!")
            print(f"   글 개수: {len(data)}")
            if len(data) > 0:
                print(f"   첫 번째 글: {data[0].get('title', {}).get('rendered', 'N/A')}")
        except Exception as e:
            print(f"\n❌ JSON 파싱 실패: {e}")
            print("   응답이 HTML일 수 있습니다")
            
except Exception as e:
    print(f"❌ 오류: {e}")

