import os
import glob
import re
import sys
import io

# UTF-8 인코딩 설정
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 카테고리별 색상 매핑
CATEGORY_COLORS = {
    '심혈관': {'color1': '#FF6B6B', 'color2': '#EE5A6F'},
    '당뇨': {'color1': '#4ECDC4', 'color2': '#44A08D'},
    '관절': {'color1': '#A18CD1', 'color2': '#FBC2EB'},
    '호르몬': {'color1': '#FA709A', 'color2': '#FEE140'},
    '정신': {'color1': '#667eea', 'color2': '#764ba2'},
    '소화': {'color1': '#f093fb', 'color2': '#f5576c'},
    '안과': {'color1': '#4facfe', 'color2': '#00f2fe'},
}

def rebuild_category_file(filepath):
    """카테고리 파일 완전히 재생성"""
    print(f"Rebuilding: {filepath}")
    
    try:
        # 기존 파일에서 콘텐츠 추출
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 제목 추출
        title_match = re.search(r'<title>(.*?)</title>', content)
        title = title_match.group(1) if title_match else "9988 건강 연구소"
        
        # 메인 아이콘 추출
        icon_match = re.search(r'<div class="main-icon">(.*?)</div>', content)
        icon = icon_match.group(1) if icon_match else "❤️"
        
        # 제목 텍스트 추출
        h2_match = re.search(r'<h2>(.*?)</h2>', content)
        page_title = h2_match.group(1) if h2_match else "질환 정보"
        
        # 카드 그리드 추출
        cards_match = re.search(r'<div class="health-cards-grid">(.*?)</div>\s*</div>\s*</div>', content, re.DOTALL)
        cards_html = cards_match.group(1) if cards_match else ""
        
        # 색상 결정
        color1 = '#667eea'
        color2 = '#764ba2'
        for key, colors in CATEGORY_COLORS.items():
            if key in filepath or key in page_title:
                color1 = colors['color1']
                color2 = colors['color2']
                break
        
        # 새로운 HTML 생성
        new_html = f'''<!DOCTYPE html>
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
        
        /* 헤더 */
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
            position: relative;
        }}
        
        /* 뒤로가기 버튼 */
        .back-button {{
            position: absolute;
            left: 20px;
            background: rgba(255,255,255,0.2);
            color: white;
            width: 40px;
            height: 40px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            text-decoration: none;
            font-size: 24px;
            transition: all 0.3s;
            font-weight: bold;
        }}
        
        .back-button:hover {{
            background: rgba(255,255,255,0.3);
            transform: scale(1.1);
        }}
        
        .logo-container {{
            position: absolute;
            left: 50%;
            transform: translateX(-50%);
            display: flex;
            align-items: center;
            text-decoration: none;
            transition: transform 0.3s;
        }}
        
        .logo-container:hover {{
            transform: translateX(-50%) scale(1.05);
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
            margin-left: auto;
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
        
        /* 콘텐츠 */
        .health-card-container {{
            padding: 60px 20px;
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
            
            .back-button {{
                left: 10px;
                width: 36px;
                height: 36px;
                font-size: 20px;
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
            <a href="javascript:history.back()" class="back-button">←</a>
            
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

    <div class="health-card-container">
        <div class="section-title">
            <div class="main-icon">{icon}</div>
            <h2>{page_title}</h2>
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
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_html)
        
        print(f"  ✅ 재생성 완료!")
        return True
        
    except Exception as e:
        print(f"  ❌ 오류: {e}")
        import traceback
        traceback.print_exc()
        return False

def rebuild_sub_file(filepath):
    """서브 파일 완전히 재생성 (2열 글 목록)"""
    print(f"Rebuilding: {filepath}")
    
    try:
        # 기존 파일에서 콘텐츠 추출
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 제목 추출
        title_match = re.search(r'<title>(.*?)</title>', content)
        title = title_match.group(1) if title_match else "9988 건강 연구소"
        
        # 페이지 제목 추출
        page_title_match = re.search(r'<h1 class="page-title">(.*?)</h1>', content)
        page_title = page_title_match.group(1) if page_title_match else "건강 정보"
        
        # 카테고리 링크 추출 (뒤로가기용)
        back_link_match = re.search(r'href="(category-[^"]+\.html)"', content)
        back_link = back_link_match.group(1) if back_link_match else "index-v2.html"
        
        # 글 목록 추출
        articles_match = re.search(r'<div class="content">(.*?)</div>\s*</div>', content, re.DOTALL)
        articles_html = articles_match.group(1) if articles_match else ""
        
        # 새로운 HTML 생성
        new_html = f'''<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <link rel="stylesheet" href="강력한-카테고리-스타일.css">
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
        
        /* 헤더 */
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
            position: relative;
        }}
        
        /* 뒤로가기 버튼 */
        .back-button {{
            position: absolute;
            left: 20px;
            background: rgba(255,255,255,0.2);
            color: white;
            width: 40px;
            height: 40px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            text-decoration: none;
            font-size: 24px;
            transition: all 0.3s;
            font-weight: bold;
        }}
        
        .back-button:hover {{
            background: rgba(255,255,255,0.3);
            transform: scale(1.1);
        }}
        
        .logo-container {{
            position: absolute;
            left: 50%;
            transform: translateX(-50%);
            display: flex;
            align-items: center;
            text-decoration: none;
            transition: transform 0.3s;
        }}
        
        .logo-container:hover {{
            transform: translateX(-50%) scale(1.05);
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
            margin-left: auto;
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
        
        @media (max-width: 768px) {{
            .header-content {{
                min-height: 70px;
            }}
            
            .back-button {{
                left: 10px;
                width: 36px;
                height: 36px;
                font-size: 20px;
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
        }}
    </style>
</head>
<body class="category archive">
    <header class="main-header">
        <div class="header-content">
            <a href="{back_link}" class="back-button">←</a>
            
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

    <div class="site-main">
        <header class="page-header">
            <h1 class="page-title">{page_title}</h1>
        </header>
        
        <div class="content">
{articles_html}        </div>
    </div>

    <script>
        document.getElementById('mobileMenuBtn').addEventListener('click', function() {{
            document.getElementById('mainNav').classList.toggle('active');
        }});
    </script>
</body>
</html>'''
        
        # 파일 저장
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_html)
        
        print(f"  ✅ 재생성 완료!")
        return True
        
    except Exception as e:
        print(f"  ❌ 오류: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("=" * 60)
    print("🔨 모든 HTML 파일 완전 재생성")
    print("=" * 60)
    
    # 카테고리 파일
    category_files = glob.glob("category-*.html")
    print(f"\n📁 카테고리 파일: {len(category_files)}개")
    
    success_count = 0
    for file in category_files:
        if rebuild_category_file(file):
            success_count += 1
    
    # 서브 파일
    sub_files = glob.glob("sub-*.html")
    print(f"\n📁 서브 페이지 파일: {len(sub_files)}개")
    
    for file in sub_files:
        if rebuild_sub_file(file):
            success_count += 1
    
    print("\n" + "=" * 60)
    print(f"✅ 완료: {success_count}/{len(category_files) + len(sub_files)}개 파일 재생성")
    print("=" * 60)

if __name__ == "__main__":
    main()

