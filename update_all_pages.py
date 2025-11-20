import os
import glob
import re
import sys
import io

# UTF-8 인코딩 설정
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 공통 헤더 HTML
HEADER_HTML = '''<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{TITLE}</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, "Noto Sans KR", sans-serif;
            background: #f5f7fa;
            min-height: 100vh;
        }
        
        /* ========== 헤더 스타일 ========== */
        .main-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            box-shadow: 0 4px 20px rgba(102, 126, 234, 0.3);
            position: sticky;
            top: 0;
            z-index: 1000;
        }
        
        .header-content {
            max-width: 1400px;
            margin: 0 auto;
            padding: 0 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            min-height: 80px;
        }
        
        .logo-container {
            display: flex;
            align-items: center;
            gap: 15px;
            text-decoration: none;
            transition: transform 0.3s;
        }
        
        .logo-container:hover {
            transform: scale(1.05);
        }
        
        .logo-image {
            height: 50px;
            width: auto;
            border-radius: 8px;
            background: white;
            padding: 5px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        
        .main-nav {
            display: flex;
            gap: 0;
        }
        
        .nav-item {
            padding: 10px 24px;
            color: white;
            text-decoration: none;
            font-weight: 600;
            font-size: 16px;
            transition: all 0.3s;
            position: relative;
            border-radius: 8px;
        }
        
        .nav-item::before {
            content: '';
            position: absolute;
            bottom: 0;
            left: 50%;
            width: 0;
            height: 3px;
            background: white;
            transform: translateX(-50%);
            transition: width 0.3s;
        }
        
        .nav-item:hover {
            background: rgba(255,255,255,0.15);
        }
        
        .nav-item:hover::before {
            width: 60%;
        }
        
        .mobile-menu-btn {
            display: none;
            background: none;
            border: none;
            color: white;
            font-size: 28px;
            cursor: pointer;
            padding: 10px;
        }
        
        /* ========== 기존 스타일 유지 ========== */
        .health-card-container {
            padding: 60px 20px;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            min-height: 100vh;
        }
        
        .section-title {
            text-align: center;
            margin-bottom: 50px;
        }
        
        .back-link {
            display: inline-block;
            margin-bottom: 25px;
            padding: 12px 28px;
            background: rgba(255,255,255,0.95);
            border-radius: 50px;
            text-decoration: none;
            color: #667eea;
            font-weight: 600;
            font-size: 15px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            transition: all 0.3s;
        }
        
        .back-link:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(0,0,0,0.15);
            background: #ffffff;
        }
        
        .main-icon {
            font-size: 72px;
            margin-bottom: 15px;
            filter: drop-shadow(0 4px 8px rgba(0,0,0,0.1));
        }
        
        .section-title h2 {
            font-size: 42px;
            font-weight: 800;
            background: linear-gradient(135deg, var(--title-color-1, #667eea) 0%, var(--title-color-2, #764ba2) 100%);
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
        
        .health-cards-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 30px;
            max-width: 1200px;
            margin: 0 auto;
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
        
        .health-card::before {
            content: '';
            position: absolute;
            top: 0;
            right: 0;
            width: 120px;
            height: 120px;
            background: rgba(255,255,255,0.1);
            border-radius: 50%;
            transform: translate(40%, -40%);
        }
        
        .health-card-icon {
            font-size: 56px;
            margin-bottom: 15px;
            filter: drop-shadow(0 2px 4px rgba(0,0,0,0.2));
            position: relative;
            z-index: 1;
        }
        
        .health-card h3 {
            font-size: 22px;
            font-weight: 700;
            color: #ffffff;
            margin: 0;
            text-shadow: 0 2px 4px rgba(0,0,0,0.1);
            position: relative;
            z-index: 1;
        }
        
        @media (max-width: 768px) {
            .header-content {
                min-height: 70px;
            }
            
            .logo-image {
                height: 40px;
            }
            
            .main-nav {
                display: none;
                position: absolute;
                top: 100%;
                left: 0;
                right: 0;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                flex-direction: column;
                padding: 20px;
                box-shadow: 0 4px 20px rgba(0,0,0,0.2);
            }
            
            .main-nav.active {
                display: flex;
            }
            
            .nav-item {
                padding: 15px 20px;
                text-align: center;
            }
            
            .mobile-menu-btn {
                display: block;
            }
            
            .health-cards-grid {
                grid-template-columns: 1fr;
                gap: 20px;
            }
            
            .section-title h2 {
                font-size: 32px;
            }
            
            .main-icon {
                font-size: 56px;
            }
        }
    </style>
</head>
<body>
    <!-- 헤더 -->
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

    {CONTENT}

    <script>
        document.getElementById('mobileMenuBtn').addEventListener('click', function() {
            document.getElementById('mainNav').classList.toggle('active');
        });
    </script>
</body>
</html>'''

def update_html_file(filepath):
    """HTML 파일 업데이트"""
    print(f"Processing: {filepath}")
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 제목 추출
        title_match = re.search(r'<title>(.*?)</title>', content)
        title = title_match.group(1) if title_match else "9988 건강 연구소"
        
        # body 내용 추출 (class 속성 포함)
        body_match = re.search(r'<body[^>]*>(.*?)</body>', content, re.DOTALL)
        if not body_match:
            print(f"  ❌ body 태그를 찾을 수 없습니다")
            return False
        
        body_content = body_match.group(1).strip()
        
        # 뒤로가기 링크 수정 (index.html -> index-v2.html)
        body_content = body_content.replace('href="index.html"', 'href="index-v2.html"')
        
        # 새로운 HTML 생성
        new_html = HEADER_HTML.replace('{TITLE}', title).replace('{CONTENT}', body_content)
        
        # 파일 저장
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_html)
        
        print(f"  ✅ 업데이트 완료!")
        return True
        
    except Exception as e:
        print(f"  ❌ 오류: {e}")
        return False

def main():
    print("=" * 60)
    print("🔄 모든 HTML 파일에 새 헤더 적용")
    print("=" * 60)
    
    # category-*.html 파일 처리
    category_files = glob.glob("category-*.html")
    print(f"\n📁 카테고리 파일: {len(category_files)}개")
    
    success_count = 0
    for file in category_files:
        if update_html_file(file):
            success_count += 1
    
    # sub-*.html 파일 처리
    sub_files = glob.glob("sub-*.html")
    print(f"\n📁 서브 페이지 파일: {len(sub_files)}개")
    
    for file in sub_files:
        if update_html_file(file):
            success_count += 1
    
    print("\n" + "=" * 60)
    print(f"✅ 완료: {success_count}/{len(category_files) + len(sub_files)}개 파일 업데이트")
    print("=" * 60)

if __name__ == "__main__":
    main()

