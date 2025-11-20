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

# 새로운 뒤로가기 버튼 CSS 스타일
NEW_BACK_BUTTON_CSS = '''        /* ========== 뒤로가기 버튼 ========== */
        .back-button {
            display: inline-block;
            margin: 30px 0 20px 0;
            margin-left: max(20px, calc((100% - 1400px) / 2 + 20px));
            padding: 10px 20px;
            color: #667eea;
            text-decoration: none;
            font-weight: 500;
            font-size: 16px;
            transition: all 0.3s;
        }
        
        .back-button:hover {
            color: #764ba2;
            transform: translateX(-3px);
        }
        
        .back-button::before {
            content: '← ';
            font-weight: bold;
        }'''

def fix_back_button_style(filepath):
    """뒤로가기 버튼 스타일 통일"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 기존 뒤로가기 버튼 CSS 찾기 및 교체
        # 패턴 1: /* ========== 뒤로가기 버튼 (헤더 밖) ========== */ 부터 다음 섹션까지
        pattern1 = r'/\* =+ 뒤로가기 버튼 \(헤더 밖\) =+ \*/\s*\n\s*\n\s*\n\s*\n\s*\n\s*\n\s*\n\s*\n\s*\n\s*\n'
        if re.search(pattern1, content):
            content = re.sub(pattern1, '', content)
        
        # 패턴 2: 기존 뒤로가기 버튼 CSS 블록 전체
        pattern2 = r'/\* =+ 뒤로가기 버튼 =+ \*/\s*\.back-button\s*\{[^}]+\}\s*\.back-button:hover\s*\{[^}]+\}\s*\.back-button::before\s*\{[^}]+\}'
        
        if re.search(pattern2, content, re.DOTALL):
            content = re.sub(pattern2, NEW_BACK_BUTTON_CSS, content, flags=re.DOTALL)
        else:
            # 패턴이 없으면 /* ========== 콘텐츠 영역 ========== */ 앞에 삽입
            insert_pattern = r'(/\* =+ 콘텐츠 영역 =+ \*/)'
            if re.search(insert_pattern, content):
                content = re.sub(insert_pattern, NEW_BACK_BUTTON_CSS + '\n        \n        \\1', content)
        
        # HTML에서 뒤로가기 버튼이 <header class="page-header"> 앞에 있는지 확인
        # 있으면 위치 조정 (margin-top 증가로 간격 확보)
        
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
    print("🎨 뒤로가기 버튼 스타일 통일")
    print("=" * 60)
    print(f"\n📝 총 {len(TARGET_FILES)}개 파일 처리 중...\n")
    
    updated_count = 0
    
    for filename in sorted(TARGET_FILES):
        if fix_back_button_style(filename):
            print(f"  ✅ {filename}")
            updated_count += 1
        else:
            print(f"  ℹ️ {filename} - 변경사항 없음")
    
    print(f"\n✅ 총 {updated_count}개 파일 수정 완료!")
    print("\n📋 적용된 스타일:")
    print("   - 헤더와의 간격: 30px (위쪽)")
    print("   - 콘텐츠와의 간격: 20px (아래쪽)")
    print("   - 색상: #667eea → #764ba2 (hover)")
    print("   - 효과: 호버 시 왼쪽으로 3px 이동")
    print("=" * 60)

if __name__ == "__main__":
    main()

