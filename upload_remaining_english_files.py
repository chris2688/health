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

def upload_files():
    """새로운 영문 파일들 및 news-main.html 업로드"""
    print("=" * 70)
    print("🚀 영문 파일 업로드")
    print("=" * 70)
    
    # 업로드할 파일 목록
    files_to_upload = [
        # 새로운 영문 파일들
        'food-diet-guide.html',
        'food-avoid-fruits.html',
        'food-warnings.html',
        'exercise-guide.html',
        'exercise-tips.html',
        'lifestyle-habits.html',
        'lifestyle-tips.html',
        
        # Main 페이지들 (링크가 업데이트됨)
        'food-main.html',
        'exercise-main.html',
        'lifestyle-main.html',
        'news-main.html',  # 이것도 재업로드
        
        # 메인 페이지들
        'index-v3.html',
        'index-v2.html',
    ]
    
    print(f"\n📝 총 {len(files_to_upload)}개 파일 업로드\n")
    
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
        
        for filename in files_to_upload:
            if not os.path.exists(filename):
                print(f"⚠️  {filename} - 로컬 파일 없음")
                continue
            
            try:
                with open(filename, 'rb') as f:
                    ftp.storbinary(f'STOR {filename}', f)
                
                size = os.path.getsize(filename) / 1024
                
                if 'news' in filename:
                    print(f"📰 {filename} ({size:.1f} KB)")
                elif filename.startswith('food-'):
                    print(f"🍽️  {filename} ({size:.1f} KB)")
                elif filename.startswith('exercise-'):
                    print(f"🏃 {filename} ({size:.1f} KB)")
                elif filename.startswith('lifestyle-'):
                    print(f"🌱 {filename} ({size:.1f} KB)")
                else:
                    print(f"✅ {filename} ({size:.1f} KB)")
                
                success_count += 1
            except Exception as e:
                print(f"❌ {filename} - {e}")
        
        ftp.quit()
        
        print(f"\n✅ {success_count}/{len(files_to_upload)}개 파일 업로드 완료!")
        
        print("\n" + "=" * 70)
        print("🎉 업로드 완료!")
        print("=" * 70)
        print("\n🔗 테스트 URL:")
        print("   건강News: https://health9988234.mycafe24.com/news-main.html")
        print("   식단/음식: https://health9988234.mycafe24.com/food-main.html")
        print("   운동/활동: https://health9988234.mycafe24.com/exercise-main.html")
        print("   생활습관: https://health9988234.mycafe24.com/lifestyle-main.html")
        print("\n새로운 영문 페이지:")
        print("   https://health9988234.mycafe24.com/food-diet-guide.html")
        print("   https://health9988234.mycafe24.com/exercise-guide.html")
        print("   https://health9988234.mycafe24.com/lifestyle-habits.html")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n❌ 오류: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    upload_files()

