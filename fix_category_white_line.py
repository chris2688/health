import os
import re

# 모든 category 페이지의 CSS 수정
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
        
        # body에 배경 그라디언트 추가
        old_body_css = '''        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, "Noto Sans KR", sans-serif;
            background: #f5f7fa;
            min-height: 100vh;
        }'''
        
        new_body_css = '''        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, "Noto Sans KR", sans-serif;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            min-height: 100vh;
        }'''
        
        content = content.replace(old_body_css, new_body_css)
        
        # .health-card-container의 배경 제거
        old_container_css = '''        .health-card-container {
            padding: 20px 0 0 0;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            min-height: calc(100vh - 80px);
        }'''
        
        new_container_css = '''        .health-card-container {
            padding: 40px 20px 60px;
            min-height: calc(100vh - 80px);
        }'''
        
        content = content.replace(old_container_css, new_container_css)
        
        # 파일 저장
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"[OK] {filename} - CSS 수정 완료")
        
    except Exception as e:
        print(f"[ERROR] {filename} 처리 중 오류: {str(e)}")

print("\n[완료] 모든 category 페이지 CSS 수정 완료!")

