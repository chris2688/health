import os

# 모든 category 페이지의 margin-top 제거
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
        
        # .section-title의 margin-top 제거
        old_css = '''        .section-title {
            margin-top: 20px;
            text-align: center;
            margin-bottom: 30px;
        }'''
        
        new_css = '''        .section-title {
            text-align: center;
            margin-bottom: 30px;
        }'''
        
        content = content.replace(old_css, new_css)
        
        # 파일 저장
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"[OK] {filename} - margin 수정 완료")
        
    except Exception as e:
        print(f"[ERROR] {filename} 처리 중 오류: {str(e)}")

print("\n[완료] 모든 category 페이지 margin 수정 완료!")

