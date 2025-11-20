import os
import sys
import io

# UTF-8 인코딩 설정
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 페이지 템플릿 불러오기
from page_template import STANDARD_PAGE_TEMPLATE, STANDARD_FOOTER

# 생활습관 데이터
LIFESTYLE_DATA = {
    'main': {
        'title': '생활습관 - 9988 건강정보',
        'icon': '🌱',
        'name': '생활습관',
        'subtitle': '좋은 습관이 건강을 만듭니다',
        'color1': '#667eea',
        'color2': '#764ba2',
        'categories': [
            {'name': '생활습관', 'icon': '🌟', 'file': 'lifestyle-생활습관.html', 'color1': '#667eea', 'color2': '#764ba2'},
            {'name': '생활습관 바꾸기 팁', 'icon': '💡', 'file': 'lifestyle-생활습관바꾸기팁.html', 'color1': '#FA709A', 'color2': '#FEE140'},
        ]
    },
    '생활습관': {
        'title': '생활습관 - 9988 건강정보',
        'icon': '🌟',
        'name': '생활습관',
        'subtitle': '건강한 생활을 위한 습관 만들기',
        'color1': '#667eea',
        'color2': '#764ba2',
        'items': [
            {'name': '수면/피로 관리', 'icon': '😴', 'color1': '#4ECDC4', 'color2': '#44A08D'},
            {'name': '스트레스/정신건강', 'icon': '🧘', 'color1': '#667eea', 'color2': '#764ba2'},
            {'name': '금연/절주 습관 만들기', 'icon': '🚭', 'color1': '#FF6B6B', 'color2': '#EE5A6F'},
            {'name': '건강한 아침/저녁 루틴 만들기', 'icon': '🌅', 'color1': '#FA709A', 'color2': '#FEE140'},
            {'name': '나쁜 습관 고치기 프로젝트', 'icon': '🎯', 'color1': '#4facfe', 'color2': '#00f2fe'},
            {'name': '뇌 건강, 기억력 관리', 'icon': '🧠', 'color1': '#A18CD1', 'color2': '#FBC2EB'},
            {'name': '생활 속 건강 아이템 활용', 'icon': '🏡', 'color1': '#43e97b', 'color2': '#38f9d7'},
            {'name': '중년의 취미, 활력 찾기', 'icon': '🎨', 'color1': '#f093fb', 'color2': '#f5576c'},
        ]
    },
    '생활습관바꾸기팁': {
        'title': '생활습관 바꾸기 팁 - 9988 건강정보',
        'icon': '💡',
        'name': '생활습관 바꾸기 팁',
        'subtitle': '작은 변화가 큰 건강을 만듭니다',
        'color1': '#FA709A',
        'color2': '#FEE140',
        'items': [
            {'name': '중년이 되면 꼭', 'desc': '바꿔야 할 저녁 루틴 3가지', 'icon': '🌙', 'color1': '#667eea', 'color2': '#764ba2'},
            {'name': '하루 종일 피곤하다면?', 'desc': '수면보다 중요한 이것', 'icon': '😴', 'color1': '#4ECDC4', 'color2': '#44A08D'},
            {'name': '의사들이 말하는', 'desc': '아침 건강 루틴, 당신은 하고 있나요?', 'icon': '👨‍⚕️', 'color1': '#FA709A', 'color2': '#FEE140'},
            {'name': '잠 안오는 진짜 이유는', 'desc': '따로 있다? 수면 방해 습관 TOP3', 'icon': '🛌', 'color1': '#A18CD1', 'color2': '#FBC2EB'},
            {'name': '매일 먹는 그 음식', 'desc': '오히려 피로를 유발합니다.', 'icon': '🍽️', 'color1': '#FF6B6B', 'color2': '#EE5A6F'},
            {'name': '스트레스를 확 낮춰주는', 'desc': '5분 습관', 'icon': '😌', 'color1': '#43e97b', 'color2': '#38f9d7'},
            {'name': '뇌를 젊게 만드는', 'desc': '생활습관 지금부터 시작하세요', 'icon': '🧠', 'color1': '#4facfe', 'color2': '#00f2fe'},
            {'name': '하루 10분', 'desc': '기억력 높이는 뇌 자극 루틴', 'icon': '💭', 'color1': '#f093fb', 'color2': '#f5576c'},
            {'name': '혼자 있기 싫을 때', 'desc': '중년 우울감 대처법', 'icon': '😔', 'color1': '#667eea', 'color2': '#764ba2'},
            {'name': '술, 하루 한 잔도', 'desc': '위험할 수 있습니다.', 'icon': '🍺', 'color1': '#FF6B6B', 'color2': '#EE5A6F'},
            {'name': '중년 남성 절주가 어려운', 'desc': '이유와 해결책', 'icon': '🚫', 'color1': '#FA709A', 'color2': '#FEE140'},
            {'name': '담배를 쉽게 끊는', 'desc': '실천 루틴 (스트레스 없이!)', 'icon': '🚭', 'color1': '#4ECDC4', 'color2': '#44A08D'},
            {'name': '앉아만 있는 당신', 'desc': '건강을 망치는 의외의 습관', 'icon': '🪑', 'color1': '#A18CD1', 'color2': '#FBC2EB'},
            {'name': '뒷목 뻐근하다면?', 'desc': '생활 속 이 자세를 의심하세요', 'icon': '🔴', 'color1': '#43e97b', 'color2': '#38f9d7'},
            {'name': '눈 깜빡할 사이 하루 끝', 'desc': '시간을 빼앗는 나쁜 습관', 'icon': '⏰', 'color1': '#4facfe', 'color2': '#00f2fe'},
            {'name': '건강을 지키는', 'desc': '아침 3분 루틴', 'icon': '🌅', 'color1': '#f093fb', 'color2': '#f5576c'},
            {'name': '당신의 수면을 망치는', 'desc': '방 안의 이 물건', 'icon': '🛏️', 'color1': '#667eea', 'color2': '#764ba2'},
            {'name': '40대 이후 꼭 필요한', 'desc': '정신 건강 체크리스트', 'icon': '📋', 'color1': '#FA709A', 'color2': '#FEE140'},
            {'name': '갱년기 우울감?', 'desc': '운동보다 중요한 건 이겁니다.', 'icon': '🌸', 'color1': '#4ECDC4', 'color2': '#44A08D'},
            {'name': '무기력할 때 필요한 것', 'desc': '휴식이 아닙니다.', 'icon': '⚡', 'color1': '#FF6B6B', 'color2': '#EE5A6F'},
        ]
    }
}

def create_lifestyle_main_page():
    """생활습관 메인 페이지 생성"""
    print("Creating: lifestyle-main.html")
    
    data = LIFESTYLE_DATA['main']
    
    header = STANDARD_PAGE_TEMPLATE.format(
        title=data['title'],
        color1=data['color1'],
        color2=data['color2']
    )
    
    # 메뉴 링크를 lifestyle-main.html로 업데이트
    header = header.replace(
        'href="https://health9988234.mycafe24.com/category/생활습관/"',
        'href="lifestyle-main.html"'
    )
    
    cards_html = ""
    for cat in data['categories']:
        cards_html += f'''            <a href="{cat['file']}" class="health-card" style="--card-color-1:{cat['color1']}; --card-color-2:{cat['color2']};">
                <div class="health-card-icon">{cat['icon']}</div>
                <h3>{cat['name']}</h3>
            </a>
            
'''
    
    content = f'''
    <div class="health-card-container">
        <div class="container-content">
            <div class="section-title">
                <div class="main-icon">{data['icon']}</div>
                <h2>{data['name']}</h2>
                <p class="subtitle">{data['subtitle']}</p>
            </div>
            
            <div class="health-cards-grid">
{cards_html}        </div>
        </div>
    </div>
'''
    
    with open('lifestyle-main.html', 'w', encoding='utf-8') as f:
        f.write(header + content + STANDARD_FOOTER)
    
    print(f"  ✅ 생성 완료! (카테고리: {len(data['categories'])}개)")

def create_lifestyle_category_page(key):
    """생활습관 카테고리 페이지 생성"""
    filename = f"lifestyle-{key}.html"
    print(f"Creating: {filename}")
    
    data = LIFESTYLE_DATA[key]
    
    header = STANDARD_PAGE_TEMPLATE.format(
        title=data['title'],
        color1=data['color1'],
        color2=data['color2']
    )
    
    # 메뉴 링크 업데이트
    header = header.replace(
        'href="https://health9988234.mycafe24.com/category/생활습관/"',
        'href="lifestyle-main.html"'
    )
    
    cards_html = ""
    for item in data['items']:
        if 'desc' in item:
            # 생활습관 바꾸기 팁 - 설명 포함
            cards_html += f'''            <a href="#" class="health-card" style="--card-color-1:{item['color1']}; --card-color-2:{item['color2']};">
                <div class="health-card-icon">{item['icon']}</div>
                <h3>{item['name']}</h3>
                <p>{item['desc']}</p>
            </a>
            
'''
        else:
            # 일반 카드
            cards_html += f'''            <a href="#" class="health-card" style="--card-color-1:{item['color1']}; --card-color-2:{item['color2']};">
                <div class="health-card-icon">{item['icon']}</div>
                <h3>{item['name']}</h3>
            </a>
            
'''
    
    content = f'''
    <div class="health-card-container">
        <div class="container-content">
            <a href="lifestyle-main.html" class="back-button">뒤로가기</a>

            <div class="section-title">
                <div class="main-icon">{data['icon']}</div>
                <h2>{data['name']}</h2>
                <p class="subtitle">{data['subtitle']}</p>
            </div>
            
            <div class="health-cards-grid">
{cards_html}        </div>
        </div>
    </div>
'''
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(header + content + STANDARD_FOOTER)
    
    print(f"  ✅ 생성 완료! (항목: {len(data['items'])}개)")

def main():
    print("=" * 60)
    print("🌱 생활습관 페이지 생성")
    print("=" * 60)
    
    # 메인 페이지
    print("\n📄 메인 페이지")
    create_lifestyle_main_page()
    
    # 카테고리 페이지들
    print("\n📁 카테고리 페이지")
    create_lifestyle_category_page('생활습관')
    create_lifestyle_category_page('생활습관바꾸기팁')
    
    print("\n" + "=" * 60)
    print("✅ 완료: 3개 페이지 생성")
    print("=" * 60)
    print("\n📦 생성된 파일:")
    print("  - lifestyle-main.html (메인)")
    print("  - lifestyle-생활습관.html (8개 항목)")
    print("  - lifestyle-생활습관바꾸기팁.html (20개 항목)")

if __name__ == "__main__":
    main()

