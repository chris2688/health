import os
import re
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

print("=" * 70)
print("🔧 모든 페이지에 뒤로가기 버튼 적용")
print("=" * 70)

# sub-diabetes.html에서 정확한 CSS 추출
with open('sub-diabetes.html', 'r', encoding='utf-8') as f:
    template = f.read()

# .back-button CSS 추출
back_button_css = """.back-button {
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

# 제외할 파일들
exclude_files = [
    'index-v3.html',
    'index-v2.html',
    'intro.html',
    'verify_lifestyle_habits.html',
    'index.html',
    'homepage_code.html',
    '메인페이지_완성코드.html',
    'post-detail.html',
]

# 뒤로가기가 있어야 하는 파일들
files_to_process = [f for f in all_files if f not in exclude_files]

print(f"\n📝 {len(files_to_process)}개 파일 처리 중...\n")

fixed_count = 0

for filename in files_to_process:
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 뒤로가기가 없는 파일은 스킵 (main 페이지 등)
        if '뒤로가기' not in content:
            continue
        
        original_content = content
        
        # 1. 모든 기존 .back-button CSS 제거
        content = re.sub(r'\.back-button\s*\{[^}]*?\}', '', content, flags=re.DOTALL)
        content = re.sub(r'\.back-button:hover\s*\{[^}]*?\}', '', content, flags=re.DOTALL)
        content = re.sub(r'\.back-button::before\s*\{[^}]*?\}', '', content, flags=re.DOTALL)
        
        # 2. 마지막 </style> 전에 정확한 CSS 추가
        if '</style>' in content:
            last_style_pos = content.rfind('</style>')
            if last_style_pos != -1:
                content = content[:last_style_pos] + '\n\n        ' + back_button_css + '\n    ' + content[last_style_pos:]
        
        # 3. HTML에서 뒤로가기 버튼에 class 확인
        # <a href="..." class="back-button">뒤로가기</a> 형식인지 확인
        back_pattern = r'<a\s+([^>]*?)>뒤로가기</a>'
        for match in re.finditer(back_pattern, content):
            full_tag = match.group(0)
            attrs = match.group(1)
            
            # class="back-button"이 없으면 추가
            if 'class="back-button"' not in full_tag and "class='back-button'" not in full_tag:
                if 'href=' in attrs:
                    # href 속성 뒤에 class 추가
                    if 'class=' not in attrs:
                        new_attrs = re.sub(r'(href="[^"]*")', r'\1 class="back-button"', attrs)
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

# 주요 파일 검증
print("\n" + "=" * 70)
print("🔍 주요 파일 검증:")
print("=" * 70 + "\n")

test_files = [
    'category-cardiovascular.html',
    'category-diabetes.html',
    'exercise-main.html',
    'food-main.html',
    'lifestyle-main.html',
    'news-main.html',
]

for filename in test_files:
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        
        has_back = '뒤로가기' in content
        has_css = '.back-button {' in content
        has_class = 'class="back-button"' in content
        
        if has_back:
            status = "✅" if (has_css and has_class) else "⚠️"
            print(f"{status} {filename} - CSS: {has_css}, HTML: {has_class}")
        else:
            print(f"ℹ️  {filename} - 뒤로가기 없음 (정상)")

print("\n" + "=" * 70)
print("🎉 완료!")
print("=" * 70)
print("\n모든 페이지에 sub-diabetes.html과 동일한 뒤로가기 버튼이 적용되었습니다!")
print("=" * 70)

