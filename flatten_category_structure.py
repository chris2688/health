import os
import re

# 모든 category 페이지의 HTML 구조 평탄화
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
        
        # 1. .health-card-container 열기 태그 제거
        content = re.sub(
            r'<div class="health-card-container">\s*\n',
            '',
            content
        )
        
        # 2. .health-card-container 닫기 태그 제거 (script 태그 바로 앞)
        # </div>를 찾되, 이것이 health-card-container를 닫는 것인지 확인
        content = re.sub(
            r'</div>\s*\n\s*</div>\s*\n\s*<script>',
            '</div>\n\n    <script>',
            content
        )
        
        # 3. .health-card-container CSS는 남겨두되, 주석 처리
        old_container_css = '''        .health-card-container {
            padding: 40px 20px 60px;
            min-height: calc(100vh - 80px);
        }'''
        
        new_container_css = '''        /* .health-card-container는 더 이상 사용되지 않음 */
        .health-card-container {
            padding: 40px 20px 60px;
            min-height: calc(100vh - 80px);
        }'''
        
        content = content.replace(old_container_css, new_container_css)
        
        # 4. section-title margin-top 추가
        content = content.replace(
            '        .section-title {',
            '        .section-title {\n            margin-top: 20px;'
        )
        
        # 파일 저장
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"[OK] {filename} - 구조 평탄화 완료")
        
    except Exception as e:
        print(f"[ERROR] {filename} 처리 중 오류: {str(e)}")

print("\n[완료] 모든 category 페이지 구조 평탄화 완료!")

