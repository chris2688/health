import os
import re

# 모든 category 페이지의 뒤로가기 버튼 위치 수정
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
        
        # 현재 구조:
        # <div class="site-main">
        #     <div class="health-card-container">
        #         <a href="..." class="back-button">뒤로가기</a>
        
        # 변경할 구조:
        # <div class="site-main">
        #     <a href="..." class="back-button">뒤로가기</a>
        #     <div class="health-card-container">
        
        # 뒤로가기 버튼 찾기 (health-card-container 안에 있는)
        pattern = r'(<div class="site-main">)\s*<div class="health-card-container">\s*(<a href="[^"]*" class="back-button">뒤로가기</a>)'
        
        # 뒤로가기 버튼을 site-main 바로 아래로 이동
        replacement = r'\1\n        \2\n        \n        <div class="health-card-container">'
        
        content = re.sub(pattern, replacement, content, flags=re.DOTALL)
        
        # 파일 저장
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"[OK] {filename} - 뒤로가기 버튼 위치 수정 완료")
        
    except Exception as e:
        print(f"[ERROR] {filename} 처리 중 오류: {str(e)}")

print("\n[완료] 모든 category 페이지 뒤로가기 버튼 위치 수정 완료!")

