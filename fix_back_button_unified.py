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

# 통일된 뒤로가기 버튼 CSS 스타일 (category 파일 스타일 기준)
UNIFIED_BACK_BUTTON_CSS = '''        .back-button {
            display: inline-block;
            margin: 30px 0 30px 0;
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

def fix_back_button_unified(filepath):
    """뒤로가기 버튼 스타일을 통일된 스타일로 교체"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 모든 기존 back-button 관련 CSS 제거
        # 패턴 1: /* ========== 뒤로가기 버튼 (헤더 밖) ========== */ 섹션 제거
        pattern1 = r'/\* =+ 뒤로가기 버튼 \(헤더 밖\) =+ \*/\s*\n(\s*\n)*'
        content = re.sub(pattern1, '', content)
        
        # 패턴 2: 모든 .back-button 관련 CSS 블록 제거
        # 여러 back-button 정의가 있을 수 있으므로 반복적으로 제거
        while True:
            # /* ========== 뒤로가기 버튼 ========== */ 부터 다음 CSS 블록까지
            pattern2 = r'/\* =+ 뒤로가기 버튼 =+ \*/\s*\.back-button\s*\{[^}]+\}\s*(\.back-button:hover\s*\{[^}]+\}\s*)?(\.back-button::before\s*\{[^}]+\}\s*)?'
            if re.search(pattern2, content, re.DOTALL):
                content = re.sub(pattern2, '', content, count=1, flags=re.DOTALL)
            else:
                break
        
        # 패턴 3: 주석 없이 .back-button 블록만 있는 경우 제거
        while True:
            pattern3 = r'\.back-button\s*\{[^}]+\}\s*\.back-button:hover\s*\{[^}]+\}(\s*\.back-button::before\s*\{[^}]+\})?'
            if re.search(pattern3, content, re.DOTALL):
                # 이미 통일된 스타일과 같은지 확인
                match = re.search(pattern3, content, re.DOTALL)
                if match and 'border-radius: 50px' in match.group(0):
                    break  # 이미 올바른 스타일이면 중단
                content = re.sub(pattern3, '', content, count=1, flags=re.DOTALL)
            else:
                break
        
        # 새로운 통일 스타일을 /* ========== 콘텐츠 영역 ========== */ 바로 앞에 삽입
        insert_pattern = r'(/\* =+ 콘텐츠 영역 =+ \*/)'
        if re.search(insert_pattern, content):
            content = re.sub(insert_pattern, UNIFIED_BACK_BUTTON_CSS + '\n        \n        \\1', content, count=1)
        else:
            # 콘텐츠 영역 주석이 없으면 body 스타일 뒤에 삽입
            body_pattern = r'(body\s*\{[^}]+\})'
            if re.search(body_pattern, content, re.DOTALL):
                content = re.sub(body_pattern, '\\1\n        \n        ' + UNIFIED_BACK_BUTTON_CSS, content, count=1, flags=re.DOTALL)
        
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
    print("🎨 뒤로가기 버튼 스타일 통일 (흰색 둥근 버튼)")
    print("=" * 60)
    print(f"\n📝 총 {len(TARGET_FILES)}개 파일 처리 중...\n")
    
    updated_count = 0
    
    for filename in sorted(TARGET_FILES):
        if fix_back_button_unified(filename):
            print(f"  ✅ {filename}")
            updated_count += 1
        else:
            print(f"  ℹ️ {filename} - 변경사항 없음 또는 이미 적용됨")
    
    print(f"\n✅ 총 {updated_count}개 파일 수정 완료!")
    print("\n📋 적용된 통일 스타일:")
    print("   - 배경: 흰색")
    print("   - 색상: #667eea (보라색)")
    print("   - 모양: 둥근 버튼 (border-radius: 50px)")
    print("   - 그림자: 0 4px 15px rgba(0,0,0,0.1)")
    print("   - 헤더 간격: 30px (위)")
    print("   - 콘텐츠 간격: 30px (아래)")
    print("   - 호버 효과: 위로 2px 이동 + 그림자 증가")
    print("=" * 60)

if __name__ == "__main__":
    main()

