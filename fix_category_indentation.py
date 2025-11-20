import os
import re

# 모든 category 페이지의 들여쓰기 정리
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
        
        # section-title의 들여쓰기 수정
        content = re.sub(
            r'\s+<div class="section-title">',
            '\n        <div class="section-title">',
            content
        )
        
        # health-cards-grid의 들여쓰기도 수정
        content = re.sub(
            r'</div>\s+<div class="health-cards-grid">',
            '</div>\n\n        <div class="health-cards-grid">',
            content
        )
        
        # 파일 저장
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"[OK] {filename} - 들여쓰기 정리 완료")
        
    except Exception as e:
        print(f"[ERROR] {filename} 처리 중 오류: {str(e)}")

print("\n[완료] 모든 category 페이지 들여쓰기 정리 완료!")

