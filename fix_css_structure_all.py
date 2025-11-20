import os
import re
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

print("=" * 70)
print("🔧 CSS 구조 수정 및 뒤로가기 버튼 완전 재적용")
print("=" * 70)

# 표준 뒤로가기 버튼 CSS
BACK_BUTTON_CSS = """        .back-button {
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
        }"""

# 모든 HTML 파일
all_files = [f for f in os.listdir('.') if f.endswith('.html') and not f.startswith('backup')]

print(f"\n📝 {len(all_files)}개 파일 처리 중...\n")

fixed_count = 0

for filename in all_files:
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 뒤로가기가 없는 파일은 스킵
        if '뒤로가기' not in content and 'back-button' not in content.lower():
            continue
        
        original_content = content
        
        # 1. </style> 태그가 있는지 확인
        if '</style>' not in content:
            print(f"❌ {filename} - </style> 태그 없음! 건너뜀")
            continue
        
        # 2. 모든 .back-button 관련 CSS 제거 (style 태그 안에서만)
        # <style>부터 </style>까지 추출
        style_pattern = r'<style>(.*?)</style>'
        style_matches = list(re.finditer(style_pattern, content, re.DOTALL))
        
        if not style_matches:
            print(f"⚠️  {filename} - <style> 태그 없음")
            continue
        
        # 마지막 style 태그에서 작업
        last_style_match = style_matches[-1]
        style_content = last_style_match.group(1)
        
        # back-button 관련 CSS 제거
        style_content = re.sub(r'\.back-button\s*\{[^}]*?\}', '', style_content, flags=re.DOTALL)
        style_content = re.sub(r'\.back-button:hover\s*\{[^}]*?\}', '', style_content, flags=re.DOTALL)
        style_content = re.sub(r'\.back-button::before\s*\{[^}]*?\}', '', style_content, flags=re.DOTALL)
        
        # 새로운 CSS 추가
        style_content = style_content.rstrip() + '\n\n' + BACK_BUTTON_CSS + '\n    '
        
        # 원본 컨텐츠의 style 태그 교체
        new_style_tag = f'<style>{style_content}</style>'
        content = content[:last_style_match.start()] + new_style_tag + content[last_style_match.end():]
        
        # 3. HTML에서 뒤로가기 링크에 class 확인
        back_link_pattern = r'<a([^>]*?)>뒤로가기</a>'
        matches = list(re.finditer(back_link_pattern, content))
        
        for match in matches:
            full_tag = match.group(0)
            attrs = match.group(1)
            
            if 'class="back-button"' not in full_tag and "class='back-button'" not in full_tag:
                if 'class=' in attrs:
                    # 기존 class에 추가
                    new_attrs = re.sub(r'class="([^"]*)"', r'class="\1 back-button"', attrs)
                    new_attrs = re.sub(r"class='([^']*)'", r"class='\1 back-button'", new_attrs)
                else:
                    # class 속성 추가
                    new_attrs = attrs + ' class="back-button"'
                
                new_tag = f'<a{new_attrs}>뒤로가기</a>'
                content = content.replace(full_tag, new_tag)
        
        # 변경사항이 있으면 저장
        if content != original_content:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ {filename}")
            fixed_count += 1
    
    except Exception as e:
        print(f"❌ {filename} - 오류: {e}")
        import traceback
        traceback.print_exc()

print(f"\n✅ {fixed_count}개 파일 수정 완료!")

# 검증
print("\n" + "=" * 70)
print("🔍 주요 파일 검증:")
print("=" * 70 + "\n")

test_files = ['lifestyle-habits.html', 'sub-diabetes.html', 'exercise-guide.html']

for filename in test_files:
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        
        has_style_tag = '<style>' in content and '</style>' in content
        has_back_css = '.back-button {' in content
        has_back_html = 'class="back-button"' in content
        
        print(f"{'✅' if (has_style_tag and has_back_css and has_back_html) else '❌'} {filename}")
        print(f"   Style 태그: {'✅' if has_style_tag else '❌'}")
        print(f"   CSS: {'✅' if has_back_css else '❌'}")
        print(f"   HTML class: {'✅' if has_back_html else '❌'}\n")

print("=" * 70)
print("🎉 완료!")
print("=" * 70)

