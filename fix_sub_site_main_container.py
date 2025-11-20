import os
import re
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# sub-*.html 파일 찾기
SUB_FILES = [f for f in os.listdir('.') if f.startswith('sub-') and f.endswith('.html')]

# .site-main 컨테이너 CSS
SITE_MAIN_CSS = '''        
        .site-main {
            max-width: 1400px;
            margin: 0 auto;
            padding: 0 20px;
        }'''

def fix_site_main_container(filepath):
    """sub 파일의 .site-main에 padding과 max-width 추가"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 기존 .site-main CSS가 있는지 확인
        site_main_pattern = r'\.site-main\s*\{[^}]+\}'
        
        if re.search(site_main_pattern, content, re.DOTALL):
            # 기존 CSS 업데이트
            content = re.sub(
                site_main_pattern,
                SITE_MAIN_CSS.strip(),
                content,
                flags=re.DOTALL
            )
        else:
            # 새로 추가 - .back-button 앞에 삽입
            back_button_pattern = r'(\.back-button\s*\{)'
            if re.search(back_button_pattern, content):
                content = re.sub(
                    back_button_pattern,
                    SITE_MAIN_CSS + '\n        \n        \\1',
                    content,
                    count=1
                )
        
        # .back-button의 margin-left를 0으로 변경 (이제 컨테이너 padding 사용)
        back_button_css_pattern = r'(\.back-button\s*\{[^}]*margin:\s*)30px 0 30px 20px;'
        if re.search(back_button_css_pattern, content, re.DOTALL):
            content = re.sub(
                back_button_css_pattern,
                r'\130px 0 30px 0;',
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
        return False

def main():
    """메인 실행"""
    print("=" * 60)
    print("🔧 sub 파일 컨테이너 padding 추가")
    print("=" * 60)
    print(f"\n📝 총 {len(SUB_FILES)}개 파일 처리 중...\n")
    
    updated_count = 0
    
    for filename in sorted(SUB_FILES):
        if fix_site_main_container(filename):
            print(f"  ✅ {filename}")
            updated_count += 1
        else:
            print(f"  ℹ️ {filename} - 변경사항 없음")
    
    print(f"\n✅ 총 {updated_count}개 파일 수정 완료!")
    print("\n📋 적용된 변경사항:")
    print("   - .site-main 컨테이너에 padding: 0 20px 추가")
    print("   - .site-main 컨테이너에 max-width: 1400px 추가")
    print("   - 뒤로가기 버튼이 컨테이너 padding 내에서 올바르게 표시")
    print("=" * 60)

if __name__ == "__main__":
    main()

