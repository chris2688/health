import os

# 모든 category 페이지의 뒤로가기 버튼 왼쪽 여백 수정
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
        
        # 1. .site-main CSS에 padding-top 추가 및 확실하게 적용
        old_site_main = '''        .site-main {
            max-width: 1400px;
            margin: 0 auto;
            padding: 0 20px;
        }'''
        
        new_site_main = '''        .site-main {
            max-width: 1400px;
            margin: 0 auto;
            padding: 40px 20px 20px 20px;
        }'''
        
        content = content.replace(old_site_main, new_site_main)
        
        # 2. .back-button CSS 들여쓰기 수정
        content = content.replace(
            '                .back-button {',
            '        .back-button {'
        )
        
        # 파일 저장
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"[OK] {filename} - 여백 수정 완료")
        
    except Exception as e:
        print(f"[ERROR] {filename} 처리 중 오류: {str(e)}")

print("\n[완료] 모든 category 페이지 여백 수정 완료!")

