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

def reupload_files():
    """골다공증 및 관련 파일 재업로드"""
    print("=" * 60)
    print("🔄 파일 재업로드")
    print("=" * 60)
    
    # 업로드할 파일 (관절/근골격계 전체)
    files_to_upload = [
        'category-관절근골격계.html',
        'sub-골다공증.html',
        'sub-퇴행성관절염.html',
        'sub-허리디스크목디스크.html',
        'sub-오십견.html',
    ]
    
    print(f"\n📝 {len(files_to_upload)}개 파일 재업로드\n")
    
    try:
        # FTP 연결
        print("🔌 FTP 서버 연결 중...")
        ftp = FTP(FTP_HOST)
        ftp.login(FTP_USER, FTP_PASSWORD)
        ftp.encoding = 'utf-8'
        print("   ✅ FTP 연결 성공\n")
        
        # 디렉토리 확인
        try:
            ftp.cwd('public_html')
            target_dir = 'public_html'
        except:
            try:
                ftp.cwd('www')
                target_dir = 'www'
            except:
                target_dir = 'root'
        
        print(f"   📁 작업 디렉토리: {target_dir}\n")
        
        # 바이너리 모드 설정
        ftp.voidcmd('TYPE I')
        
        # 파일 업로드
        print("📤 파일 업로드 시작...\n")
        success_count = 0
        
        for filename in files_to_upload:
            if not os.path.exists(filename):
                print(f"   ⚠️  {filename} - 로컬에 파일이 없습니다")
                continue
            
            try:
                with open(filename, 'rb') as f:
                    ftp.storbinary(f'STOR {filename}', f)
                
                # 파일 크기 확인
                size = os.path.getsize(filename)
                size_kb = size / 1024
                
                if filename.startswith('category-'):
                    print(f"   📂 {filename} ({size_kb:.1f} KB)")
                else:
                    print(f"   📄 {filename} ({size_kb:.1f} KB)")
                success_count += 1
            except Exception as e:
                print(f"   ❌ {filename} - 오류: {e}")
        
        # 업로드된 파일 확인
        print("\n📋 서버에 업로드된 파일 확인 중...\n")
        try:
            files_on_server = ftp.nlst()
            for filename in files_to_upload:
                if filename in files_on_server:
                    print(f"   ✅ {filename} - 서버에 존재")
                else:
                    print(f"   ❌ {filename} - 서버에 없음")
        except Exception as e:
            print(f"   ⚠️  파일 목록 확인 실패: {e}")
        
        ftp.quit()
        
        print(f"\n✅ 총 {success_count}/{len(files_to_upload)}개 파일 재업로드 완료!")
        print("\n" + "=" * 60)
        print("🔗 테스트 URL:")
        print("=" * 60)
        print("   https://health9988234.mycafe24.com/category-관절근골격계.html")
        print("   https://health9988234.mycafe24.com/sub-골다공증.html")
        print("   https://health9988234.mycafe24.com/sub-퇴행성관절염.html")
        print("   https://health9988234.mycafe24.com/sub-허리디스크목디스크.html")
        print("   https://health9988234.mycafe24.com/sub-오십견.html")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ FTP 오류: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    reupload_files()

