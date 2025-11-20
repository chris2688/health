import os
import re
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 수정할 파일 목록
ALL_FILES = [
    "category-심혈관질환.html",
    "category-당뇨병.html",
    "category-관절근골격계.html",
    "category-호르몬내분비.html",
    "category-정신건강신경계.html",
    "category-소화기질환.html",
    "category-안과치과기타.html",
    "food-main.html",
    "exercise-main.html",
    "lifestyle-main.html",
    "news-main.html",
]


def fix_back_button_css(filepath):
    """뒤로가기 버튼 CSS 확인 및 수정"""
    if not os.path.exists(filepath):
        return False, None
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # .back-button CSS가 제대로 있는지 확인
        if '.back-button' in content:
            # CSS가 있지만 적용이 안되는 경우, 스타일이 더 명확하게 적용되도록 수정
            # margin-top 추가하여 위치 조정
            if 'margin-top' not in content.split('.back-button')[1].split('}')[0]:
                content = re.sub(
                    r'(\.back-button\s*\{[^}]*?margin:\s*)([^;]+);',
                    r'\1\2;\n            margin-top: 20px;',
                    content,
                    flags=re.DOTALL
                )
        
        return content != original_content, content
        
    except Exception as e:
        print(f"  ❌ {filepath} - 오류: {e}")
        return False, None


def fix_news_main_structure(filepath):
    """news-main.html 구조 확인 및 수정"""
    if not os.path.exists(filepath):
        return False, None
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # </body>와 </html> 태그 확인
        if '</body>' not in content:
            # </body> 태그 추가
            if '</script>' in content:
                content = re.sub(
                    r'(</script>)',
                    r'\1\n</body>',
                    content,
                    count=1
                )
            else:
                content += '\n</body>'
        
        if '</html>' not in content:
            # </html> 태그 추가
            content += '\n</html>'
        
        return content != original_content, content
        
    except Exception as e:
        print(f"  ❌ {filepath} - 오류: {e}")
        return False, None


def main():
    """메인 실행"""
    print("=" * 60)
    print("🔧 남은 문제 수정")
    print("=" * 60)
    print("\n💡 수정 사항:")
    print("   1. 뒤로가기 버튼 CSS 확인")
    print("   2. news-main.html 구조 확인\n")
    
    print("📝 파일 수정 중...\n")
    
    fixed_count = 0
    
    for file in ALL_FILES:
        changed = False
        content = None
        
        # 뒤로가기 버튼 CSS (category 파일만)
        if file.startswith('category-'):
            css_changed, content = fix_back_button_css(file)
            if css_changed and content:
                changed = True
                with open(file, 'w', encoding='utf-8') as f:
                    f.write(content)
        
        # news-main.html 구조
        if file == 'news-main.html':
            if not content:
                with open(file, 'r', encoding='utf-8') as f:
                    content = f.read()
            
            news_changed, content = fix_news_main_structure(file)
            if news_changed and content:
                changed = True
                with open(file, 'w', encoding='utf-8') as f:
                    f.write(content)
        
        if changed:
            print(f"  ✅ {file} - 수정 완료")
            fixed_count += 1
        else:
            print(f"  ℹ️ {file} - 변경사항 없음")
    
    print(f"\n✅ 총 {fixed_count}개 파일 수정 완료!")
    print("=" * 60)


if __name__ == "__main__":
    main()

