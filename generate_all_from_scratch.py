import os
import sys
import io

# UTF-8 인코딩 설정
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 공통 헤더 (index-v2.html과 동일)
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
        
        /* ========== 헤더 스타일 (메인과 동일) ========== */
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
        
        /* ========== 뒤로가기 버튼 (헤더 밖) ========== */
        .back-button {{
            display: inline-block;
            margin: 20px 0 0 40px;
            padding: 12px 24px;
            background: rgba(102, 126, 234, 0.1);
            color: #667eea;
            text-decoration: none;
            border-radius: 50px;
            font-weight: 600;
            font-size: 15px;
            transition: all 0.3s;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
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
                <a href="https://health9988234.mycafe24.com/category/식단-음식/" class="nav-item">식단/음식</a>
                <a href="https://health9988234.mycafe24.com/category/운동-활동/" class="nav-item">운동/활동</a>
                <a href="https://health9988234.mycafe24.com/category/생활습관/" class="nav-item">생활습관</a>
                <a href="https://health9988234.mycafe24.com/category/건강-new/" class="nav-item">건강News</a>
            </nav>
            
            <button class="mobile-menu-btn" id="mobileMenuBtn">☰</button>
        </div>
    </header>
'''

# 카테고리 데이터
CATEGORIES = {
    '심혈관질환': {
        'title': '심혈관 질환 - 9988 건강정보',
        'icon': '❤️',
        'name': '심혈관 질환',
        'color1': '#FF6B6B',
        'color2': '#EE5A6F',
        'subcategories': [
            {'name': '고혈압', 'icon': '🩺', 'file': 'sub-고혈압.html', 'color1': '#FF6B6B', 'color2': '#EE5A6F'},
            {'name': '고지혈증(콜레스테롤)', 'icon': '💊', 'file': 'sub-고지혈증.html', 'color1': '#4ECDC4', 'color2': '#44A08D'},
            {'name': '협심증/심근경색', 'icon': '💔', 'file': 'sub-협심증심근경색.html', 'color1': '#A18CD1', 'color2': '#FBC2EB'},
            {'name': '동맥경화', 'icon': '🫀', 'file': 'sub-동맥경화.html', 'color1': '#FA709A', 'color2': '#FEE140'},
            {'name': '뇌졸중', 'icon': '🧠', 'file': 'sub-뇌졸중.html', 'color1': '#667eea', 'color2': '#764ba2'},
        ]
    },
    '당뇨병': {
        'title': '당뇨병 - 9988 건강정보',
        'icon': '💉',
        'name': '당뇨병',
        'color1': '#4ECDC4',
        'color2': '#44A08D',
        'subcategories': [
            {'name': '당뇨병', 'icon': '💉', 'file': 'sub-당뇨.html', 'color1': '#4ECDC4', 'color2': '#44A08D'},
            {'name': '공복혈당장애', 'icon': '📊', 'file': 'sub-공복혈당장애.html', 'color1': '#FF6B6B', 'color2': '#EE5A6F'},
            {'name': '당뇨병 합병증 (망막,신장 등)', 'icon': '👁️', 'file': 'sub-당뇨병합병증.html', 'color1': '#A18CD1', 'color2': '#FBC2EB'},
        ]
    },
    '관절근골격계': {
        'title': '관절/근골격계 질환 - 9988 건강정보',
        'icon': '🦴',
        'name': '관절/근골격계 질환',
        'color1': '#A18CD1',
        'color2': '#FBC2EB',
        'subcategories': [
            {'name': '퇴행성 관절염', 'icon': '🦵', 'file': 'sub-퇴행성관절염.html', 'color1': '#FF6B6B', 'color2': '#EE5A6F'},
            {'name': '허리디스크/목디스크', 'icon': '🔴', 'file': 'sub-허리디스크목디스크.html', 'color1': '#4ECDC4', 'color2': '#44A08D'},
            {'name': '골다공증', 'icon': '🦴', 'file': 'sub-골다공증.html', 'color1': '#A18CD1', 'color2': '#FBC2EB'},
            {'name': '오십견(유착성 관절낭염)', 'icon': '💪', 'file': 'sub-오십견.html', 'color1': '#FA709A', 'color2': '#FEE140'},
        ]
    },
    '소화기질환': {
        'title': '소화기 질환 - 9988 건강정보',
        'icon': '🍽️',
        'name': '소화기 질환',
        'color1': '#f093fb',
        'color2': '#f5576c',
        'subcategories': [
            {'name': '위염/위궤양', 'icon': '🔴', 'file': 'sub-위염위궤양.html', 'color1': '#FF6B6B', 'color2': '#EE5A6F'},
            {'name': '역류성 식도염', 'icon': '🔥', 'file': 'sub-역류성식도염.html', 'color1': '#4ECDC4', 'color2': '#44A08D'},
            {'name': '과민성 대장증후군', 'icon': '💫', 'file': 'sub-과민성대장증후군.html', 'color1': '#A18CD1', 'color2': '#FBC2EB'},
            {'name': '지방간/간기능 저하', 'icon': '🫀', 'file': 'sub-지방간.html', 'color1': '#FA709A', 'color2': '#FEE140'},
        ]
    },
    '호르몬내분비': {
        'title': '호르몬/내분비 질환 - 9988 건강정보',
        'icon': '🌡️',
        'name': '호르몬/내분비 질환',
        'color1': '#FA709A',
        'color2': '#FEE140',
        'subcategories': [
            {'name': '갑상선 기능 저하/항진', 'icon': '🦋', 'file': 'sub-갑상선.html', 'color1': '#FF6B6B', 'color2': '#EE5A6F'},
            {'name': '갱년기 증후군', 'icon': '🌸', 'file': 'sub-갱년기증후군.html', 'color1': '#4ECDC4', 'color2': '#44A08D'},
            {'name': '대사증후군', 'icon': '⚖️', 'file': 'sub-대사증후군.html', 'color1': '#A18CD1', 'color2': '#FBC2EB'},
        ]
    },
    '정신건강신경계': {
        'title': '정신건강/신경계 - 9988 건강정보',
        'icon': '🧠',
        'name': '정신건강/신경계',
        'color1': '#667eea',
        'color2': '#764ba2',
        'subcategories': [
            {'name': '우울증/번아웃 증후군', 'icon': '😔', 'file': 'sub-우울증번아웃.html', 'color1': '#FF6B6B', 'color2': '#EE5A6F'},
            {'name': '수면장애/불면증', 'icon': '😴', 'file': 'sub-수면장애불면증.html', 'color1': '#4ECDC4', 'color2': '#44A08D'},
            {'name': '치매/경도인지장애', 'icon': '🧩', 'file': 'sub-치매경도인지장애.html', 'color1': '#A18CD1', 'color2': '#FBC2EB'},
            {'name': '이명/어지럼증', 'icon': '👂', 'file': 'sub-이명어지럼증.html', 'color1': '#FA709A', 'color2': '#FEE140'},
        ]
    },
    '안과치과기타': {
        'title': '안과/치과/기타 - 9988 건강정보',
        'icon': '👁️',
        'name': '안과/치과/기타',
        'color1': '#4facfe',
        'color2': '#00f2fe',
        'subcategories': [
            {'name': '백내장/녹내장', 'icon': '👓', 'file': 'sub-백내장녹내장.html', 'color1': '#FF6B6B', 'color2': '#EE5A6F'},
            {'name': '치주염/치아손실', 'icon': '🦷', 'file': 'sub-치주염치아손실.html', 'color1': '#4ECDC4', 'color2': '#44A08D'},
            {'name': '비만/체형변화', 'icon': '⚖️', 'file': 'sub-비만체형변화.html', 'color1': '#A18CD1', 'color2': '#FBC2EB'},
        ]
    },
}

def create_category_page(category_key, data):
    """카테고리 페이지 생성"""
    filename = f"category-{category_key}.html"
    print(f"Creating: {filename}")
    
    # 헤더
    header = HEADER_TEMPLATE.format(
        title=data['title'],
        color1=data['color1'],
        color2=data['color2']
    )
    
    # 서브카테고리 카드들
    cards_html = ""
    for sub in data['subcategories']:
        cards_html += f'''            <a href="{sub['file']}" class="health-card" style="--card-color-1:{sub['color1']}; --card-color-2:{sub['color2']};">
                <div class="health-card-icon">{sub['icon']}</div>
                <h3>{sub['name']}</h3>
            </a>
            
'''
    
    # 본문
    content = f'''
    <a href="index-v2.html" class="back-button">뒤로가기</a>

    <div class="health-card-container">
        <div class="section-title">
            <div class="main-icon">{data['icon']}</div>
            <h2>{data['name']}</h2>
            <p class="subtitle">관심있는 주제를 선택하세요</p>
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
    
    # 파일 저장
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(header + content)
    
    print(f"  ✅ 생성 완료! (서브카테고리: {len(data['subcategories'])}개)")

def main():
    print("=" * 60)
    print("🎨 카테고리 페이지 새로 생성")
    print("=" * 60)
    
    for key, data in CATEGORIES.items():
        create_category_page(key, data)
    
    print("\n" + "=" * 60)
    print(f"✅ 완료: {len(CATEGORIES)}개 파일 생성")
    print("=" * 60)

if __name__ == "__main__":
    main()

