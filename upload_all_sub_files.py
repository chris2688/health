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

def upload_sub_files():
    """모든 sub-*.html 파일 업로드"""
    print("=" * 60)
    print("📤 sub-*.html 파일 업로드 시작")
    print("=" * 60)
    
    # 업로드할 파일 목록
    sub_files = [f for f in os.listdir('.') if f.startswith('sub-') and f.endswith('.html')]
    
    print(f"\n📝 총 {len(sub_files)}개 파일 업로드 예정\n")
    
    try:
        # FTP 연결
        print("🔌 FTP 서버 연결 중...")
        ftp = FTP(FTP_HOST)
        ftp.login(FTP_USER, FTP_PASSWORD)
        ftp.encoding = 'utf-8'
        print("   ✅ FTP 연결 성공\n")
        
        # 디렉토리 찾기
        try:
            ftp.cwd('public_html')
            print("   📁 작업 디렉토리: public_html\n")
        except:
            try:
                ftp.cwd('www')
                print("   📁 작업 디렉토리: www\n")
            except:
                print("   📁 작업 디렉토리: root\n")
        
        # 바이너리 모드 설정
        ftp.voidcmd('TYPE I')
        
        # 파일 업로드
        success_count = 0
        for filename in sub_files:
            try:
                with open(filename, 'rb') as f:
                    ftp.storbinary(f'STOR {filename}', f)
                print(f"   ✅ {filename}")
                success_count += 1
            except Exception as e:
                print(f"   ❌ {filename} - 오류: {e}")
        
        ftp.quit()
        
        print(f"\n✅ 총 {success_count}/{len(sub_files)}개 파일 업로드 완료!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ FTP 오류: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    upload_sub_files()

