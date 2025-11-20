import os
import sys
import io

# UTF-8 인코딩 설정
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 공통 헤더 템플릿
HEADER_TEMPLATE = '''<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, "Noto Sans KR", sans-serif;
            background: #f5f7fa;
            min-height: 100vh;
        }}
        
        /* ========== 헤더 스타일 ========== */
        .main-header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            box-shadow: 0 4px 20px rgba(102, 126, 234, 0.3);
            position: sticky;
            top: 0;
            z-index: 1000;
        }}
        
        .header-content {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 0 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            min-height: 80px;
        }}
        
        .logo-container {{
            display: flex;
            align-items: center;
            gap: 15px;
            text-decoration: none;
            transition: transform 0.3s;
        }}
        
        .logo-container:hover {{
            transform: scale(1.05);
        }}
        
        .logo-image {{
            height: 50px;
            width: auto;
            border-radius: 8px;
            background: white;
            padding: 5px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        
        .main-nav {{
            display: flex;
            gap: 0;
        }}
        
        .nav-item {{
            padding: 10px 24px;
            color: white;
            text-decoration: none;
            font-weight: 600;
            font-size: 16px;
            transition: all 0.3s;
            position: relative;
            border-radius: 8px;
        }}
        
        .nav-item::before {{
            content: '';
            position: absolute;
            bottom: 0;
            left: 50%;
            width: 0;
            height: 3px;
            background: white;
            transform: translateX(-50%);
            transition: width 0.3s;
        }}
        
        .nav-item:hover {{
            background: rgba(255,255,255,0.15);
        }}
        
        .nav-item:hover::before {{
            width: 60%;
        }}
        
        .mobile-menu-btn {{
            display: none;
            background: none;
            border: none;
            color: white;
            font-size: 28px;
            cursor: pointer;
            padding: 10px;
        }}
        
        /* ========== 뒤로가기 버튼 ========== */
        .back-button {{
            display: inline-block;
            margin: 0 0 30px 0;
            margin-left: max(20px, calc((100% - 1200px) / 2 + 20px));
            padding: 12px 24px;
            background: rgba(102, 126, 234, 0.1);
            color: #667eea;
            text-decoration: none;
            border-radius: 50px;
            font-weight: 600;
            font-size: 15px;
            transition: all 0.3s;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        }}
        
        .back-button:hover {{
            background: rgba(102, 126, 234, 0.2);
            transform: translateX(-5px);
        }}
        
        .back-button::before {{
            content: '← ';
            font-weight: bold;
        }}
        
        /* ========== 콘텐츠 영역 ========== */
        .health-card-container {{
            padding: 40px 20px 60px;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            min-height: calc(100vh - 80px);
        }}
        
        .section-title {{
            text-align: center;
            margin-bottom: 50px;
        }}
        
        .main-icon {{
            font-size: 72px;
            margin-bottom: 15px;
            filter: drop-shadow(0 4px 8px rgba(0,0,0,0.1));
        }}
        
        .section-title h2 {{
            font-size: 42px;
            font-weight: 800;
            background: linear-gradient(135deg, {color1} 0%, {color2} 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin: 0 0 15px 0;
        }}
        
        .subtitle {{
            font-size: 18px;
            color: #666;
            font-weight: 500;
        }}
        
        .health-cards-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 30px;
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
        }}
        
        .health-card {{
            position: relative;
            padding: 40px 30px;
            border-radius: 24px;
            background: linear-gradient(135deg, var(--card-color-1) 0%, var(--card-color-2) 100%);
            box-shadow: 0 10px 30px rgba(0,0,0,0.15);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            cursor: pointer;
            overflow: hidden;
            min-height: 200px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
            text-decoration: none;
        }}
        
        .health-card:hover {{
            transform: translateY(-8px) scale(1.02);
            box-shadow: 0 20px 40px rgba(0,0,0,0.25);
        }}
        
        .health-card::before {{
            content: '';
            position: absolute;
            top: 0;
            right: 0;
            width: 120px;
            height: 120px;
            background: rgba(255,255,255,0.1);
            border-radius: 50%;
            transform: translate(40%, -40%);
        }}
        
        .health-card-icon {{
            font-size: 56px;
            margin-bottom: 15px;
            filter: drop-shadow(0 2px 4px rgba(0,0,0,0.2));
            position: relative;
            z-index: 1;
        }}
        
        .health-card h3 {{
            font-size: 22px;
            font-weight: 700;
            color: #ffffff;
            margin: 0;
            text-shadow: 0 2px 4px rgba(0,0,0,0.1);
            position: relative;
            z-index: 1;
        }}
        
        .health-card p {{
            font-size: 14px;
            color: rgba(255,255,255,0.9);
            margin-top: 8px;
            line-height: 1.4;
            position: relative;
            z-index: 1;
        }}
        
        @media (max-width: 768px) {{
            .header-content {{
                min-height: 70px;
            }}
            
            .logo-image {{
                height: 40px;
            }}
            
            .main-nav {{
                display: none;
                position: absolute;
                top: 100%;
                left: 0;
                right: 0;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                flex-direction: column;
                padding: 20px;
                box-shadow: 0 4px 20px rgba(0,0,0,0.2);
            }}
            
            .main-nav.active {{
                display: flex;
            }}
            
            .nav-item {{
                padding: 15px 20px;
                text-align: center;
            }}
            
            .mobile-menu-btn {{
                display: block;
            }}
            
            .back-button {{
                margin-left: 20px;
            }}
            
            .health-cards-grid {{
                grid-template-columns: 1fr;
                gap: 20px;
            }}
            
            .section-title h2 {{
                font-size: 32px;
            }}
            
            .main-icon {{
                font-size: 56px;
            }}
        }}
    </style>
</head>
<body>
    <header class="main-header">
        <div class="header-content">
            <a href="index-v2.html" class="logo-container">
                <img src="https://health9988234.mycafe24.com/wp-content/uploads/2025/11/cropped-1-1.png" 
                     alt="9988 건강 연구소" 
                     class="logo-image">
            </a>
            
            <nav class="main-nav" id="mainNav">
                <a href="index-v2.html" class="nav-item">질환별 정보</a>
                <a href="food-main.html" class="nav-item">식단/음식</a>
                <a href="https://health9988234.mycafe24.com/category/운동-활동/" class="nav-item">운동/활동</a>
                <a href="https://health9988234.mycafe24.com/category/생활습관/" class="nav-item">생활습관</a>
                <a href="https://health9988234.mycafe24.com/category/건강-new/" class="nav-item">건강News</a>
            </nav>
            
            <button class="mobile-menu-btn" id="mobileMenuBtn">☰</button>
        </div>
    </header>
'''

# 식단/음식 데이터
FOOD_DATA = {
    'main': {
        'title': '식단/음식 - 9988 건강정보',
        'icon': '🍽️',
        'name': '식단/음식',
        'subtitle': '건강은 식탁에서 시작됩니다',
        'color1': '#4facfe',
        'color2': '#00f2fe',
        'categories': [
            {'name': '질환별 식단', 'icon': '🥗', 'file': 'food-질환별식단.html', 'color1': '#4ECDC4', 'color2': '#44A08D'},
            {'name': '피해야 할 과일', 'icon': '🍎', 'file': 'food-피해야할과일.html', 'color1': '#FA709A', 'color2': '#FEE140'},
            {'name': '모르면 독이 된다', 'icon': '⚠️', 'file': 'food-모르면독이된다.html', 'color1': '#FF6B6B', 'color2': '#EE5A6F'},
        ]
    },
    '질환별식단': {
        'title': '질환별 식단 - 9988 건강정보',
        'icon': '🥗',
        'name': '질환별 식단',
        'subtitle': '질환에 맞는 올바른 식단 관리',
        'color1': '#4ECDC4',
        'color2': '#44A08D',
        'items': [
            {'name': '고혈압 식단', 'icon': '🩺', 'color1': '#FF6B6B', 'color2': '#EE5A6F'},
            {'name': '당뇨 식단', 'icon': '💉', 'color1': '#4ECDC4', 'color2': '#44A08D'},
            {'name': '지방간 식단', 'icon': '🫀', 'color1': '#A18CD1', 'color2': '#FBC2EB'},
            {'name': '갱년기 식단', 'icon': '🌸', 'color1': '#FA709A', 'color2': '#FEE140'},
            {'name': '우울증 식단', 'icon': '😔', 'color1': '#667eea', 'color2': '#764ba2'},
            {'name': '협심증/심근경색 식단', 'icon': '💔', 'color1': '#f093fb', 'color2': '#f5576c'},
            {'name': '퇴행성 관절염/오십견 식단', 'icon': '🦴', 'color1': '#4facfe', 'color2': '#00f2fe'},
            {'name': '골다공증 식단', 'icon': '🦵', 'color1': '#43e97b', 'color2': '#38f9d7'},
            {'name': '역류성 식도염 식단', 'icon': '🔥', 'color1': '#fa709a', 'color2': '#fee140'},
            {'name': '고지혈증(콜레스테롤) 식단', 'icon': '💊', 'color1': '#30cfd0', 'color2': '#330867'},
        ]
    },
    '피해야할과일': {
        'title': '피해야 할 과일 - 9988 건강정보',
        'icon': '🍎',
        'name': '피해야 할 과일',
        'subtitle': '질환별로 주의해야 할 과일 정보',
        'color1': '#FA709A',
        'color2': '#FEE140',
        'items': [
            {'name': '고혈압', 'desc': '피해야 할 과일 3가지 (의외의 1등은?)', 'icon': '🩺', 'color1': '#FF6B6B', 'color2': '#EE5A6F'},
            {'name': '당뇨', 'desc': '이 과일은 꼭 피하세요. 혈당이 확 오릅니다.', 'icon': '💉', 'color1': '#4ECDC4', 'color2': '#44A08D'},
            {'name': '고지혈증(콜레스테롤)', 'desc': '콜레스테롤 높은 분들, 이 과일은 피하셔야 합니다.', 'icon': '💊', 'color1': '#A18CD1', 'color2': '#FBC2EB'},
            {'name': '지방간', 'desc': '간에 독이 되는 과일? 달콤하지만 위험한 선택', 'icon': '🫀', 'color1': '#FA709A', 'color2': '#FEE140'},
            {'name': '위염/역류성 식도염', 'desc': '위염 있으세요? 속 쓰리게 만드는 과일 3가지', 'icon': '🔥', 'color1': '#667eea', 'color2': '#764ba2'},
            {'name': '골다공증', 'desc': '뼈 건강에 안 좋은 과일이 있다고요? 꼭 피하세요!', 'icon': '🦴', 'color1': '#f093fb', 'color2': '#f5576c'},
            {'name': '갱년기', 'desc': '갱년기 증상 더 악화시키는 과일, 의외로 자주 먹는 이것!', 'icon': '🌸', 'color1': '#4facfe', 'color2': '#00f2fe'},
            {'name': '우울증', 'desc': '기분 더 가라앉게 만드는 과일? 우울증에 안 좋은 과일 리스트', 'icon': '😔', 'color1': '#43e97b', 'color2': '#38f9d7'},
            {'name': '수면장애', 'desc': '잠 안 올 때 피해야 할 과일, 숙면을 방해합니다', 'icon': '😴', 'color1': '#fa709a', 'color2': '#fee140'},
            {'name': '협심증/심근경색', 'desc': '심장 건강에 해로운 과일? 협심증 환자 주의!', 'icon': '💔', 'color1': '#30cfd0', 'color2': '#330867'},
        ]
    },
    '모르면독이된다': {
        'title': '모르면 독이 된다 - 9988 건강정보',
        'icon': '⚠️',
        'name': '모르면 독이 된다',
        'subtitle': '건강을 해치는 잘못된 식습관',
        'color1': '#FF6B6B',
        'color2': '#EE5A6F',
        'items': [
            {'name': '비타민 먹을 때 절대 같이 먹으면 안되는 음식', 'icon': '💊', 'color1': '#FF6B6B', 'color2': '#EE5A6F'},
            {'name': '아침 공복에 먹으면 해로운 음식', 'icon': '🌅', 'color1': '#4ECDC4', 'color2': '#44A08D'},
            {'name': '자기 전에 먹으면 살찌는 음식 TOP3', 'icon': '🌙', 'color1': '#A18CD1', 'color2': '#FBC2EB'},
            {'name': '아침에 먹기 좋은 vs 나쁜 음식', 'icon': '☀️', 'color1': '#FA709A', 'color2': '#FEE140'},
            {'name': '당 줄였는데 더 해로운 \'무설탕\' 음식들', 'icon': '🚫', 'color1': '#667eea', 'color2': '#764ba2'},
            {'name': '건강식인 줄 알았는데? 숨은 나트륨 폭탄', 'icon': '💣', 'color1': '#f093fb', 'color2': '#f5576c'},
            {'name': '다이어트할 때 절대 같이 먹으면 안되는 조합', 'icon': '⚖️', 'color1': '#4facfe', 'color2': '#00f2fe'},
            {'name': '과일주스는 건강할까? 진짜 진실', 'icon': '🧃', 'color1': '#43e97b', 'color2': '#38f9d7'},
            {'name': '단백질은 많이 먹을수록 좋다?', 'icon': '🥩', 'color1': '#fa709a', 'color2': '#fee140'},
            {'name': '밥을 줄였는데도 살 안 빠지는 이유', 'icon': '🍚', 'color1': '#30cfd0', 'color2': '#330867'},
            {'name': '샐러드만 먹는데 혈당 오르는 이유', 'icon': '🥗', 'color1': '#a8edea', 'color2': '#fed6e3'},
            {'name': '오메가3와 절대 같이 먹지 말아야 할 음식', 'icon': '🐟', 'color1': '#ff9a9e', 'color2': '#fecfef'},
            {'name': '칼슘제 복용 시 피해야 할 음료', 'icon': '🥛', 'color1': '#ffecd2', 'color2': '#fcb69f'},
            {'name': '설탕보다 무서운 당분 \'○○ 시럽\'이 문제입니다', 'icon': '🍯', 'color1': '#ff6e7f', 'color2': '#bfe9ff'},
            {'name': '건강 간식에 숨은 나트륨', 'icon': '🍿', 'color1': '#e0c3fc', 'color2': '#8ec5fc'},
        ]
    }
}

def create_food_main_page():
    """식단/음식 메인 페이지 생성"""
    print("Creating: food-main.html")
    
    data = FOOD_DATA['main']
    
    header = HEADER_TEMPLATE.format(
        title=data['title'],
        color1=data['color1'],
        color2=data['color2']
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
        <div class="section-title">
            <div class="main-icon">{data['icon']}</div>
            <h2>{data['name']}</h2>
            <p class="subtitle">{data['subtitle']}</p>
        </div>
        
        <div class="health-cards-grid">
{cards_html}        </div>
    </div>

    <script>
        document.getElementById('mobileMenuBtn').addEventListener('click', function() {{
            document.getElementById('mainNav').classList.toggle('active');
        }});
    </script>
</body>
</html>'''
    
    with open('food-main.html', 'w', encoding='utf-8') as f:
        f.write(header + content)
    
    print(f"  ✅ 생성 완료! (카테고리: {len(data['categories'])}개)")

def create_food_category_page(key):
    """식단/음식 카테고리 페이지 생성"""
    filename = f"food-{key}.html"
    print(f"Creating: {filename}")
    
    data = FOOD_DATA[key]
    
    header = HEADER_TEMPLATE.format(
        title=data['title'],
        color1=data['color1'],
        color2=data['color2']
    )
    
    cards_html = ""
    for item in data['items']:
        if 'desc' in item:
            # 피해야 할 과일 - 설명 포함
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
    <a href="food-main.html" class="back-button">뒤로가기</a>

    <div class="health-card-container">
        <div class="section-title">
            <div class="main-icon">{data['icon']}</div>
            <h2>{data['name']}</h2>
            <p class="subtitle">{data['subtitle']}</p>
        </div>
        
        <div class="health-cards-grid">
{cards_html}        </div>
    </div>

    <script>
        document.getElementById('mobileMenuBtn').addEventListener('click', function() {{
            document.getElementById('mainNav').classList.toggle('active');
        }});
    </script>
</body>
</html>'''
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(header + content)
    
    print(f"  ✅ 생성 완료! (항목: {len(data['items'])}개)")

def main():
    print("=" * 60)
    print("🍽️ 식단/음식 페이지 생성")
    print("=" * 60)
    
    # 메인 페이지
    print("\n📄 메인 페이지")
    create_food_main_page()
    
    # 카테고리 페이지들
    print("\n📁 카테고리 페이지")
    create_food_category_page('질환별식단')
    create_food_category_page('피해야할과일')
    create_food_category_page('모르면독이된다')
    
    print("\n" + "=" * 60)
    print("✅ 완료: 4개 페이지 생성")
    print("=" * 60)
    print("\n📦 생성된 파일:")
    print("  - food-main.html (메인)")
    print("  - food-질환별식단.html (10개 항목)")
    print("  - food-피해야할과일.html (10개 항목)")
    print("  - food-모르면독이된다.html (15개 항목)")

if __name__ == "__main__":
    main()

