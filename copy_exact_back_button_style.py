import os
import re
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

print("=" * 70)
print("🔧 sub-diabetes.html의 정확한 뒤로가기 스타일 복사")
print("=" * 70)

# sub-diabetes.html에서 정확한 CSS 추출
with open('sub-diabetes.html', 'r', encoding='utf-8') as f:
    sub_content = f.read()

# sub-diabetes.html의 정확한 .back-button CSS 추출
back_button_css_match = re.search(
    r'(\.back-button \{.*?\.back-button::before \{.*?\})',
    sub_content,
    re.DOTALL
)

if not back_button_css_match:
    print("❌ sub-diabetes.html에서 .back-button CSS를 찾을 수 없습니다!")
    exit(1)

EXACT_CSS = back_button_css_match.group(1)

print("\n✅ sub-diabetes.html에서 추출한 CSS:")
print("-" * 70)
print(EXACT_CSS[:200] + "...")
print("-" * 70)

# 모든 HTML 파일 처리
all_files = [f for f in os.listdir('.') if f.endswith('.html') and not f.startswith('backup') and f != 'sub-diabetes.html']

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
        
        # </style> 태그 찾기
        if '</style>' not in content:
            print(f"⚠️  {filename} - </style> 태그 없음, 건너뜀")
            continue
        
        # 기존 모든 .back-button 관련 CSS 제거
        content = re.sub(r'\.back-button\s*\{[^}]*?\}', '', content, flags=re.DOTALL)
        content = re.sub(r'\.back-button:hover\s*\{[^}]*?\}', '', content, flags=re.DOTALL)
        content = re.sub(r'\.back-button::before\s*\{[^}]*?\}', '', content, flags=re.DOTALL)
        
        # 마지막 </style> 바로 전에 정확한 CSS 삽입
        last_style_pos = content.rfind('</style>')
        if last_style_pos != -1:
            # 들여쓰기 맞추기
            indent = '        '
            formatted_css = '\n' + indent + EXACT_CSS.replace('\n', '\n' + indent) + '\n    '
            content = content[:last_style_pos] + formatted_css + content[last_style_pos:]
        
        # HTML에서 뒤로가기 링크에 class="back-button" 확인
        back_pattern = r'<a([^>]*?)>뒤로가기</a>'
        for match in re.finditer(back_pattern, content):
            full_tag = match.group(0)
            attrs = match.group(1)
            
            if 'class="back-button"' not in full_tag:
                if 'class=' in attrs:
                    new_attrs = re.sub(r'class="([^"]*)"', r'class="\1 back-button"', attrs)
                else:
                    new_attrs = attrs + ' class="back-button"'
                
                new_tag = f'<a{new_attrs}>뒤로가기</a>'
                content = content.replace(full_tag, new_tag, 1)
        
        # 변경사항이 있으면 저장
        if content != original_content:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ {filename}")
            fixed_count += 1
    
    except Exception as e:
        print(f"❌ {filename} - 오류: {e}")

print(f"\n✅ {fixed_count}개 파일 수정 완료!")

# 검증
print("\n" + "=" * 70)
print("🔍 검증: lifestyle-habits.html")
print("=" * 70)

if os.path.exists('lifestyle-habits.html'):
    with open('lifestyle-habits.html', 'r', encoding='utf-8') as f:
        test_content = f.read()
    
    has_css = '.back-button {' in test_content
    has_hover = '.back-button:hover' in test_content
    has_before = '.back-button::before' in test_content
    has_class = 'class="back-button"' in test_content
    
    print(f"✅ CSS 존재: {has_css}")
    print(f"✅ :hover 존재: {has_hover}")
    print(f"✅ ::before 존재: {has_before}")
    print(f"✅ HTML class 존재: {has_class}")
    
    if has_css and has_hover and has_before and has_class:
        print("\n🎉 lifestyle-habits.html 완벽!")
    else:
        print("\n⚠️  일부 요소 누락")

print("\n" + "=" * 70)
print("🎉 완료!")
print("=" * 70)

