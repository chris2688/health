import os
import re
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

def fix_category_file(filepath):
    """카테고리 파일 구조 수정"""
    if not os.path.exists(filepath):
        print(f"  ⚠️ 파일 없음: {filepath}")
        return False
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 1. health-cards-grid 닫는 태그 확인
        # 패턴: </a> 다음에 빈 줄들이 있고, 그 다음에 </div>가 없으면 추가
        pattern = r'(</a>\s*\n\s*\n\s*)(</div>|</style>|<style>|</script>)'
        matches = list(re.finditer(pattern, content))
        if matches:
            # 마지막 health-card 다음의 패턴 찾기
            for match in reversed(matches):
                if match.group(2) not in ['</div>']:
                    # </div> 추가
                    before = content[:match.start()]
                    after = content[match.end():]
                    replacement = match.group(1) + '</div>\n\n        </div>\n\n    </div>\n\n    ' + match.group(2)
                    content = before + replacement + after
                    break
        
        # 2. posts-section이 health-card-container 밖에 있는지 확인
        if '<div class="health-card-container">' in content and '<div class="posts-section">' in content:
            # posts-section이 health-card-container 안에 있으면 밖으로 이동
            pattern = r'(</div>\s*</div>\s*</div>\s*)(<div class="posts-section">)'
            if re.search(pattern, content):
                # 이미 밖에 있음
                pass
            else:
                # 안에 있으면 밖으로 이동
                pattern2 = r'(</div>\s*</div>\s*)(<div class="posts-section">)'
                if re.search(pattern2, content):
                    content = re.sub(pattern2, r'\1</div>\n\n    \2', content)
        
        # 3. style 태그가 body 안에 있으면 head로 이동 (하지만 이미 head에 있을 수 있으므로 확인만)
        
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
        
    except Exception as e:
        print(f"  ❌ {filepath} - 오류: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """메인 실행"""
    print("=" * 60)
    print("🔧 category-심혈관질환.html 구조 수정")
    print("=" * 60)
    
    filepath = "category-심혈관질환.html"
    if fix_category_file(filepath):
        print(f"  ✅ {filepath} - 구조 수정 완료")
    else:
        print(f"  ℹ️ {filepath} - 변경사항 없음")
    
    print("=" * 60)

if __name__ == "__main__":
    main()

