import os
import glob
import re
import sys
import io

# UTF-8 인코딩 설정
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

def remove_duplicates(filepath):
    """중복된 헤더 제거 및 뒤로가기 버튼 제거"""
    print(f"Processing: {filepath}")
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 중복된 헤더 제거 (두 번째 헤더만 삭제)
        header_pattern = r'(<header class="main-header">.*?</header>)\s*<header class="main-header">.*?</header>'
        content = re.sub(header_pattern, r'\1', content, flags=re.DOTALL)
        
        # 중복된 스크립트 제거
        script_pattern = r'(<script>\s*document\.getElementById\(\'mobileMenuBtn\'\).*?</script>)\s*<script>\s*document\.getElementById\(\'mobileMenuBtn\'\).*?</script>'
        content = re.sub(script_pattern, r'\1', content, flags=re.DOTALL)
        
        # "← 홈으로 돌아가기" 버튼 제거
        back_button_pattern = r'<a href="index-v2\.html" class="back-link">← 홈으로 돌아가기</a>\s*'
        content = re.sub(back_button_pattern, '', content)
        
        # 파일 저장
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"  ✅ 수정 완료!")
        return True
        
    except Exception as e:
        print(f"  ❌ 오류: {e}")
        return False

def main():
    print("=" * 60)
    print("🔧 중복 제거 및 정리")
    print("=" * 60)
    
    # 모든 HTML 파일 처리
    all_files = glob.glob("category-*.html") + glob.glob("sub-*.html")
    print(f"\n📁 총 {len(all_files)}개 파일")
    
    success_count = 0
    for file in all_files:
        if remove_duplicates(file):
            success_count += 1
    
    print("\n" + "=" * 60)
    print(f"✅ 완료: {success_count}/{len(all_files)}개 파일 수정")
    print("=" * 60)

if __name__ == "__main__":
    main()

