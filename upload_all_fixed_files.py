import os
from ftplib import FTP
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# FTP 설정
FTP_HOST = "health9988234.mycafe24.com"
FTP_USER = "health9988234"
FTP_PASSWORD = "ssurlf7904!"

def upload_all_files():
    """뒤로가기 버튼이 수정된 모든 파일 업로드"""
    print("=" * 70)
    print("🚀 수정된 모든 파일 FTP 업로드")
    print("=" * 70)
    
    # 업로드할 파일 목록 (영문 파일만)
    files_to_upload = [
        # 메인 파일
        'index-v3.html',
        'index-v2.html',
        
        # 카테고리 파일
        'category-cardiovascular.html',
        'category-diabetes.html',
        'category-musculoskeletal.html',
        'category-digestive.html',
        'category-endocrine.html',
        'category-neuroscience.html',
        'category-others.html',
        
        # Sub 페이지 (심혈관)
        'sub-hypertension.html',
        'sub-hyperlipidemia.html',
        'sub-angina.html',
        'sub-arteriosclerosis.html',
        'sub-stroke.html',
        
        # Sub 페이지 (당뇨병)
        'sub-diabetes.html',
        'sub-fasting-glucose.html',
        'sub-diabetes-complications.html',
        
        # Sub 페이지 (관절/근골격계)
        'sub-degenerative-arthritis.html',
        'sub-disc-herniation.html',
        'sub-osteoporosis.html',
        'sub-frozen-shoulder.html',
        'sub-arthritis.html',
        
        # Sub 페이지 (소화기)
        'sub-gastritis.html',
        'sub-reflux-esophagitis.html',
        'sub-ibs.html',
        'sub-fatty-liver.html',
        'sub-gastritis-simple.html',
        
        # Sub 페이지 (호르몬/내분비)
        'sub-thyroid.html',
        'sub-menopause.html',
        'sub-metabolic.html',
        'sub-menopause-simple.html',
        
        # Sub 페이지 (정신건강/신경계)
        'sub-depression.html',
        'sub-insomnia.html',
        'sub-dementia.html',
        'sub-tinnitus.html',
        'sub-depression-simple.html',
        'sub-sleep-disorder.html',
        'sub-dementia-simple.html',
        'sub-anxiety.html',
        
        # Sub 페이지 (안과/치과/기타)
        'sub-cataract-glaucoma.html',
        'sub-periodontal.html',
        'sub-obesity.html',
        'sub-cataract.html',
        'sub-glaucoma.html',
        'sub-periodontal-simple.html',
        'sub-obesity-simple.html',
        
        # Main 페이지들
        'food-main.html',
        'exercise-main.html',
        'lifestyle-main.html',
        'news-main.html',
        
        # Food 페이지들
        'food-diet-guide.html',
        'food-avoid-fruits.html',
        'food-warnings.html',
        
        # Exercise 페이지들
        'exercise-guide.html',
        'exercise-tips.html',
        
        # Lifestyle 페이지들
        'lifestyle-habits.html',
        'lifestyle-tips.html',
    ]
    
    print(f"\n📝 총 {len(files_to_upload)}개 파일 업로드 예정\n")
    
    try:
        ftp = FTP(FTP_HOST)
        ftp.login(FTP_USER, FTP_PASSWORD)
        ftp.encoding = 'utf-8'
        print("✅ FTP 연결 성공\n")
        
        # 디렉토리 확인
        try:
            ftp.cwd('public_html')
        except:
            try:
                ftp.cwd('www')
            except:
                pass
        
        success_count = 0
        failed_files = []
        
        for filename in files_to_upload:
            if not os.path.exists(filename):
                print(f"⚠️  {filename} - 로컬 파일 없음")
                continue
            
            try:
                with open(filename, 'rb') as f:
                    ftp.storbinary(f'STOR {filename}', f)
                
                size = os.path.getsize(filename) / 1024
                
                if filename.startswith('index-'):
                    print(f"⭐ {filename} ({size:.1f} KB)")
                elif filename.startswith('category-'):
                    print(f"📂 {filename} ({size:.1f} KB)")
                elif filename.startswith('sub-'):
                    print(f"📄 {filename} ({size:.1f} KB)")
                elif 'main' in filename:
                    print(f"🏠 {filename} ({size:.1f} KB)")
                else:
                    print(f"✅ {filename} ({size:.1f} KB)")
                
                success_count += 1
            except Exception as e:
                print(f"❌ {filename} - {e}")
                failed_files.append(filename)
        
        ftp.quit()
        
        print(f"\n✅ 총 {success_count}/{len(files_to_upload)}개 파일 업로드 완료!")
        
        if failed_files:
            print(f"\n❌ 실패한 파일 ({len(failed_files)}개):")
            for f in failed_files:
                print(f"   - {f}")
        
        print("\n" + "=" * 70)
        print("🎉 전체 사이트 업로드 완료!")
        print("=" * 70)
        print("\n✅ 뒤로가기 버튼이 모든 페이지에 통일되었습니다!")
        print("\n🔗 테스트 URL:")
        print("   메인: https://health9988234.mycafe24.com/index-v3.html")
        print("   건강News: https://health9988234.mycafe24.com/news-main.html")
        print("   운동가이드: https://health9988234.mycafe24.com/exercise-guide.html")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n❌ FTP 오류: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    upload_all_files()
