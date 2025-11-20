import sys
import io
import os
import re

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

print("=" * 70)
print("🏥 전체 카테고리 및 서브 페이지 생성")
print("=" * 70)

# 전체 카테고리 정의
ALL_CATEGORIES = {
    '관절근골격계': {
        'title': '관절/근골격계 질환',
        'icon': '🦴',
        'color1': '#FA709A',
        'color2': '#FEE140',
        'filename': 'category-관절근골격계.html',
        'sub_categories': [
            {'name': '퇴행성관절염', 'title': '퇴행성 관절염', 'icon': '🦵', 'slugs': ['퇴행성관절염', 'musculoskeletal', '관절-근골격계-질환']},
            {'name': '허리디스크목디스크', 'title': '허리디스크/목디스크', 'icon': '🦴', 'slugs': ['허리디스크', '목디스크', 'musculoskeletal', '관절-근골격계-질환']},
            {'name': '골다공증', 'title': '골다공증', 'icon': '🦴', 'slugs': ['골다공증', 'musculoskeletal', '관절-근골격계-질환']},
            {'name': '오십견', 'title': '오십견<br>(유착성 관절낭염)', 'icon': '💪', 'slugs': ['오십견', 'musculoskeletal', '관절-근골격계-질환']},
        ]
    },
    '소화기질환': {
        'title': '소화기 질환',
        'icon': '🫁',
        'color1': '#FFB84D',
        'color2': '#F77737',
        'filename': 'category-소화기질환.html',
        'sub_categories': [
            {'name': '위염위궤양', 'title': '위염/위궤양', 'icon': '🩺', 'slugs': ['위염', '위궤양', 'digestive', '소화기-질환']},
            {'name': '역류성식도염', 'title': '역류성 식도염', 'icon': '🔥', 'slugs': ['역류성식도염', 'digestive', '소화기-질환']},
            {'name': '과민성대장증후군', 'title': '과민성 대장증후군', 'icon': '💊', 'slugs': ['과민성대장증후군', 'digestive', '소화기-질환']},
            {'name': '지방간', 'title': '지방간/간기능 저하', 'icon': '🫘', 'slugs': ['지방간', 'digestive', '소화기-질환']},
        ]
    },
    '호르몬내분비': {
        'title': '호르몬/내분비 질환',
        'icon': '⚗️',
        'color1': '#A18CD1',
        'color2': '#FBC2EB',
        'filename': 'category-호르몬내분비.html',
        'sub_categories': [
            {'name': '갑상선', 'title': '갑상선 기능 저하/항진', 'icon': '🦋', 'slugs': ['갑상선', 'endocrine', '호르몬-내분비-질환']},
            {'name': '갱년기증후군', 'title': '갱년기 증후군', 'icon': '🌡️', 'slugs': ['갱년기', '갱년기증후군', 'endocrine', '호르몬-내분비-질환']},
            {'name': '대사증후군', 'title': '대사증후군', 'icon': '⚖️', 'slugs': ['대사증후군', 'endocrine', '호르몬-내분비-질환']},
        ]
    },
    '정신건강신경계': {
        'title': '정신건강/신경계',
        'icon': '🧠',
        'color1': '#667eea',
        'color2': '#764ba2',
        'filename': 'category-정신건강신경계.html',
        'sub_categories': [
            {'name': '우울증번아웃', 'title': '우울증/번아웃 증후군', 'icon': '💭', 'slugs': ['우울증', '번아웃', 'neuroscience', '정신-건강-신경계']},
            {'name': '수면장애불면증', 'title': '수면장애/불면증', 'icon': '😴', 'slugs': ['수면장애', '불면증', 'neuroscience', '정신-건강-신경계']},
            {'name': '치매경도인지장애', 'title': '치매/경도인지장애', 'icon': '🧩', 'slugs': ['치매', '인지장애', 'neuroscience', '정신-건강-신경계']},
            {'name': '이명어지럼증', 'title': '이명/어지럼증', 'icon': '👂', 'slugs': ['이명', '어지럼증', 'neuroscience', '정신-건강-신경계']},
        ]
    },
    '안과치과기타': {
        'title': '안과/치과/기타',
        'icon': '👁️',
        'color1': '#FF6B6B',
        'color2': '#EE5A6F',
        'filename': 'category-안과치과기타.html',
        'sub_categories': [
            {'name': '백내장녹내장', 'title': '백내장/녹내장', 'icon': '👁️', 'slugs': ['백내장', '녹내장', 'eyes-dental', '안과-치과-기타']},
            {'name': '치주염치아손실', 'title': '치주염/치아손실', 'icon': '🦷', 'slugs': ['치주염', '치아손실', 'eyes-dental', '안과-치과-기타']},
            {'name': '비만체형변화', 'title': '비만/체형 변화', 'icon': '⚖️', 'slugs': ['비만', '체형변화', 'eyes-dental', '안과-치과-기타']},
        ]
    }
}

# 템플릿 파일 로드
if not os.path.exists('category-심혈관질환.html'):
    print("❌ 템플릿 파일을 찾을 수 없습니다.")
    exit(1)

with open('category-심혈관질환.html', 'r', encoding='utf-8') as f:
    category_template = f.read()

if not os.path.exists('sub-고혈압.html'):
    print("❌ 서브 페이지 템플릿을 찾을 수 없습니다.")
    exit(1)

with open('sub-고혈압.html', 'r', encoding='utf-8') as f:
    sub_template = f.read()

# 카테고리 파일 생성
print("\n📂 카테고리 페이지 생성 중...\n")
category_count = 0

for cat_key, cat_data in ALL_CATEGORIES.items():
    print(f"   {cat_data['icon']} {cat_data['title']} ({cat_data['filename']})")
    
    content = category_template
    
    # 제목 변경
    content = content.replace('<title>심혈관 질환 - 9988 건강정보</title>',
                             f'<title>{cat_data["title"]} - 9988 건강정보</title>')
    
    # 아이콘과 제목 변경
    content = content.replace('<div class="main-icon">❤️</div>',
                             f'<div class="main-icon">{cat_data["icon"]}</div>')
    content = content.replace('<h2>심혈관 질환</h2>',
                             f'<h2>{cat_data["title"]}</h2>')
    
    # 서브 카테고리 카드 생성
    cards_html = []
    colors = [
        ('FF6B6B', 'EE5A6F'),
        ('4ECDC4', '44A08D'),
        ('A18CD1', 'FBC2EB'),
        ('FA709A', 'FEE140'),
        ('667eea', '764ba2'),
        ('FFB84D', 'F77737'),
    ]
    
    for i, sub in enumerate(cat_data['sub_categories']):
        color1, color2 = colors[i % len(colors)]
        card = f'''<a href="sub-{sub['name']}.html" class="health-card" style="--card-color-1:#{color1}; --card-color-2:#{color2};">
                    <div class="health-card-icon">{sub['icon']}</div>
                    <h3>{sub['title']}</h3>
                </a>'''
        cards_html.append(card)
    
    # 기존 카드 교체
    old_cards_pattern = r'<a href="sub-고혈압\.html".*?</a>(\s*<a href="sub-.*?</a>)*'
    new_cards = '\n                \n                '.join(cards_html)
    content = re.sub(old_cards_pattern, new_cards, content, flags=re.DOTALL)
    
    # 파일 저장
    with open(cat_data['filename'], 'w', encoding='utf-8') as f:
        f.write(content)
    
    category_count += 1

print(f"\n✅ {category_count}개 카테고리 페이지 생성 완료!\n")

# 서브 페이지 생성
print("📄 서브 페이지 생성 중...\n")
sub_count = 0

for cat_key, cat_data in ALL_CATEGORIES.items():
    for sub in cat_data['sub_categories']:
        filename = f"sub-{sub['name']}.html"
        print(f"   {sub['icon']} {sub['title']} ({filename})")
        
        content = sub_template
        
        # 제목 변경
        clean_title = sub['title'].replace('<br>', ' ')
        content = content.replace('<title>고혈압 - 9988 건강정보</title>',
                                 f'<title>{clean_title} - 9988 건강정보</title>')
        
        # 페이지 타이틀 변경
        content = content.replace('<h1 class="page-title">고혈압</h1>',
                                 f'<h1 class="page-title">{clean_title}</h1>')
        
        # 뒤로가기 링크 변경
        content = content.replace('href="category-심혈관질환.html"',
                                 f'href="{cat_data["filename"]}"')
        
        # pageToCategory 매핑 추가
        mapping_line = f"'{filename}': {sub['slugs']},"
        
        # 매핑이 이미 있으면 업데이트, 없으면 추가
        if f"'{filename}'" in content:
            pattern = f"'{filename}':\\s*\\[[^\\]]+\\],"
            content = re.sub(pattern, mapping_line, content)
        else:
            # 고혈압 매핑 다음에 추가
            old_line = "'sub-고혈압.html': ['고혈압', 'cardiovascular', '심혈관-질환'],"
            content = content.replace(old_line, old_line + "\n                " + mapping_line)
        
        # 파일 저장
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        
        sub_count += 1

print(f"\n✅ 총 {sub_count}개 서브 페이지 생성 완료!")
print("\n" + "=" * 70)
print("🎉 전체 카테고리 및 서브 페이지 생성 완료!")
print("=" * 70)
print(f"\n📊 생성 요약:")
print(f"   - 카테고리 페이지: {category_count}개")
print(f"   - 서브 페이지: {sub_count}개")
print(f"   - 총: {category_count + sub_count}개 파일")
print("\n📋 생성된 카테고리:")
for cat_key, cat_data in ALL_CATEGORIES.items():
    print(f"\n   {cat_data['icon']} {cat_data['title']}")
    for sub in cat_data['sub_categories']:
        print(f"      └─ {sub['icon']} {sub['title'].replace('<br>', ' ')}")
print("=" * 70)

