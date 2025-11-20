import os
import re
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

print("=" * 70)
print("🧹 모든 HTML 파일 정리 및 뒤로가기 버튼 수정")
print("=" * 70)

# sub-diabetes.html에서 템플릿 가져오기
with open('sub-diabetes.html', 'r', encoding='utf-8') as f:
    template = f.read()

# 정확한 .back-button CSS 추출
back_css_match = re.search(
    r'(\.back-button \{[^}]+\}\s+\.back-button:hover \{[^}]+\}\s+\.back-button::before \{[^}]+\})',
    template,
    re.DOTALL
)

if not back_css_match:
    print("❌ CSS를 찾을 수 없습니다!")
    exit(1)

EXACT_BACK_CSS = back_css_match.group(1).strip()

print("\n✅ 추출한 CSS:")
print("-" * 70)
print(EXACT_BACK_CSS)
print("-" * 70)

# 모든 HTML 파일
all_files = [f for f in os.listdir('.') if f.endswith('.html') and not f.startswith('backup') and f != 'sub-diabetes.html']

print(f"\n📝 {len(all_files)}개 파일 처리 중...\n")

fixed_count = 0

for filename in all_files:
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 뒤로가기가 없는 파일은 스킵
        if '뒤로가기' not in content:
            continue
        
        original_content = content
        
        # 1. 불필요한 빈 줄 제거 (연속된 빈 줄을 하나로)
        content = re.sub(r'\n\n\n+', '\n\n', content)
        
        # 2. 모든 .back-button 관련 CSS 제거
        content = re.sub(r'\.back-button\s*\{[^}]*?\}', '', content, flags=re.DOTALL)
        content = re.sub(r'\.back-button:hover\s*\{[^}]*?\}', '', content, flags=re.DOTALL)
        content = re.sub(r'\.back-button::before\s*\{[^}]*?\}', '', content, flags=re.DOTALL)
        
        # 3. </style> 전에 정확한 CSS 추가
        if '</style>' in content:
            content = content.replace('</style>', f'\n\n        {EXACT_BACK_CSS}\n    </style>')
        
        # 4. 뒤로가기 HTML에 class 확인
        back_pattern = r'<a\s+([^>]*?)>뒤로가기</a>'
        for match in re.finditer(back_pattern, content):
            full_tag = match.group(0)
            attrs = match.group(1)
            
            # class="back-button"이 없으면 추가
            if 'class="back-button"' not in full_tag:
                if 'href=' in attrs and 'class=' not in attrs:
                    # href는 있지만 class가 없음
                    new_tag = full_tag.replace('href=', 'class="back-button" href=')
                    content = content.replace(full_tag, new_tag, 1)
                elif 'class=' in attrs:
                    # class가 있으면 추가
                    new_attrs = re.sub(r'class="([^"]*)"', r'class="\1 back-button"', attrs)
                    new_tag = f'<a {new_attrs}>뒤로가기</a>'
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

# 상세 검증
print("\n" + "=" * 70)
print("🔍 lifestyle-habits.html 상세 검증:")
print("=" * 70 + "\n")

if os.path.exists('lifestyle-habits.html'):
    with open('lifestyle-habits.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # CSS 확인
    has_back_button = '.back-button {' in content
    has_hover = '.back-button:hover' in content
    has_before = '.back-button::before' in content
    
    # HTML 확인
    has_class = 'class="back-button"' in content
    has_text = '뒤로가기' in content
    
    print(f"CSS:")
    print(f"  ✅ .back-button: {has_back_button}")
    print(f"  ✅ :hover: {has_hover}")
    print(f"  ✅ ::before: {has_before}")
    print(f"\nHTML:")
    print(f"  ✅ class='back-button': {has_class}")
    print(f"  ✅ 뒤로가기 텍스트: {has_text}")
    
    if all([has_back_button, has_hover, has_before, has_class, has_text]):
        print(f"\n🎉 lifestyle-habits.html 완벽!")
    else:
        print(f"\n⚠️  문제가 있습니다!")
        
        # 뒤로가기 관련 부분 출력
        back_match = re.search(r'<a[^>]*?뒤로가기[^>]*?>', content)
        if back_match:
            print(f"\n현재 HTML: {back_match.group(0)}")

print("\n" + "=" * 70)
print("🎉 완료!")
print("=" * 70)

