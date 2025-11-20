import os
import glob
import sys
import io
import shutil

# UTF-8 인코딩 설정
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 개선된 스크립트 (sub-고혈압.html에서 복사)
def get_improved_script():
    with open('sub-고혈압.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 스크립트 부분 추출
    start = content.find('<script>', content.find('// 썸네일 이미지 가져오기'))
    end = content.find('</script>', start) + len('</script>')
    
    return content[start:end]

def update_file(filepath):
    """파일의 스크립트 부분을 개선된 버전으로 교체"""
    print(f"Processing: {filepath}")
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 이미 개선된 버전이 있으면 스킵
        if 'function getThumbnailUrl(post)' in content:
            print(f"  ⏭️  이미 개선됨, 스킵")
            return False
        
        # 기존 스크립트 찾기
        old_start = content.find('<script>', content.find('// 워드프레스 REST API로 포스트 목록 가져오기'))
        if old_start == -1:
            print(f"  ⚠️  스크립트를 찾을 수 없음")
            return False
        
        old_end = content.find('</script>', old_start) + len('</script>')
        
        # 개선된 스크립트로 교체
        improved_script = get_improved_script()
        content = content[:old_start] + improved_script + content[old_end:]
        
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
    print("🖼️  모든 서브 페이지 썸네일 로딩 개선 (일괄 적용)")
    print("=" * 60)
    
    # sub-고혈압.html 제외 (이미 수정됨)
    target_files = [f for f in glob.glob("sub-*.html") if f != 'sub-고혈압.html']
    
    print(f"\n📁 총 {len(target_files)}개 파일")
    
    success_count = 0
    for file in target_files:
        if update_file(file):
            success_count += 1
    
    print("\n" + "=" * 60)
    print(f"✅ 완료: {success_count}/{len(target_files)}개 파일")
    print("=" * 60)

if __name__ == "__main__":
    main()

