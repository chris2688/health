import sys
import io
import os
from ftplib import FTP

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# FTP 정보
FTP_HOST = "health9988234.mycafe24.com"
FTP_USER = "health9988234"
FTP_PASS = "ssurlf7904!"
FTP_PORT = 21

FILE_TO_UPLOAD = "index-v2.html"


def main():
    """메인 실행"""
    print("=" * 60)
    print("📤 index-v2.html 업로드")
    print("=" * 60)
    
    if not os.path.exists(FILE_TO_UPLOAD):
        print(f"\n❌ 파일이 없습니다: {FILE_TO_UPLOAD}")
        return
    
    file_size = os.path.getsize(FILE_TO_UPLOAD)
    print(f"\n📋 업로드할 파일: {FILE_TO_UPLOAD} ({file_size:,} bytes)")
    
    try:
        print(f"\n🔗 FTP 서버 연결 중...")
        ftp = FTP()
        ftp.encoding = 'utf-8'
        ftp.connect(FTP_HOST, FTP_PORT, timeout=10)
        print("✅ 연결 성공!")
        
        print(f"🔐 로그인 중...")
        ftp.login(FTP_USER, FTP_PASS)
        print("✅ 로그인 성공!")
        
        print(f"\n📤 파일 업로드 중...")
        with open(FILE_TO_UPLOAD, "rb") as f:
            ftp.storbinary(f"STOR {FILE_TO_UPLOAD}", f)
        print(f"✅ 업로드 완료!")
        
        ftp.quit()
        
        print(f"\n" + "=" * 60)
        print(f"✅ 업로드 완료!")
        print("=" * 60)
            
    except Exception as e:
        print(f"\n❌ FTP 업로드 오류: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

