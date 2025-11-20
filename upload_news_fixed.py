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

def upload_news():
    """수정된 news-main.html 업로드"""
    print("=" * 70)
    print("📰 news-main.html 업로드")
    print("=" * 70)
    
    filename = 'news-main.html'
    
    if not os.path.exists(filename):
        print(f"\n❌ {filename} 파일이 없습니다.")
        return
    
    try:
        ftp = FTP(FTP_HOST)
        ftp.login(FTP_USER, FTP_PASSWORD)
        ftp.encoding = 'utf-8'
        print("\n✅ FTP 연결 성공\n")
        
        # 디렉토리 확인
        try:
            ftp.cwd('public_html')
        except:
            try:
                ftp.cwd('www')
            except:
                pass
        
        # 파일 업로드
        with open(filename, 'rb') as f:
            ftp.storbinary(f'STOR {filename}', f)
        
        size = os.path.getsize(filename) / 1024
        print(f"✅ {filename} ({size:.1f} KB) 업로드 완료!")
        
        ftp.quit()
        
        print("\n" + "=" * 70)
        print("🎉 업로드 완료!")
        print("=" * 70)
        print("\n🔗 테스트:")
        print("   https://health9988234.mycafe24.com/news-main.html")
        print("\n   또는 메인 페이지에서 '건강News' 클릭")
        print("   https://health9988234.mycafe24.com/index-v3.html")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n❌ 오류: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    upload_news()

