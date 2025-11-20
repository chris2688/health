import os
import re
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

print("=" * 70)
print("🔧 뒤로가기 버튼 최종 통일 (두 번째 캡처 스타일)")
print("=" * 70)

# 두 번째 캡처의 정확한 스타일
FINAL_BACK_BUTTON_CSS = """
        .back-button {
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
        }
"""

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
        
        # 1. 기존 모든 .back-button 관련 CSS 제거
        # 다양한 패턴으로 제거
        patterns = [
            r'\.back-button\s*\{[^}]*?\}(?:\s*\.back-button:[^}]*?\{[^}]*?\})*(?:\s*\.back-button::[^}]*?\{[^}]*?\})*',
            r'\.back-button\s*\{[^}]*?\}',
            r'\.back-button:hover\s*\{[^}]*?\}',
            r'\.back-button::before\s*\{[^}]*?\}',
        ]
        
        for pattern in patterns:
            content = re.sub(pattern, '', content, flags=re.DOTALL)
        
        # 2. 마지막 </style> 앞에 새로운 CSS 삽입
        last_style_close = content.rfind('</style>')
        if last_style_close != -1:
            content = content[:last_style_close] + FINAL_BACK_BUTTON_CSS + '\n    ' + content[last_style_close:]
        
        # 3. HTML에서 뒤로가기 버튼에 class 확인 및 추가
        # <a> 태그에 "뒤로가기" 있으면 class="back-button" 확인
        back_link_pattern = r'<a([^>]*?)뒤로가기([^>]*?)>(.*?)</a>'
        matches = list(re.finditer(back_link_pattern, content, re.DOTALL))
        
        for match in matches:
            full_tag = match.group(0)
            if 'class="back-button"' not in full_tag and "class='back-button'" not in full_tag:
                # class 속성 추가
                if 'class=' in full_tag:
                    # 이미 class가 있으면 back-button 추가
                    new_tag = re.sub(r'class="([^"]*)"', r'class="\1 back-button"', full_tag)
                    new_tag = re.sub(r"class='([^']*)'", r"class='\1 back-button'", new_tag)
                else:
                    # class 속성이 없으면 새로 추가
                    new_tag = full_tag.replace('<a', '<a class="back-button"', 1)
                
                content = content.replace(full_tag, new_tag)
        
        # 변경사항이 있으면 저장
        if content != original_content:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ {filename}")
            fixed_count += 1
        else:
            if '뒤로가기' in original_content:
                print(f"ℹ️  {filename} - 이미 최신")
    
    except Exception as e:
        print(f"❌ {filename} - 오류: {e}")

print(f"\n✅ {fixed_count}개 파일 수정 완료!")

# 주요 파일 검증
print("\n" + "=" * 70)
print("🔍 주요 파일 검증:")
print("=" * 70 + "\n")

test_files = [
    'lifestyle-habits.html',
    'sub-diabetes.html',
    'category-cardiovascular.html',
    'food-main.html',
    'exercise-guide.html',
    'news-main.html',
]

for filename in test_files:
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        
        has_back = '뒤로가기' in content
        has_css = '.back-button {' in content
        has_class = 'class="back-button"' in content
        
        status = "✅" if (has_back and has_css and has_class) else "⚠️"
        print(f"{status} {filename}")
        if has_back and not has_class:
            print(f"   ⚠️  CSS는 있지만 HTML class가 없습니다!")

print("\n" + "=" * 70)
print("🎉 완료! 모든 뒤로가기 버튼이 통일되었습니다!")
print("=" * 70)
print("\n스타일:")
print("  - 흰색 배경 (white)")
print("  - 보라색 텍스트 (#667eea)")
print("  - 둥근 모서리 (50px)")
print("  - 그림자 효과")
print("  - 호버 시 위로 이동")
print("  - '← ' 화살표 자동 추가")
print("=" * 70)

