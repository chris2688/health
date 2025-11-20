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

print("=" * 70)
print("🔍 서버 파일 확인 및 재업로드")
print("=" * 70)

try:
    ftp = FTP(FTP_HOST)
    ftp.login(FTP_USER, FTP_PASSWORD)
    ftp.encoding = 'utf-8'
    print("\n✅ FTP 연결 성공\n")
    
    # 디렉토리 이동
    try:
        ftp.cwd('public_html')
        print("📁 작업 디렉토리: public_html\n")
    except:
        try:
            ftp.cwd('www')
            print("📁 작업 디렉토리: www\n")
        except:
            print("📁 작업 디렉토리: root\n")
    
    # lifestyle 관련 파일들 확인
    print("🔍 lifestyle 관련 파일 확인:\n")
    
    files_to_check = [
        'lifestyle-habits.html',
        'lifestyle-tips.html',
        'lifestyle-main.html',
        'food-main.html',
        'exercise-main.html',
    ]
    
    existing_files = []
    missing_files = []
    
    try:
        # 서버의 파일 목록 가져오기 (바이너리 모드)
        file_list = []
        ftp.retrlines('LIST', file_list.append)
        
        server_files = []
        for line in file_list:
            parts = line.split()
            if len(parts) > 8:
                filename = parts[-1]
                server_files.append(filename)
        
        for filename in files_to_check:
            if filename in server_files:
                print(f"✅ {filename} - 존재")
                existing_files.append(filename)
            else:
                print(f"❌ {filename} - 없음!")
                missing_files.append(filename)
    
    except Exception as e:
        print(f"⚠️  파일 목록 확인 오류: {e}")
        print("모든 파일을 강제로 재업로드합니다.\n")
        missing_files = files_to_check
    
    # 누락된 파일들 업로드
    if missing_files:
        print(f"\n📤 {len(missing_files)}개 파일 업로드 중...\n")
        
        for filename in missing_files:
            if os.path.exists(filename):
                try:
                    with open(filename, 'rb') as f:
                        ftp.storbinary(f'STOR {filename}', f)
                    
                    size = os.path.getsize(filename) / 1024
                    print(f"✅ {filename} ({size:.1f} KB) 업로드 완료")
                except Exception as e:
                    print(f"❌ {filename} - 업로드 실패: {e}")
            else:
                print(f"⚠️  {filename} - 로컬 파일 없음")
    else:
        print("\n✅ 모든 파일이 서버에 있습니다!")
    
    ftp.quit()
    
    print("\n" + "=" * 70)
    print("🎉 완료!")
    print("=" * 70)
    print("\n🔗 테스트 URL:")
    print("   https://health9988234.mycafe24.com/lifestyle-habits.html")
    print("=" * 70)

except Exception as e:
    print(f"\n❌ FTP 오류: {e}")
    import traceback
    traceback.print_exc()

