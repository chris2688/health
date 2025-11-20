import os
import re
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

print("=" * 70)
print("🔧 모든 뒤로가기 버튼 완전 통일")
print("=" * 70)

# 표준 뒤로가기 버튼 CSS
STANDARD_CSS = """.back-button {
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

# 모든 HTML 파일 검사
html_files = []
for filename in os.listdir('.'):
    if filename.endswith('.html') and not filename.startswith('backup'):
        html_files.append(filename)

print(f"\n📝 {len(html_files)}개 HTML 파일 검사 중...\n")

fixed_count = 0
checked_count = 0

for filename in html_files:
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 뒤로가기 버튼이 있는지 확인
        if 'back-button' not in content.lower() and '뒤로가기' not in content:
            continue
        
        checked_count += 1
        original_content = content
        
        # 1. 기존 .back-button CSS를 모두 제거
        # 여러 패턴으로 제거 시도
        patterns_to_remove = [
            r'\.back-button\s*\{[^}]*?\}(?:\s*\.back-button:[^}]*?\{[^}]*?\})*(?:\s*\.back-button::[^}]*?\{[^}]*?\})*',
            r'\.back-button\s*\{[^}]*?\}',
        ]
        
        for pattern in patterns_to_remove:
            content = re.sub(pattern, '', content, flags=re.DOTALL)
        
        # 2. </style> 태그 바로 앞에 표준 CSS 삽입
        if '</style>' in content:
            # 마지막 </style> 찾기
            last_style_pos = content.rfind('</style>')
            if last_style_pos != -1:
                content = content[:last_style_pos] + '\n        ' + STANDARD_CSS + '\n    ' + content[last_style_pos:]
        
        # 3. HTML에서 뒤로가기 버튼 구조 확인 및 수정
        # class="back-button"이 있는지 확인
        back_button_patterns = [
            r'<a[^>]*?뒤로가기[^>]*?>.*?</a>',
            r'<button[^>]*?뒤로가기[^>]*?>.*?</button>',
        ]
        
        for pattern in back_button_patterns:
            matches = re.finditer(pattern, content, re.DOTALL | re.IGNORECASE)
            for match in matches:
                old_tag = match.group(0)
                # class="back-button"이 없으면 추가
                if 'class="back-button"' not in old_tag:
                    if '<a' in old_tag:
                        new_tag = re.sub(r'<a\s+', '<a class="back-button" ', old_tag)
                        if new_tag == old_tag:  # 공백이 없는 경우
                            new_tag = old_tag.replace('<a', '<a class="back-button"')
                        content = content.replace(old_tag, new_tag)
        
        # 변경사항이 있으면 저장
        if content != original_content:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ {filename}")
            fixed_count += 1
        else:
            print(f"ℹ️  {filename} - 이미 표준")
    
    except Exception as e:
        print(f"❌ {filename} - 오류: {e}")

print(f"\n" + "=" * 70)
print("📊 결과:")
print(f"   - 검사한 파일: {checked_count}개")
print(f"   - 수정한 파일: {fixed_count}개")
print("=" * 70)

# 특정 파일들 개별 확인
print("\n🔍 주요 페이지 개별 확인:\n")

important_files = [
    'exercise-guide.html',
    'exercise-main.html',
    'food-main.html',
    'lifestyle-main.html',
    'news-main.html',
    'category-cardiovascular.html',
    'category-diabetes.html',
]

for filename in important_files:
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        
        has_back = '뒤로가기' in content or 'back-button' in content
        has_css = '.back-button {' in content
        
        if has_back:
            print(f"   {'✅' if has_css else '❌'} {filename} - 뒤로가기: {has_back}, CSS: {has_css}")

print("\n" + "=" * 70)
print("🎉 완료!")
print("=" * 70)

