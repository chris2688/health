import urllib.request
import urllib.parse
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

BASE_URL = "https://health9988234.mycafe24.com/"

FILES_TO_DOWNLOAD = [
    "index-v2.html",
    "category-심혈관질환.html",
    "category-당뇨병.html",
    "category-관절근골격계.html",
    "category-호르몬내분비.html",
    "category-정신건강신경계.html",
    "category-소화기질환.html",
    "category-안과치과기타.html",
    "food-main.html",
    "exercise-main.html",
    "lifestyle-main.html",
    "news-main.html",
    "food-피해야할과일.html",
    "food-질환별식단.html",
    "food-모르면독이된다.html",
    "exercise-질환별운동가이드.html",
    "exercise-운동팁.html",
    "lifestyle-생활습관.html",
    "lifestyle-생활습관바꾸기팁.html",
]

def download_file(filename):
    # URL 인코딩 (한글 파일명 처리)
    encoded_filename = urllib.parse.quote(filename, safe='')
    url = BASE_URL + encoded_filename
    try:
        print(f"  다운로드 중: {filename}...", end=" ")
        with urllib.request.urlopen(url) as response:
            content = response.read().decode('utf-8')
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ 완료 ({len(content)} bytes)")
        return True
    except Exception as e:
        print(f"❌ 실패: {e}")
        return False

def main():
    print("=" * 60)
    print("📥 웹사이트에서 모든 파일 다운로드")
    print("=" * 60)
    print("\n💡 X 버튼 요청 이전 상태로 복구하기 위해")
    print("   웹사이트의 파일을 다운로드합니다.\n")
    
    print("📥 파일 다운로드 시작...\n")
    
    downloaded = []
    failed = []
    
    for filename in FILES_TO_DOWNLOAD:
        if download_file(filename):
            downloaded.append(filename)
        else:
            failed.append(filename)
    
    print("\n" + "=" * 60)
    print("✅ 다운로드 완료!")
    print("=" * 60)
    print(f"\n📊 다운로드 결과:")
    print(f"   ✅ 성공: {len(downloaded)}개")
    if failed:
        print(f"   ❌ 실패: {len(failed)}개")
        for filename in failed:
            print(f"      - {filename}")
    
    print("\n💡 이제 복구 스크립트를 실행하세요.")
    print("=" * 60)

if __name__ == "__main__":
    main()

