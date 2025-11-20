import os
import re
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 뒤로가기 버튼이 있는 모든 파일
TARGET_FILES = []
for f in os.listdir('.'):
    if f.endswith('.html'):
        with open(f, 'r', encoding='utf-8') as file:
            content = file.read()
            if '뒤로가기' in content or 'back-button' in content:
                TARGET_FILES.append(f)

# 통일된 뒤로가기 버튼 CSS (margin-left 제거, container padding 활용)
UNIFIED_BACK_BUTTON_CSS = '''        .back-button {
            display: inline-block;
            margin: 30px 0 30px 20px;
            padding: 12px 24px;
            background: white;
            color: #667eea;
            text-decoration: none;
            border-radius: 50px;
            font-weight: 600;
            font-size: 16px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            transition: all 0.3s;
        }
        
        .back-button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(0,0,0,0.15);
        }
        
        .back-button::before {
            content: '← ';
            font-weight: bold;
        }'''

def fix_back_button_position(filepath):
    """뒤로가기 버튼 위치를 왼쪽 여백 20px로 통일"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 모든 .back-button CSS 블록 제거
        while True:
            # 주석 포함 블록
            pattern1 = r'/\*[^*]*\*+(?:[^/*][^*]*\*+)*/\s*\.back-button\s*\{[^}]+\}\s*(\.back-button:hover\s*\{[^}]+\}\s*)?(\.back-button::before\s*\{[^}]+\}\s*)?'
            if re.search(pattern1, content, re.DOTALL):
                content = re.sub(pattern1, '', content, count=1, flags=re.DOTALL)
                continue
            
            # 주석 없는 블록
            pattern2 = r'\.back-button\s*\{[^}]+\}\s*\.back-button:hover\s*\{[^}]+\}(\s*\.back-button::before\s*\{[^}]+\})?'
            if re.search(pattern2, content, re.DOTALL):
                # 이미 올바른 스타일인지 확인
                match = re.search(pattern2, content, re.DOTALL)
                if match and 'margin: 30px 0 30px 20px' in match.group(0):
                    break  # 이미 올바른 스타일
                content = re.sub(pattern2, '', content, count=1, flags=re.DOTALL)
            else:
                break
        
        # 새로운 스타일을 body 스타일 뒤나 콘텐츠 영역 앞에 삽입
        # 우선 /* ========== 콘텐츠 영역 ========== */ 앞에 삽입 시도
        insert_pattern1 = r'(/\* =+ 콘텐츠 영역 =+ \*/)'
        if re.search(insert_pattern1, content):
            content = re.sub(insert_pattern1, UNIFIED_BACK_BUTTON_CSS + '\n        \n        \\1', content, count=1)
        else:
            # 없으면 .health-card-container 또는 .site-main 앞에 삽입
            insert_pattern2 = r'(\.health-card-container\s*\{|\.site-main\s*\{)'
            if re.search(insert_pattern2, content):
                content = re.sub(insert_pattern2, UNIFIED_BACK_BUTTON_CSS + '\n        \n        \\1', content, count=1)
        
        # 모바일 미디어 쿼리에서 .back-button margin-left 수정
        mobile_pattern = r'(\.back-button\s*\{\s*margin-left:\s*)[^;]+;'
        content = re.sub(mobile_pattern, r'\120px;', content)
        
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
    print("📍 뒤로가기 버튼 위치 통일 (왼쪽 20px 여백)")
    print("=" * 60)
    print(f"\n📝 총 {len(TARGET_FILES)}개 파일 처리 중...\n")
    
    updated_count = 0
    
    for filename in sorted(TARGET_FILES):
        if fix_back_button_position(filename):
            print(f"  ✅ {filename}")
            updated_count += 1
        else:
            print(f"  ℹ️ {filename} - 변경사항 없음")
    
    print(f"\n✅ 총 {updated_count}개 파일 수정 완료!")
    print("\n📋 적용된 위치:")
    print("   - 왼쪽 여백: 20px")
    print("   - 위쪽 여백: 30px")
    print("   - 아래쪽 여백: 30px")
    print("   - 모든 페이지 동일한 위치")
    print("=" * 60)

if __name__ == "__main__":
    main()
