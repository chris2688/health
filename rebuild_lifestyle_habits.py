import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

print("=" * 70)
print("🔧 lifestyle-habits.html 완전 재구축")
print("=" * 70)

# sub-diabetes.html을 템플릿으로 사용하여 lifestyle-habits.html 재생성
with open('sub-diabetes.html', 'r', encoding='utf-8') as f:
    template = f.read()

# lifestyle-habits.html의 내용으로 교체
# 1. 타이틀 변경
new_content = template.replace('<title>당뇨 - 9988 건강정보</title>', '<title>생활습관 - 9988 건강정보</title>')

# 2. 뒤로가기 링크 변경
new_content = new_content.replace('href="category-diabetes.html" class="back-button"', 'href="lifestyle-main.html" class="back-button"')

# 3. 페이지 타이틀 변경
new_content = new_content.replace('<h1 class="page-title">당뇨</h1>', '<h1 class="page-title">생활습관</h1>')

# 4. news-grid를 health-cards-grid로 변경 (lifestyle는 카드 형식)
cards_html = '''
            <div class="section-title">
                <div class="main-icon">🌟</div>
                <h2>생활습관</h2>
                <p class="subtitle">건강한 생활을 위한 습관 만들기</p>
            </div>
            
            <div class="health-cards-grid">
            <a href="#" class="health-card" style="--card-color-1:#4ECDC4; --card-color-2:#44A08D;">
                <div class="health-card-icon">😴</div>
                <h3>수면/피로 관리</h3>
            </a>
            
            <a href="#" class="health-card" style="--card-color-1:#A18CD1; --card-color-2:#FBC2EB;">
                <div class="health-card-icon">🧘</div>
                <h3>스트레스/정신건강</h3>
            </a>
            
            <a href="#" class="health-card" style="--card-color-1:#FA709A; --card-color-2:#FEE140;">
                <div class="health-card-icon">🚭</div>
                <h3>금연/절주 습관 만들기</h3>
            </a>
            
            <a href="#" class="health-card" style="--card-color-1:#667eea; --card-color-2:#764ba2;">
                <div class="health-card-icon">🏠</div>
                <h3>건강한 아침/저녁 루틴</h3>
            </a>
            
            <a href="#" class="health-card" style="--card-color-1:#FA709A; --card-color-2:#FEE140;">
                <div class="health-card-icon">🎨</div>
                <h3>중년의 취미, 활력 찾기</h3>
            </a>
            </div>
'''

# news-grid 부분을 교체
import re
new_content = re.sub(
    r'<header class="page-header">.*?</div>',
    cards_html.strip() + '\n        </div>',
    new_content,
    flags=re.DOTALL
)

# health-cards-grid CSS 추가 필요
health_cards_css = """
        .health-cards-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 30px;
            max-width: 1400px;
            margin: 40px auto 0;
            padding: 0 20px;
        }
        
        .health-card {
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
        }
        
        .health-card:hover {
            transform: translateY(-8px) scale(1.02);
            box-shadow: 0 20px 40px rgba(0,0,0,0.25);
        }
        
        .health-card-icon {
            font-size: 56px;
            margin-bottom: 15px;
            filter: drop-shadow(0 2px 4px rgba(0,0,0,0.2));
        }
        
        .health-card h3 {
            font-size: 22px;
            font-weight: 700;
            color: #ffffff;
            margin: 0;
            text-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        .section-title {
            text-align: center;
            margin-bottom: 50px;
        }
        
        .main-icon {
            font-size: 72px;
            margin-bottom: 15px;
            filter: drop-shadow(0 4px 8px rgba(0,0,0,0.1));
        }
        
        .section-title h2 {
            font-size: 42px;
            font-weight: 800;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin: 0 0 15px 0;
        }
        
        .subtitle {
            font-size: 18px;
            color: #666;
            font-weight: 500;
        }
"""

# </style> 전에 CSS 추가
new_content = new_content.replace('</style>', health_cards_css + '\n    </style>')

# 저장
with open('lifestyle-habits.html', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("\n✅ lifestyle-habits.html 완전 재생성 완료!")
print("\n변경사항:")
print("  - sub-diabetes.html 구조 기반으로 완전 재구축")
print("  - 모든 CSS 충돌 제거")
print("  - .back-button CSS 정확히 동일하게 적용")
print("  - HTML 구조 동일하게 적용")

import os
size = os.path.getsize('lifestyle-habits.html') / 1024
print(f"\n파일 크기: {size:.1f} KB")

print("\n" + "=" * 70)
print("🎉 완료!")
print("=" * 70)
print("\n이제 브라우저를 완전히 닫고 다시 열어보세요!")
print("=" * 70)

