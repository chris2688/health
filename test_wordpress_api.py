import requests
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

WP_BASE_URL = "https://health9988234.mycafe24.com"

print("=" * 60)
print("🔍 WordPress REST API 테스트")
print("=" * 60)

# 1. 기본 posts API 테스트
print("\n1️⃣ Posts API 테스트...")
try:
    url = f"{WP_BASE_URL}/wp-json/wp/v2/posts?per_page=1"
    print(f"   URL: {url}")
    response = requests.get(url, timeout=10)
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ 성공! {len(data)}개 글 발견")
        if len(data) > 0:
            print(f"   첫 번째 글: {data[0]['title']['rendered']}")
    else:
        print(f"   ❌ 실패: {response.text[:200]}")
except Exception as e:
    print(f"   ❌ 오류: {e}")

# 2. Categories API 테스트
print("\n2️⃣ Categories API 테스트...")
try:
    url = f"{WP_BASE_URL}/wp-json/wp/v2/categories?per_page=10"
    print(f"   URL: {url}")
    response = requests.get(url, timeout=10)
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ 성공! {len(data)}개 카테고리 발견")
        for cat in data[:5]:
            print(f"   - {cat['name']} (slug: {cat['slug']})")
    else:
        print(f"   ❌ 실패: {response.text[:200]}")
except Exception as e:
    print(f"   ❌ 오류: {e}")

# 3. 특정 카테고리로 글 검색 테스트
print("\n3️⃣ '당뇨병' 카테고리로 글 검색 테스트...")
test_slugs = ["당뇨병", "diabetes", "당뇨"]
for slug in test_slugs:
    try:
        # 카테고리 찾기
        cat_url = f"{WP_BASE_URL}/wp-json/wp/v2/categories?slug={slug}"
        print(f"   카테고리 찾기: {cat_url}")
        cat_response = requests.get(cat_url, timeout=10)
        if cat_response.status_code == 200:
            categories = cat_response.json()
            if len(categories) > 0:
                cat_id = categories[0]['id']
                cat_name = categories[0]['name']
                print(f"   ✅ 카테고리 발견: {cat_name} (ID: {cat_id})")
                
                # 해당 카테고리의 글 가져오기
                posts_url = f"{WP_BASE_URL}/wp-json/wp/v2/posts?categories={cat_id}&per_page=5"
                print(f"   글 가져오기: {posts_url}")
                posts_response = requests.get(posts_url, timeout=10)
                if posts_response.status_code == 200:
                    posts = posts_response.json()
                    print(f"   ✅ {len(posts)}개 글 발견")
                    for post in posts[:3]:
                        print(f"      - {post['title']['rendered']}")
                else:
                    print(f"   ❌ 글 가져오기 실패: {posts_response.status_code}")
                break
            else:
                print(f"   ⚠️ 카테고리 없음: {slug}")
        else:
            print(f"   ❌ 카테고리 API 실패: {cat_response.status_code}")
    except Exception as e:
        print(f"   ❌ 오류: {e}")

print("\n" + "=" * 60)
print("✅ 테스트 완료")
print("=" * 60)

