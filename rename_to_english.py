import os
import shutil
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

print("=" * 60)
print("🔄 한글 파일명을 영문으로 변경")
print("=" * 60)

# 파일명 매핑 (한글 → 영문)
rename_mapping = {
    # 카테고리 파일
    'category-심혈관질환.html': 'category-cardiovascular.html',
    'category-당뇨병.html': 'category-diabetes.html',
    'category-관절근골격계.html': 'category-musculoskeletal.html',
    'category-소화기질환.html': 'category-digestive.html',
    'category-호르몬내분비.html': 'category-endocrine.html',
    'category-정신건강신경계.html': 'category-neuroscience.html',
    'category-안과치과기타.html': 'category-others.html',
    
    # 서브 파일 (문제 파일 우선)
    'sub-골다공증.html': 'sub-osteoporosis.html',
    'sub-갑상선.html': 'sub-thyroid.html',
    'sub-갱년기증후군.html': 'sub-menopause.html',
    'sub-대사증후군.html': 'sub-metabolic.html',
}

print("\n📝 파일명 변경 중...\n")

renamed_count = 0
for old_name, new_name in rename_mapping.items():
    if os.path.exists(old_name):
        try:
            shutil.copy2(old_name, new_name)
            print(f"✅ {old_name}")
            print(f"   → {new_name}\n")
            renamed_count += 1
        except Exception as e:
            print(f"❌ {old_name} - 오류: {e}\n")
    else:
        print(f"⚠️  {old_name} - 파일 없음\n")

print(f"✅ 총 {renamed_count}개 파일 변경 완료!")
print("=" * 60)

