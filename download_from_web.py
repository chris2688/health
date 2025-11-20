import urllib.request
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

url = "https://health9988234.mycafe24.com/index-v2.html"

try:
    print("웹사이트에서 파일 다운로드 중...")
    with urllib.request.urlopen(url) as response:
        content = response.read().decode('utf-8')
    
    with open('index-v2.html', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ index-v2.html 다운로드 완료! ({len(content)} bytes)")
except Exception as e:
    print(f"❌ 오류: {e}")

