import os
import glob
import sys
import io

# UTF-8 인코딩 설정
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 개선된 스크립트 (sub-고혈압.html에서 복사)
def get_improved_script():
    with open('sub-고혈압.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 스마트 매핑 함수와 DOMContentLoaded 부분 추출
    start = content.find('// 페이지 제목 기반 카테고리 자동 매핑')
    end = content.find('</script>', start) + len('</script>')
    
    return content[start:end]

def update_file(filepath):
    """파일의 카테고리 매핑 부분을 스마트 매핑으로 교체"""
    print(f"Processing: {filepath}")
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 이미 스마트 매핑이 있으면 스킵
        if 'async function findCategoryByPageTitle' in content:
            print(f"  ⏭️  이미 스마트 매핑이 있음, 스킵")
            return False
        
        # 기존 DOMContentLoaded 부분 찾기
        old_start = content.find('// 페이지 로드 시 실행')
        if old_start == -1:
            print(f"  ⚠️  DOMContentLoaded 핸들러를 찾을 수 없음")
            return False
        
        old_end = content.find('</script>', old_start) + len('</script>')
        
        # 개선된 스크립트로 교체
        improved_script = get_improved_script()
        content = content[:old_start] + improved_script
        
        # 파일 저장
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"  ✅ 완료!")
        return True
        
    except Exception as e:
        print(f"  ❌ 오류: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("=" * 60)
    print("🧠 모든 페이지에 스마트 카테고리 매핑 적용")
    print("=" * 60)
    
    # sub-고혈압.html 제외 (이미 수정됨)
    target_files = ['news-main.html'] + [f for f in glob.glob("sub-*.html") if f != 'sub-고혈압.html']
    
    print(f"\n📁 총 {len(target_files)}개 파일")
    
    success_count = 0
    for file in target_files:
        if update_file(file):
            success_count += 1
    
    print("\n" + "=" * 60)
    print(f"✅ 완료: {success_count}/{len(target_files)}개 파일")
    print("=" * 60)
    print("\n📝 개선사항:")
    print("  ✅ 페이지 제목 기반 자동 카테고리 매핑")
    print("  ✅ 워드프레스 카테고리와 자동 매칭")
    print("  ✅ 키워드 기반 폴백 매핑")
    print("  ✅ 하드코딩된 매핑도 유지 (백업)")

if __name__ == "__main__":
    main()

