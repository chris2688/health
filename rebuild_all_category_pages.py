import os

# 모든 category 페이지의 뒤로가기 버튼 스타일 수정
category_files = [
    'category-cardiovascular.html',
    'category-diabetes.html',
    'category-musculoskeletal.html',
    'category-digestive.html',
    'category-endocrine.html',
    'category-neuroscience.html',
    'category-others.html'
]

for filename in category_files:
    if not os.path.exists(filename):
        print(f"[경고] 파일을 찾을 수 없습니다: {filename}")
        continue
        
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # HTML 구조 수정: health-card-container 앞에 site-main 추가
        if '<div class="health-card-container">' in content and '<div class="site-main">' not in content:
            # CSS에 site-main 스타일 추가
            if '.site-main {' not in content:
                site_main_css = '''        
        .site-main {
            max-width: 1400px;
            margin: 0 auto;
            padding: 0 20px;
        }
                
        '''
                # back-button CSS 바로 앞에 추가
                content = content.replace('        .back-button {', site_main_css + '        .back-button {')
            
            # HTML 구조 변경: <div class="health-card-container"> 앞에 <div class="site-main"> 추가
            # 그리고 container-content 제거
            content = content.replace(
                '    <div class="health-card-container">\n        <div class="container-content">',
                '    <div class="site-main">\n        <div class="health-card-container">'
            )
            
            # 닫는 태그도 수정 (역순)
            # </div>\n    </div> (container-content + health-card-container) 를
            # </div>\n    </div> (health-card-container + site-main) 로 변경
            # 마지막 두 개의 닫는 div 찾기
            last_divs = content.rfind('        </div>\n    </div>\n\n    <script>')
            if last_divs != -1:
                content = content[:last_divs] + '    </div>\n    </div>\n\n    <script>' + content[last_divs+len('        </div>\n    </div>\n\n    <script>'):]
        
        # 파일 저장
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"[OK] {filename} - 구조 수정 완료")
        
    except Exception as e:
        print(f"[ERROR] {filename} 처리 중 오류: {str(e)}")

print("\n[완료] 모든 category 페이지 구조 수정 완료!")

