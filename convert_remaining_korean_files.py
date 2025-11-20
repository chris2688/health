import os
import shutil
import re
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

print("=" * 70)
print("🔄 남은 한글 파일명 영문 변환")
print("=" * 70)

# 추가 파일명 매핑 (한글 → 영문)
ADDITIONAL_MAPPING = {
    # Food 카테고리
    'food-질환별식단.html': 'food-diet-guide.html',
    'food-피해야할과일.html': 'food-avoid-fruits.html',
    'food-모르면독이된다.html': 'food-warnings.html',
    
    # Exercise 카테고리
    'exercise-질환별운동가이드.html': 'exercise-guide.html',
    'exercise-운동팁.html': 'exercise-tips.html',
    
    # Lifestyle 카테고리
    'lifestyle-생활습관.html': 'lifestyle-habits.html',
    'lifestyle-생활습관바꾸기팁.html': 'lifestyle-tips.html',
}

# 1단계: 파일명 변경
print("\n📝 1단계: 파일명 변경 중...\n")
renamed_count = 0

for old_name, new_name in ADDITIONAL_MAPPING.items():
    if os.path.exists(old_name):
        try:
            shutil.copy2(old_name, new_name)
            print(f"✅ {old_name} → {new_name}")
            renamed_count += 1
        except Exception as e:
            print(f"❌ {old_name} - 오류: {e}")
    else:
        print(f"ℹ️  {old_name} - 파일 없음")

print(f"\n✅ {renamed_count}개 파일 복사 완료!")

# 2단계: 모든 HTML 파일에서 링크 업데이트
print("\n" + "=" * 70)
print("📝 2단계: 모든 파일의 링크 업데이트 중...")
print("=" * 70 + "\n")

updated_files = 0
html_files = [f for f in os.listdir('.') if f.endswith('.html') and not f.startswith('backup')]

for filename in html_files:
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 모든 한글 파일명을 영문으로 치환
        for old_name, new_name in ADDITIONAL_MAPPING.items():
            # href="..." 형태
            content = content.replace(f'href="{old_name}"', f'href="{new_name}"')
            # href='...' 형태
            content = content.replace(f"href='{old_name}'", f"href='{new_name}'")
        
        # 변경사항이 있으면 저장
        if content != original_content:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ {filename} - 링크 업데이트 완료")
            updated_files += 1
    
    except Exception as e:
        print(f"❌ {filename} - 오류: {e}")

print(f"\n✅ {updated_files}개 파일 링크 업데이트 완료!")

print("\n" + "=" * 70)
print("🎉 변환 완료!")
print("=" * 70)
print(f"\n📊 요약:")
print(f"   - 파일명 변경: {renamed_count}개")
print(f"   - 링크 업데이트: {updated_files}개")
print(f"\n영문 파일명:")
for old_name, new_name in ADDITIONAL_MAPPING.items():
    print(f"   ✅ {new_name}")
print("=" * 70)

