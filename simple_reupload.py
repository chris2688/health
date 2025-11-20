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

def simple_upload():
    """단순 재업로드"""
    print("=" * 60)
    print("📤 파일 재업로드")
    print("=" * 60)
    
    files = [
        'sub-골다공증.html',
        'category-호르몬내분비.html',
        'category-관절근골격계.html',
        'news-main.html',
    ]
    
    try:
        ftp = FTP(FTP_HOST)
        ftp.login(FTP_USER, FTP_PASSWORD)
        ftp.encoding = 'utf-8'
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
                print(f"❌ {filename} - 로컬 파일 없음")
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
        
    except Exception as e:
        print(f"❌ 오류: {e}")

if __name__ == "__main__":
    simple_upload()

