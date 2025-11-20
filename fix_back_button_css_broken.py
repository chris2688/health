import os
import re
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 모든 HTML 파일
ALL_HTML_FILES = [f for f in os.listdir('.') if f.endswith('.html')]

# 올바른 .back-button CSS
CORRECT_BACK_BUTTON_CSS = '''        .back-button {
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

def fix_broken_css(filepath):
    """깨진 .back-button CSS 수정"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if 'back-button' not in content and '뒤로가기' not in content:
            return False
        
        original_content = content
        
        # 패턴 1: 깨진 CSS (Xpx 0 30px 0; 같은 패턴)
        broken_pattern1 = r'Xpx 0 30px 0;\s*padding: 12px 24px;'
        if re.search(broken_pattern1, content):
            # 깨진 부분 전체를 올바른 CSS로 교체
            content = re.sub(
                r'Xpx 0 30px 0;\s*padding: 12px 24px;\s*background: white;\s*color: #667eea;\s*text-decoration: none;\s*border-radius: 50px;\s*font-weight: 600;\s*font-size: 16px;\s*box-shadow: [^;]+;\s*transition: all 0\.3s;\s*\}',
                CORRECT_BACK_BUTTON_CSS,
                content,
                flags=re.DOTALL
            )
        
        # 패턴 2: .back-button { 없이 속성만 있는 경우
        pattern2 = r'(\s+)(margin: 30px 0 30px 0;)\s*(padding: 12px 24px;)\s*(background: white;)'
        if re.search(pattern2, content) and '.back-button {' not in content[:content.find('margin: 30px 0 30px 0;') if 'margin: 30px 0 30px 0;' in content else 0]:
            # 앞에 .back-button { 추가
            content = re.sub(
                pattern2,
                r'\1.back-button {\n\1    display: inline-block;\n\1    \2\n\1    \3\n\1    \4',
                content
            )
        
        # 패턴 3: .site-main 바로 뒤에 잘못된 CSS가 있는 경우
        pattern3 = r'(\.site-main\s*\{[^}]+\})\s*Xpx 0 30px 0;'
        if re.search(pattern3, content, re.DOTALL):
            content = re.sub(
                pattern3,
                r'\1\n        \n' + CORRECT_BACK_BUTTON_CSS,
                content,
                flags=re.DOTALL
            )
        
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
    print("🔧 깨진 .back-button CSS 수정")
    print("=" * 60)
    
    # 뒤로가기 버튼이 있는 파일만 필터링
    target_files = []
    for f in ALL_HTML_FILES:
        try:
            with open(f, 'r', encoding='utf-8') as file:
                content = file.read()
                if '뒤로가기' in content or 'back-button' in content:
                    target_files.append(f)
        except:
            pass
    
    print(f"\n📝 총 {len(target_files)}개 파일 처리 중...\n")
    
    updated_count = 0
    
    for filename in sorted(target_files):
        if fix_broken_css(filename):
            print(f"  ✅ {filename}")
            updated_count += 1
        else:
            print(f"  ℹ️ {filename} - 변경사항 없음")
    
    print(f"\n✅ 총 {updated_count}개 파일 수정 완료!")
    print("\n📋 올바른 CSS 적용:")
    print("   - 배경: 흰색")
    print("   - 테두리: 둥근 모양 (border-radius: 50px)")
    print("   - 그림자: 0 4px 15px rgba(0,0,0,0.1)")
    print("   - 호버 효과: 위로 이동 + 그림자 증가")
    print("=" * 60)

if __name__ == "__main__":
    main()

