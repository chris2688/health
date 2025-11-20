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

def upload_diabetes_files():
    """당뇨병 관련 파일 업로드"""
    print("=" * 60)
    print("🚀 당뇨병 페이지 FTP 업로드")
    print("=" * 60)
    
    # 업로드할 파일 목록
    files_to_upload = [
        'category-당뇨병.html',
        'sub-당뇨.html',
        'sub-공복혈당장애.html',
        'sub-당뇨병합병증.html'
    ]
    
    print(f"\n📝 총 {len(files_to_upload)}개 파일 업로드 예정:")
    for f in files_to_upload:
        print(f"   - {f}")
    print()
    
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
        print("📤 파일 업로드 시작...\n")
        success_count = 0
        
        for filename in files_to_upload:
            if not os.path.exists(filename):
                print(f"   ⚠️  {filename} - 파일을 찾을 수 없습니다")
                continue
            
            try:
                with open(filename, 'rb') as f:
                    ftp.storbinary(f'STOR {filename}', f)
                
                if filename.startswith('category-'):
                    print(f"   📂 {filename}")
                elif filename.startswith('sub-'):
                    print(f"   📄 {filename}")
                else:
                    print(f"   ✅ {filename}")
                success_count += 1
            except Exception as e:
                print(f"   ❌ {filename} - 오류: {e}")
        
        ftp.quit()
        
        print(f"\n✅ 총 {success_count}/{len(files_to_upload)}개 파일 업로드 완료!")
        print("\n" + "=" * 60)
        print("🎉 당뇨병 페이지 업로드 완료!")
        print("=" * 60)
        print("\n📋 구조:")
        print("   메인 페이지 → 당뇨병 카드")
        print("   └─ category-당뇨병.html")
        print("       ├─ 💉 당뇨 (sub-당뇨.html)")
        print("       ├─ 🩸 공복혈당장애 (sub-공복혈당장애.html)")
        print("       └─ ⚕️ 당뇨병 합병증 (sub-당뇨병합병증.html)")
        print("\n🌐 테스트:")
        print("   https://health9988234.mycafe24.com")
        print("   → 당뇨병 카드 클릭")
        print("   → 3개 서브 카테고리 확인")
        print("   → 각 페이지에서 WordPress 글 매핑 확인")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ FTP 오류: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    upload_diabetes_files()

