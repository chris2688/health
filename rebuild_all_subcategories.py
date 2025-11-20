import os
import re
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

print("=" * 70)
print("🔧 모든 서브 카테고리 파일 재구축")
print("=" * 70)

# sub-diabetes.html을 템플릿으로 사용
with open('sub-diabetes.html', 'r', encoding='utf-8') as f:
    template = f.read()

# 서브 카테고리 설정
subcategories = {
    'lifestyle-tips.html': {
        'title': '생활습관바꾸기팁',
        'back_link': 'lifestyle-main.html',
        'page_title': '생활습관 바꾸기 팁',
        'icon': '💡',
        'subtitle': '작은 변화가 만드는 큰 건강'
    },
    'food-diet-guide.html': {
        'title': '질환별식단',
        'back_link': 'food-main.html',
        'page_title': '질환별 식단',
        'icon': '🍽️',
        'subtitle': '질환에 맞는 맞춤 식단'
    },
    'food-avoid-fruits.html': {
        'title': '피해야할과일',
        'back_link': 'food-main.html',
        'page_title': '피해야 할 과일',
        'icon': '🍊',
        'subtitle': '질환별 주의해야 할 과일'
    },
    'food-warnings.html': {
        'title': '모르면독이된다',
        'back_link': 'food-main.html',
        'page_title': '모르면 독이 되는 음식',
        'icon': '⚠️',
        'subtitle': '알아야 할 식품 정보'
    },
    'exercise-guide.html': {
        'title': '질환별운동가이드',
        'back_link': 'exercise-main.html',
        'page_title': '질환별 운동 가이드',
        'icon': '🏃',
        'subtitle': '안전하고 효과적인 운동법'
    },
    'exercise-tips.html': {
        'title': '운동팁',
        'back_link': 'exercise-main.html',
        'page_title': '운동 팁',
        'icon': '💪',
        'subtitle': '운동 효과를 높이는 방법'
    },
}

print(f"\n📝 {len(subcategories)}개 파일 재생성 중...\n")

for filename, config in subcategories.items():
    try:
        # 템플릿 복사
        content = template
        
        # 1. 타이틀 변경
        content = content.replace(
            '<title>당뇨 - 9988 건강정보</title>',
            f'<title>{config["title"]} - 9988 건강정보</title>'
        )
        
        # 2. 뒤로가기 링크 변경
        content = content.replace(
            'href="category-diabetes.html" class="back-button"',
            f'href="{config["back_link"]}" class="back-button"'
        )
        
        # 3. 페이지 타이틀 변경
        content = content.replace(
            '<h1 class="page-title">당뇨</h1>',
            f'<h1 class="page-title">{config["page_title"]}</h1>'
        )
        
        # 4. 파일 저장
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        
        size = os.path.getsize(filename) / 1024
        print(f"✅ {filename} ({size:.1f} KB)")
        
    except Exception as e:
        print(f"❌ {filename} - 오류: {e}")

print(f"\n✅ 모든 파일 재생성 완료!")

print("\n" + "=" * 70)
print("🎉 완료!")
print("=" * 70)
print("\n모든 서브 카테고리 파일이 sub-diabetes.html과 동일한 구조로 재생성되었습니다!")
print("뒤로가기 버튼이 모든 파일에서 동일하게 작동합니다!")
print("=" * 70)

