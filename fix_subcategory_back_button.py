import os
import re
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

print("=" * 70)
print("🔧 서브 카테고리 페이지 뒤로가기 버튼 수정")
print("=" * 70)

# 서브 카테고리 파일들 (food-, exercise-, lifestyle- 등)
subcategory_files = [
    'lifestyle-habits.html',
    'lifestyle-tips.html',
    'food-diet-guide.html',
    'food-avoid-fruits.html',
    'food-warnings.html',
    'exercise-guide.html',
    'exercise-tips.html',
]

# sub-diabetes.html의 .site-main CSS와 구조를 가져오기
with open('sub-diabetes.html', 'r', encoding='utf-8') as f:
    sub_content = f.read()

# .site-main CSS 추출
site_main_css = """.site-main {
            max-width: 1400px;
            margin: 0 auto;
            padding: 0 20px;
        }"""

print(f"\n📝 {len(subcategory_files)}개 서브 카테고리 파일 수정 중...\n")

fixed_count = 0

for filename in subcategory_files:
    if not os.path.exists(filename):
        print(f"⚠️  {filename} - 파일 없음")
        continue
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 1. .site-main CSS가 없으면 추가
        if '.site-main' not in content:
            # </style> 전에 추가
            content = content.replace('</style>', f'\n        {site_main_css}\n    </style>')
        
        # 2. HTML 구조 변경: health-card-container -> site-main
        # <div class="health-card-container">를 <div class="site-main">으로 변경
        content = re.sub(
            r'<div class="health-card-container">',
            '<div class="site-main">',
            content
        )
        
        # 3. container-content div 제거
        # <div class="container-content">와 그 닫는 태그 제거
        content = re.sub(
            r'<div class="container-content">\s*',
            '',
            content
        )
        
        # container-content의 닫는 태그 찾기 (뒤로가기와 section-title 사이)
        # 매우 조심스럽게 제거
        content = re.sub(
            r'</div>\s*<div class="section-title">',
            '<div class="section-title">',
            content,
            count=1
        )
        
        # 4. 불필요한 빈 줄 제거
        content = re.sub(r'\n\n\n+', '\n\n', content)
        
        # 변경사항이 있으면 저장
        if content != original_content:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ {filename}")
            fixed_count += 1
        else:
            print(f"ℹ️  {filename} - 변경 없음")
    
    except Exception as e:
        print(f"❌ {filename} - 오류: {e}")

print(f"\n✅ {fixed_count}개 파일 수정 완료!")

# 검증
print("\n" + "=" * 70)
print("🔍 lifestyle-habits.html 검증:")
print("=" * 70 + "\n")

if os.path.exists('lifestyle-habits.html'):
    with open('lifestyle-habits.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    has_site_main_css = '.site-main {' in content
    has_site_main_html = '<div class="site-main">' in content
    has_back_button = 'class="back-button"' in content
    no_container_content = 'class="container-content"' not in content
    
    print(f"✅ .site-main CSS: {has_site_main_css}")
    print(f"✅ <div class='site-main'>: {has_site_main_html}")
    print(f"✅ back-button class: {has_back_button}")
    print(f"✅ container-content 제거: {no_container_content}")
    
    if all([has_site_main_css, has_site_main_html, has_back_button, no_container_content]):
        print(f"\n🎉 lifestyle-habits.html 완벽!")
    else:
        print(f"\n⚠️  일부 문제 있음")

print("\n" + "=" * 70)
print("🎉 완료!")
print("=" * 70)

