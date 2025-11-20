import os
import re
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 업데이트할 파일 목록
HTML_FILES = []
for file in os.listdir('.'):
    if file.endswith('.html') and file != 'index-v3.html':
        HTML_FILES.append(file)

def update_links_in_file(filepath):
    """파일 내의 index-v2.html 링크를 index-v3.html로 업데이트"""
    if not os.path.exists(filepath):
        return False
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # index-v2.html을 index-v3.html로 변경
        content = content.replace('href="index-v2.html"', 'href="index-v3.html"')
        content = content.replace("href='index-v2.html'", "href='index-v3.html'")
        content = content.replace('href=index-v2.html', 'href=index-v3.html')
        
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
        
    except Exception as e:
        print(f"  ❌ {filepath} - 오류: {e}")
        return False

def main():
    """메인 실행"""
    print("=" * 60)
    print("🔗 모든 페이지 링크를 index-v3.html로 업데이트")
    print("=" * 60)
    print(f"\n📝 총 {len(HTML_FILES)}개 파일 처리 중...\n")
    
    updated_count = 0
    
    for file in HTML_FILES:
        if update_links_in_file(file):
            print(f"  ✅ {file} - 업데이트 완료")
            updated_count += 1
        else:
            print(f"  ℹ️ {file} - 변경사항 없음")
    
    print(f"\n✅ 총 {updated_count}개 파일 업데이트 완료!")
    print("=" * 60)

if __name__ == "__main__":
    main()

