import ftplib
import os

# FTP 연결 정보
FTP_HOST = 'health9988234.mycafe24.com'
FTP_USER = 'health9988234'
FTP_PASS = 'ssurlf7904!'

print("=" * 60)
print("워드프레스 서버에서 모든 HTML 파일 다운로드")
print("=" * 60)

# 알려진 파일 목록 (서버에 있을 것으로 예상되는 파일들)
known_files = [
    'index-v3.html', 'index-v2.html', 'index.html',
    'category-cardiovascular.html', 'category-diabetes.html',
    'category-musculoskeletal.html', 'category-endocrine.html',
    'category-neuroscience.html', 'category-digestive.html',
    'category-others.html',
    'food-main.html', 'food-diet-guide.html', 'food-avoid-fruits.html', 'food-warnings.html',
    'exercise-main.html', 'exercise-guide.html', 'exercise-tips.html',
    'lifestyle-main.html', 'lifestyle-habits.html', 'lifestyle-tips.html',
    'news-main.html',
    'sub-hypertension.html', 'sub-diabetes.html', 'sub-osteoporosis.html',
    'sub-angina.html', 'sub-stroke.html', 'sub-hyperlipidemia.html',
    'sub-arteriosclerosis.html', 'sub-fasting-glucose.html', 'sub-diabetes-complications.html',
    'sub-disc-herniation.html', 'sub-degenerative-arthritis.html', 'sub-frozen-shoulder.html',
    'sub-arthritis.html', 'sub-menopause.html', 'sub-thyroid.html', 'sub-metabolic.html',
    'sub-depression.html', 'sub-dementia.html', 'sub-sleep-disorder.html', 'sub-anxiety.html',
    'sub-gastritis.html', 'sub-fatty-liver.html', 'sub-reflux-esophagitis.html', 'sub-ibs.html',
    'sub-cataract.html', 'sub-glaucoma.html', 'sub-periodontal.html', 'sub-tinnitus.html',
    # 한글 파일명도 추가
    'category-심혈관질환.html', 'category-당뇨병.html', 'category-관절근골격계.html',
    'category-호르몬내분비.html', 'category-정신건강신경계.html', 'category-소화기질환.html',
    'category-안과치과기타.html',
    'food-질환별식단.html', 'food-피해야할과일.html', 'food-모르면독이된다.html',
    'exercise-질환별운동가이드.html', 'exercise-운동팁.html',
    'lifestyle-생활습관.html', 'lifestyle-생활습관바꾸기팁.html',
    'sub-고혈압.html', 'sub-당뇨.html', 'sub-골다공증.html', 'sub-협심증.html',
    'sub-뇌졸중.html', 'sub-고지혈증.html', 'sub-동맥경화.html', 'sub-공복혈당.html',
    'sub-당뇨합병증.html', 'sub-허리디스크.html', 'sub-퇴행성관절염.html', 'sub-오십견.html',
    'sub-류마티스관절염.html', 'sub-갱년기.html', 'sub-갑상선.html', 'sub-대사증후군.html',
    'sub-우울증.html', 'sub-치매.html', 'sub-수면장애.html', 'sub-불안장애.html',
    'sub-위염.html', 'sub-지방간.html', 'sub-역류성식도염.html', 'sub-과민성대장증후군.html',
    'sub-백내장.html', 'sub-녹내장.html', 'sub-치주질환.html', 'sub-이명.html'
]

try:
    # FTP 연결
    ftp = ftplib.FTP(FTP_HOST)
    ftp.login(FTP_USER, FTP_PASS)
    
    print("\nFTP 연결 성공!")
    
    print(f"\n총 {len(known_files)}개 파일 다운로드 시도...\n")
    
    downloaded_count = 0
    error_count = 0
    
    for filename in known_files:
        try:
            # 바이너리 모드로 전환
            ftp.voidcmd('TYPE I')
            
            # 바이너리 모드로 다운로드
            with open(filename, 'wb') as f:
                ftp.retrbinary(f'RETR {filename}', f.write)
            
            downloaded_count += 1
            if downloaded_count <= 50:  # 처음 50개만 출력
                print(f"[OK] {filename}")
            elif downloaded_count == 51:
                print("...")
            
        except ftplib.error_perm as e:
            # 파일이 없거나 접근 불가
            error_count += 1
            if error_count <= 20:  # 처음 20개 에러만 출력
                print(f"[SKIP] {filename} - 파일 없음")
        except Exception as e:
            error_count += 1
            if error_count <= 20:
                print(f"[ERROR] {filename}: {str(e)}")
    
    if downloaded_count > 50:
        print(f"\n... 외 {downloaded_count - 50}개 파일 다운로드됨")
    
    ftp.quit()
    
    print(f"\n완료: {downloaded_count}개 다운로드, {error_count}개 실패/없음")
    
except Exception as e:
    print(f"\n[ERROR] FTP 연결 실패: {str(e)}")
    import traceback
    traceback.print_exc()
