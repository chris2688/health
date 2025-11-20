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

def upload_htaccess():
    """'.htaccess' 파일 업로드"""
    print("=" * 70)
    print("🔄 .htaccess 파일 업로드")
    print("=" * 70)
    
    filename = '.htaccess'
    
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
            print("📁 작업 디렉토리: public_html\n")
        except:
            try:
                ftp.cwd('www')
                print("📁 작업 디렉토리: www\n")
            except:
                print("📁 작업 디렉토리: root\n")
        
        # 파일 업로드
        with open(filename, 'rb') as f:
            ftp.storbinary(f'STOR {filename}', f)
        
        size = os.path.getsize(filename) / 1024
        print(f"✅ {filename} ({size:.2f} KB) 업로드 완료!")
        
        ftp.quit()
        
        print("\n" + "=" * 70)
        print("🎉 .htaccess 업로드 완료!")
        print("=" * 70)
        print("\n변경사항:")
        print("  ✅ 메인 도메인(/) → index-v3.html")
        print("  ✅ index-v2.html 접근 시 → index-v3.html로 301 리디렉션")
        print("\n테스트:")
        print("  1. https://health9988234.mycafe24.com/")
        print("  2. https://health9988234.mycafe24.com/index-v2.html")
        print("  → 모두 index-v3.html로 이동!")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n❌ 오류: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    upload_htaccess()
