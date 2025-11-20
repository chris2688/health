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

def check_files():
    """서버에 파일이 실제로 있는지 확인"""
    print("=" * 60)
    print("🔍 서버 파일 확인")
    print("=" * 60)
    
    check_files = [
        'sub-골다공증.html',
        'category-호르몬내분비.html',
        'category-관절근골격계.html',
        'news-main.html',
    ]
    
    try:
        ftp = FTP(FTP_HOST)
        ftp.login(FTP_USER, FTP_PASSWORD)
        print("\n✅ FTP 연결 성공\n")
        
        # 디렉토리 이동
        current_dir = '/'
        try:
            ftp.cwd('public_html')
            current_dir = '/public_html'
        except:
            try:
                ftp.cwd('www')
                current_dir = '/www'
            except:
                pass
        
        print(f"📁 현재 디렉토리: {current_dir}\n")
        
        # 각 파일 확인
        print("📋 파일 확인 결과:\n")
        for filename in check_files:
            try:
                # SIZE 명령으로 파일 크기 확인
                size = ftp.size(filename)
                if size:
                    print(f"✅ {filename}")
                    print(f"   크기: {size:,} bytes ({size/1024:.1f} KB)")
                    print(f"   URL: https://health9988234.mycafe24.com/{filename}\n")
                else:
                    print(f"⚠️  {filename} - 파일이 0 바이트\n")
            except Exception as e:
                print(f"❌ {filename} - 파일 없음 또는 접근 불가")
                print(f"   오류: {e}\n")
        
        # 서버의 모든 .html 파일 목록 (일부만)
        print("\n📂 서버의 HTML 파일 목록 (처음 20개):\n")
        try:
            ftp.retrlines('LIST *.html', lambda x: print(f"   {x}"))
        except Exception as e:
            print(f"   목록 가져오기 실패: {e}")
        
        ftp.quit()
        
    except Exception as e:
        print(f"\n❌ 오류: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_files()

