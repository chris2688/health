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

def upload_english_files():
    """영문 파일명으로 업로드"""
    print("=" * 60)
    print("📤 영문 파일명 업로드")
    print("=" * 60)
    
    files = [
        'category-cardiovascular.html',
        'category-diabetes.html',
        'category-musculoskeletal.html',
        'category-digestive.html',
        'category-endocrine.html',
        'category-neuroscience.html',
        'category-others.html',
        'sub-osteoporosis.html',
        'sub-thyroid.html',
        'sub-menopause.html',
        'sub-metabolic.html',
    ]
    
    try:
        ftp = FTP(FTP_HOST)
        ftp.login(FTP_USER, FTP_PASSWORD)
        print("\n✅ FTP 연결 성공\n")
        
        # 디렉토리 이동
        try:
            ftp.cwd('public_html')
        except:
            try:
                ftp.cwd('www')
            except:
                pass
        
        success = 0
        for filename in files:
            if not os.path.exists(filename):
                print(f"⚠️  {filename} - 로컬 파일 없음")
                continue
            
            try:
                with open(filename, 'rb') as f:
                    ftp.storbinary(f'STOR {filename}', f)
                size = os.path.getsize(filename) / 1024
                print(f"✅ {filename} ({size:.1f} KB)")
                success += 1
            except Exception as e:
                print(f"❌ {filename} - {e}")
        
        ftp.quit()
        print(f"\n✅ {success}/{len(files)}개 파일 업로드 완료")
        
        print("\n" + "=" * 60)
        print("🔗 테스트 URL (영문 파일명):")
        print("=" * 60)
        print("   골다공증: https://health9988234.mycafe24.com/sub-osteoporosis.html")
        print("   호르몬/내분비: https://health9988234.mycafe24.com/category-endocrine.html")
        print("   관절/근골격계: https://health9988234.mycafe24.com/category-musculoskeletal.html")
        print("=" * 60)
        
    except Exception as e:
        print(f"❌ 오류: {e}")

if __name__ == "__main__":
    upload_english_files()

