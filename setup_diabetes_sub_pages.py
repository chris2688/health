import sys
import io
import os

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

print("=" * 60)
print("🏥 당뇨병 서브 페이지 설정")
print("=" * 60)

# 서브 페이지 정의
sub_pages = [
    {
        'filename': 'sub-당뇨.html',
        'title': '당뇨',
        'icon': '💉',
        'category_slugs': ['당뇨', 'diabetes', '당뇨병'],
        'back_link': 'category-당뇨병.html'
    },
    {
        'filename': 'sub-공복혈당장애.html',
        'title': '공복혈당장애',
        'icon': '🩸',
        'category_slugs': ['공복혈당', '공복혈당장애', 'diabetes', '당뇨병'],
        'back_link': 'category-당뇨병.html'
    },
    {
        'filename': 'sub-당뇨병합병증.html',
        'title': '당뇨병 합병증',
        'icon': '⚕️',
        'category_slugs': ['당뇨병합병증', '당뇨합병증', 'diabetes', '당뇨병'],
        'back_link': 'category-당뇨병.html'
    }
]

# sub-고혈압.html을 템플릿으로 사용
if not os.path.exists('sub-고혈압.html'):
    print("❌ 템플릿 파일 sub-고혈압.html을 찾을 수 없습니다.")
    exit(1)

with open('sub-고혈압.html', 'r', encoding='utf-8') as f:
    template = f.read()

created_count = 0

for page in sub_pages:
    print(f"\n📝 {page['filename']} 생성 중...")
    
    content = template
    
    # 제목 변경
    content = content.replace('<title>고혈압 - 9988 건강정보</title>',
                             f'<title>{page["title"]} - 9988 건강정보</title>')
    
    # 페이지 타이틀 변경
    content = content.replace('<h1 class="page-title">고혈압</h1>',
                             f'<h1 class="page-title">{page["title"]}</h1>')
    
    # 뒤로가기 링크 변경
    content = content.replace('href="category-심혈관질환.html"',
                             f'href="{page["back_link"]}"')
    
    # pageToCategory 매핑 업데이트
    # 기존 매핑에 추가
    old_mapping_line = "'sub-고혈압.html': ['고혈압', 'cardiovascular', '심혈관-질환'],"
    new_mapping_line = f"'{page['filename']}': {page['category_slugs']},"
    
    # 매핑이 이미 있으면 업데이트, 없으면 추가
    if f"'{page['filename']}'" in content:
        # 기존 매핑 업데이트
        import re
        pattern = f"'{page['filename']}':\\s*\\[[^\\]]+\\],"
        content = re.sub(pattern, new_mapping_line, content)
    else:
        # 새 매핑 추가 (고혈압 매핑 다음에)
        content = content.replace(old_mapping_line,
                                 old_mapping_line + "\n                " + new_mapping_line)
    
    # 파일 저장
    with open(page['filename'], 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"   ✅ {page['filename']} 생성 완료")
    print(f"      - 제목: {page['title']}")
    print(f"      - 매핑: {page['category_slugs']}")
    created_count += 1

print(f"\n✅ 총 {created_count}개 서브 페이지 생성 완료!")
print("\n📋 생성된 페이지:")
for page in sub_pages:
    print(f"   {page['icon']} {page['title']} → {page['filename']}")
print("=" * 60)

