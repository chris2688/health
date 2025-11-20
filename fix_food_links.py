import os

print("=" * 60)
print("식단 서브 카테고리 링크 수정")
print("=" * 60)

# 파일명 매핑
file_mapping = {
    'food-diet-guide.html': 'food-질환별식단.html',
    'food-avoid-fruits.html': 'food-피해야할과일.html',
    'food-warnings.html': 'food-모르면독이된다.html'
}

# food-main.html 수정
filename = 'food-main.html'
if os.path.exists(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # 영문 파일명을 한글 파일명으로 변경
    for eng_name, kor_name in file_mapping.items():
        if os.path.exists(kor_name):
            # href 속성만 변경
            content = content.replace(f'href="{eng_name}"', f'href="{kor_name}"')
            print(f"[OK] {eng_name} -> {kor_name}")
        else:
            print(f"[WARN] {kor_name} 파일이 없습니다")
    
    if content != original_content:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"\n[OK] {filename} 수정 완료")
    else:
        print(f"\n[SKIP] {filename} - 변경사항 없음")
else:
    print(f"[ERROR] {filename} 파일이 없습니다")

print("\n완료!")

