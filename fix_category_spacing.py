import os
import re

# 모든 category 페이지의 spacing 수정
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
        
        # 뒤로가기 버튼 뒤에 빈 줄 추가 및 들여쓰기 수정
        # 현재: <a ... class="back-button">뒤로가기</a>\n        <div class="section-title">
        # 변경: <a ... class="back-button">뒤로가기</a>\n        \n        <div class="section-title">
        
        content = re.sub(
            r'(<a href="[^"]*" class="back-button">뒤로가기</a>)\s*<div class="section-title">',
            r'\1\n        \n        <div class="section-title">',
            content
        )
        
        # section-title 내부 들여쓰기 수정
        content = re.sub(
            r'<div class="section-title">\s*<div class="main-icon">',
            '<div class="section-title">\n            <div class="main-icon">',
            content
        )
        
        content = re.sub(
            r'</div>\s*<h2>',
            '</div>\n            <h2>',
            content
        )
        
        content = re.sub(
            r'</h2>\s*<p class="subtitle">',
            '</h2>\n            <p class="subtitle">',
            content
        )
        
        content = re.sub(
            r'</p>\s*</div>\s*<div class="health-cards-grid">',
            '</p>\n        </div>\n\n        <div class="health-cards-grid">',
            content
        )
        
        # 파일 저장
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"[OK] {filename} - spacing 수정 완료")
        
    except Exception as e:
        print(f"[ERROR] {filename} 처리 중 오류: {str(e)}")

print("\n[완료] 모든 category 페이지 spacing 수정 완료!")

