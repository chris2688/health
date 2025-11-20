import requests
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print("WordPress REST API 상태 확인 중...")
print("=" * 60)

try:
    # Posts endpoint 확인
    url = "https://health9988234.mycafe24.com/wp-json/wp/v2/posts"
    response = requests.get(url, timeout=10)
    print(f"[OK] Posts API: {response.status_code}")
    if response.status_code == 200:
        posts = response.json()
        print(f"   총 {len(posts)}개 포스트 반환")
    else:
        print(f"   오류: {response.text[:200]}")
except Exception as e:
    print(f"[ERROR] Posts API 오류: {e}")

print()

try:
    # Categories endpoint 확인
    url = "https://health9988234.mycafe24.com/wp-json/wp/v2/categories"
    response = requests.get(url, timeout=10)
    print(f"[OK] Categories API: {response.status_code}")
    if response.status_code == 200:
        cats = response.json()
        print(f"   총 {len(cats)}개 카테고리 반환")
    else:
        print(f"   오류: {response.text[:200]}")
except Exception as e:
    print(f"[ERROR] Categories API 오류: {e}")

print("=" * 60)

