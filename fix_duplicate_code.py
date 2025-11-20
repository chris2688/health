import os
import re
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 모든 sub-*.html 파일 찾기
SUBCATEGORY_FILES = [f for f in os.listdir('.') if f.startswith('sub-') and f.endswith('.html')]

def fix_duplicate_code(filepath):
    """중복된 코드 제거"""
    if not os.path.exists(filepath):
        return False
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 중복된 loadPosts 호출 제거
        pattern = r'loadPosts\([^)]+\);\s*\}\);loadPosts\([^)]+\);\s*\}\);'
        if re.search(pattern, content):
            content = re.sub(pattern, lambda m: m.group(0).split('});')[0] + '});', content)
        
        # 다른 패턴: loadPosts가 두 번 연속
        pattern2 = r'(loadPosts\([^)]+\);)\s*\1'
        if re.search(pattern2, content):
            content = re.sub(pattern2, r'\1', content)
        
        # 중복된 }); 제거
        pattern3 = r'\}\);\s*loadPosts\([^)]+\);\s*\}\);'
        if re.search(pattern3, content):
            content = re.sub(pattern3, '});', content)
        
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
    print("🔧 중복 코드 제거")
    print("=" * 60)
    print(f"\n📝 총 {len(SUBCATEGORY_FILES)}개 파일 처리 중...\n")
    
    updated_count = 0
    
    for filename in SUBCATEGORY_FILES:
        if fix_duplicate_code(filename):
            print(f"  ✅ {filename} - 수정 완료")
            updated_count += 1
        else:
            print(f"  ℹ️ {filename} - 변경사항 없음")
    
    print(f"\n✅ 총 {updated_count}개 파일 수정 완료!")
    print("=" * 60)

if __name__ == "__main__":
    main()

