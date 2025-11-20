import os
import sys
import io

# UTF-8 인코딩 설정
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 페이지 템플릿 불러오기
from page_template import STANDARD_PAGE_TEMPLATE, STANDARD_FOOTER

# 운동/활동 데이터
EXERCISE_DATA = {
    'main': {
        'title': '운동/활동 - 9988 건강정보',
        'icon': '🏃',
        'name': '운동/활동',
        'subtitle': '움직이는 만큼 건강이 따라옵니다',
        'color1': '#43e97b',
        'color2': '#38f9d7',
        'categories': [
            {'name': '질환별 운동 가이드', 'icon': '🏋️', 'file': 'exercise-질환별운동가이드.html', 'color1': '#4facfe', 'color2': '#00f2fe'},
            {'name': '운동 팁!', 'icon': '💡', 'file': 'exercise-운동팁.html', 'color1': '#43e97b', 'color2': '#38f9d7'},
        ]
    },
    '질환별운동가이드': {
        'title': '질환별 운동 가이드 - 9988 건강정보',
        'icon': '🏋️',
        'name': '질환별 운동 가이드',
        'subtitle': '질환에 맞는 안전한 운동법',
        'color1': '#4facfe',
        'color2': '#00f2fe',
        'items': [
            {'name': '고혈압 운동가이드', 'icon': '🩺', 'color1': '#FF6B6B', 'color2': '#EE5A6F'},
            {'name': '당뇨병 운동가이드', 'icon': '💉', 'color1': '#4ECDC4', 'color2': '#44A08D'},
            {'name': '콜레스테롤(고지혈증) 운동가이드', 'icon': '💊', 'color1': '#A18CD1', 'color2': '#FBC2EB'},
            {'name': '협심증/심근경색 운동가이드', 'icon': '💔', 'color1': '#FA709A', 'color2': '#FEE140'},
            {'name': '퇴행성 관절염 운동가이드', 'icon': '🦵', 'color1': '#667eea', 'color2': '#764ba2'},
            {'name': '오십견 운동가이드', 'icon': '💪', 'color1': '#f093fb', 'color2': '#f5576c'},
            {'name': '골다공증 운동가이드', 'icon': '🦴', 'color1': '#4facfe', 'color2': '#00f2fe'},
            {'name': '지방간 운동가이드', 'icon': '🫀', 'color1': '#43e97b', 'color2': '#38f9d7'},
            {'name': '갱년기 운동가이드', 'icon': '🌸', 'color1': '#fa709a', 'color2': '#fee140'},
            {'name': '우울증 운동가이드', 'icon': '😔', 'color1': '#30cfd0', 'color2': '#330867'},
            {'name': '수면장애 운동가이드', 'icon': '😴', 'color1': '#a8edea', 'color2': '#fed6e3'},
            {'name': '허리 디스크 운동가이드', 'icon': '🔴', 'color1': '#ff9a9e', 'color2': '#fecfef'},
            {'name': '목 디스크 운동가이드', 'icon': '🟠', 'color1': '#ffecd2', 'color2': '#fcb69f'},
        ]
    },
    '운동팁': {
        'title': '운동 팁 - 9988 건강정보',
        'icon': '💡',
        'name': '운동 팁!',
        'subtitle': '실천 가능한 운동 노하우',
        'color1': '#43e97b',
        'color2': '#38f9d7',
        'items': [
            {'name': '하루 10분으로 끝내는', 'desc': '관절 스트레칭 루틴', 'icon': '⏰', 'color1': '#FF6B6B', 'color2': '#EE5A6F'},
            {'name': '고혈압 좋은 유산소운동', 'desc': '이렇게 시작하세요', 'icon': '🏃', 'color1': '#4ECDC4', 'color2': '#44A08D'},
            {'name': '무릎에 무리 없는', 'desc': '하체 근력운동 BEST 3', 'icon': '🦵', 'color1': '#A18CD1', 'color2': '#FBC2EB'},
            {'name': '당뇨 환자를 위한', 'desc': '식후 혈당 안정 운동 루틴', 'icon': '💉', 'color1': '#FA709A', 'color2': '#FEE140'},
            {'name': '땀만 나면 운동이 될까?', 'desc': '운동 효과 높이는 팁', 'icon': '💦', 'color1': '#667eea', 'color2': '#764ba2'},
            {'name': '운동 전 절대 하지 말아야 할', 'desc': '행동 3', 'icon': '🚫', 'color1': '#f093fb', 'color2': '#f5576c'},
            {'name': '잠들기 전 5분', 'desc': '수면을 부르는 스트레칭', 'icon': '😴', 'color1': '#4facfe', 'color2': '#00f2fe'},
            {'name': '헬스장 안 가도 되는', 'desc': '집콕 전신 운동법', 'icon': '🏠', 'color1': '#43e97b', 'color2': '#38f9d7'},
            {'name': '걷기 효과를', 'desc': '2배로 높이는 방법', 'icon': '🚶', 'color1': '#fa709a', 'color2': '#fee140'},
            {'name': '다이어트에 좋은 운동 조합', 'desc': '유산소 + ○○', 'icon': '⚖️', 'color1': '#30cfd0', 'color2': '#330867'},
            {'name': '기분이 가라앉을 때', 'desc': '기분 전환 운동 루틴', 'icon': '😊', 'color1': '#a8edea', 'color2': '#fed6e3'},
            {'name': '나이 들수록 중요한 근육', 'desc': '이렇게 지키세요', 'icon': '💪', 'color1': '#ff9a9e', 'color2': '#fecfef'},
            {'name': '갱년기 여성에게 좋은', 'desc': '요가 자세 TOP 3', 'icon': '🧘', 'color1': '#ffecd2', 'color2': '#fcb69f'},
            {'name': '복부 지방 줄이는', 'desc': '코어 운동 루틴', 'icon': '🔥', 'color1': '#ff6e7f', 'color2': '#bfe9ff'},
            {'name': '일하면서 할 수 있는', 'desc': '의자 스트레칭', 'icon': '🪑', 'color1': '#e0c3fc', 'color2': '#8ec5fc'},
            {'name': '아침에 하면 활력이 살아나는', 'desc': '운동 루틴', 'icon': '🌅', 'color1': '#fbc2eb', 'color2': '#a6c1ee'},
            {'name': '운동 전후 꼭 챙겨야 할', 'desc': '음식과 타이밍', 'icon': '🍎', 'color1': '#fdcbf1', 'color2': '#e6dee9'},
            {'name': '체중보다 중요한', 'desc': '근육량 관리법 알려드려요', 'icon': '📊', 'color1': '#a1c4fd', 'color2': '#c2e9fb'},
            {'name': '허리 아픈 분들을 위한', 'desc': '부담 없는 운동 팁', 'icon': '🔴', 'color1': '#ffecd2', 'color2': '#fcb69f'},
            {'name': '스트레칭은 언제 해야 효과적일까?', 'desc': '아침 vs 저녁', 'icon': '🤔', 'color1': '#ff9a9e', 'color2': '#fad0c4'},
        ]
    }
}

def create_exercise_main_page():
    """운동/활동 메인 페이지 생성"""
    print("Creating: exercise-main.html")
    
    data = EXERCISE_DATA['main']
    
    header = STANDARD_PAGE_TEMPLATE.format(
        title=data['title'],
        color1=data['color1'],
        color2=data['color2']
    )
    
    # 메뉴 링크를 exercise-main.html로 업데이트
    header = header.replace(
        'href="https://health9988234.mycafe24.com/category/운동-활동/"',
        'href="exercise-main.html"'
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
    
    with open('exercise-main.html', 'w', encoding='utf-8') as f:
        f.write(header + content + STANDARD_FOOTER)
    
    print(f"  ✅ 생성 완료! (카테고리: {len(data['categories'])}개)")

def create_exercise_category_page(key):
    """운동/활동 카테고리 페이지 생성"""
    filename = f"exercise-{key}.html"
    print(f"Creating: {filename}")
    
    data = EXERCISE_DATA[key]
    
    header = STANDARD_PAGE_TEMPLATE.format(
        title=data['title'],
        color1=data['color1'],
        color2=data['color2']
    )
    
    # 메뉴 링크 업데이트
    header = header.replace(
        'href="https://health9988234.mycafe24.com/category/운동-활동/"',
        'href="exercise-main.html"'
    )
    
    cards_html = ""
    for item in data['items']:
        if 'desc' in item:
            # 운동 팁 - 설명 포함
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
            <a href="exercise-main.html" class="back-button">뒤로가기</a>

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
    print("🏃 운동/활동 페이지 생성")
    print("=" * 60)
    
    # 메인 페이지
    print("\n📄 메인 페이지")
    create_exercise_main_page()
    
    # 카테고리 페이지들
    print("\n📁 카테고리 페이지")
    create_exercise_category_page('질환별운동가이드')
    create_exercise_category_page('운동팁')
    
    print("\n" + "=" * 60)
    print("✅ 완료: 3개 페이지 생성")
    print("=" * 60)
    print("\n📦 생성된 파일:")
    print("  - exercise-main.html (메인)")
    print("  - exercise-질환별운동가이드.html (13개 항목)")
    print("  - exercise-운동팁.html (20개 항목)")

if __name__ == "__main__":
    main()

