import os
import shutil
import re
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

print("=" * 70)
print("🔄 전체 파일명 영문 변환 및 링크 업데이트")
print("=" * 70)

# 완전한 파일명 매핑 (한글 → 영문)
FILE_MAPPING = {
    # 메인 파일
    'index-v2.html': 'index-v2.html',  # 유지
    'index-v3.html': 'index-v3.html',  # 유지
    'intro.html': 'intro.html',  # 유지
    
    # 카테고리 파일
    'category-심혈관질환.html': 'category-cardiovascular.html',
    'category-당뇨병.html': 'category-diabetes.html',
    'category-관절근골격계.html': 'category-musculoskeletal.html',
    'category-소화기질환.html': 'category-digestive.html',
    'category-호르몬내분비.html': 'category-endocrine.html',
    'category-정신건강신경계.html': 'category-neuroscience.html',
    'category-안과치과기타.html': 'category-others.html',
    
    # 심혈관 질환 서브
    'sub-고혈압.html': 'sub-hypertension.html',
    'sub-고지혈증.html': 'sub-hyperlipidemia.html',
    'sub-협심증심근경색.html': 'sub-angina.html',
    'sub-동맥경화.html': 'sub-arteriosclerosis.html',
    'sub-뇌졸중.html': 'sub-stroke.html',
    
    # 당뇨병 서브
    'sub-당뇨.html': 'sub-diabetes.html',
    'sub-공복혈당장애.html': 'sub-fasting-glucose.html',
    'sub-당뇨병합병증.html': 'sub-diabetes-complications.html',
    
    # 관절/근골격계 서브
    'sub-퇴행성관절염.html': 'sub-degenerative-arthritis.html',
    'sub-허리디스크목디스크.html': 'sub-disc-herniation.html',
    'sub-골다공증.html': 'sub-osteoporosis.html',
    'sub-오십견.html': 'sub-frozen-shoulder.html',
    'sub-관절염.html': 'sub-arthritis.html',
    
    # 소화기 질환 서브
    'sub-위염위궤양.html': 'sub-gastritis.html',
    'sub-역류성식도염.html': 'sub-reflux-esophagitis.html',
    'sub-과민성대장증후군.html': 'sub-ibs.html',
    'sub-지방간.html': 'sub-fatty-liver.html',
    'sub-위염.html': 'sub-gastritis-simple.html',
    
    # 호르몬/내분비 서브
    'sub-갑상선.html': 'sub-thyroid.html',
    'sub-갱년기증후군.html': 'sub-menopause.html',
    'sub-대사증후군.html': 'sub-metabolic.html',
    'sub-갱년기.html': 'sub-menopause-simple.html',
    
    # 정신건강/신경계 서브
    'sub-우울증번아웃.html': 'sub-depression.html',
    'sub-수면장애불면증.html': 'sub-insomnia.html',
    'sub-치매경도인지장애.html': 'sub-dementia.html',
    'sub-이명어지럼증.html': 'sub-tinnitus.html',
    'sub-우울증.html': 'sub-depression-simple.html',
    'sub-수면장애.html': 'sub-sleep-disorder.html',
    'sub-치매.html': 'sub-dementia-simple.html',
    'sub-불안장애.html': 'sub-anxiety.html',
    
    # 안과/치과/기타 서브
    'sub-백내장녹내장.html': 'sub-cataract-glaucoma.html',
    'sub-치주염치아손실.html': 'sub-periodontal.html',
    'sub-비만체형변화.html': 'sub-obesity.html',
    'sub-백내장.html': 'sub-cataract.html',
    'sub-녹내장.html': 'sub-glaucoma.html',
    'sub-치주질환.html': 'sub-periodontal-simple.html',
    'sub-비만.html': 'sub-obesity-simple.html',
    
    # Main 페이지들
    'food-main.html': 'food-main.html',
    'exercise-main.html': 'exercise-main.html',
    'lifestyle-main.html': 'lifestyle-main.html',
    'news-main.html': 'news-main.html',
}

# 1단계: 모든 파일 복사 (영문명으로)
print("\n📝 1단계: 파일명 변경 중...\n")
renamed_count = 0

for old_name, new_name in FILE_MAPPING.items():
    if old_name == new_name:
        continue  # 이미 영문인 경우 스킵
    
    if os.path.exists(old_name):
        try:
            shutil.copy2(old_name, new_name)
            print(f"✅ {old_name} → {new_name}")
            renamed_count += 1
        except Exception as e:
            print(f"❌ {old_name} - 오류: {e}")

print(f"\n✅ {renamed_count}개 파일 복사 완료!")

# 2단계: 모든 영문 파일 내부의 링크 업데이트
print("\n" + "=" * 70)
print("📝 2단계: 파일 내부 링크 업데이트 중...")
print("=" * 70 + "\n")

updated_files = 0
english_files = list(set(FILE_MAPPING.values()))

for filename in english_files:
    if not os.path.exists(filename):
        continue
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 모든 한글 파일명을 영문으로 치환
        for old_name, new_name in FILE_MAPPING.items():
            if old_name != new_name:
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
print(f"\n다음 단계: FTP 업로드")
print("=" * 70)

