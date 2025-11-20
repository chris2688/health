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

# 업로드할 카테고리 파일 목록
CATEGORY_FILES = [
    "category-심혈관질환.html",
    "category-당뇨병.html",
    "category-관절근골격계.html",
    "category-호르몬내분비.html",
    "category-정신건강신경계.html",
    "category-소화기질환.html",
    "category-안과치과기타.html",
]


def upload_file(ftp, local_file, remote_file):
    """FTP로 파일 업로드"""
    try:
        with open(local_file, "rb") as f:
            ftp.storbinary(f"STOR {remote_file}", f)
        file_size = os.path.getsize(local_file)
        return True, file_size
    except Exception as e:
        return False, str(e)


def main():
    """메인 실행"""
    print("=" * 60)
    print("📤 수정된 카테고리 파일들을 WordPress 서버에 업로드")
    print("=" * 60)
    
    # 업로드할 파일 확인
    existing_files = []
    missing_files = []
    
    for file in CATEGORY_FILES:
        if os.path.exists(file):
            existing_files.append(file)
        else:
            missing_files.append(file)
    
    if missing_files:
        print(f"\n⚠️ 다음 파일들이 로컬에 없습니다:")
        for f in missing_files:
            print(f"   - {f}")
        print()
    
    if not existing_files:
        print("\n❌ 업로드할 파일이 없습니다!")
        return
    
    print(f"\n📋 업로드할 파일: {len(existing_files)}개")
    for f in existing_files:
        size = os.path.getsize(f)
        print(f"   - {f} ({size:,} bytes)")
    
    try:
        print(f"\n🔗 FTP 서버 연결 중...")
        ftp = FTP()
        ftp.encoding = 'utf-8'
        ftp.connect(FTP_HOST, FTP_PORT, timeout=10)
        print("✅ 연결 성공!")
        
        print(f"🔐 로그인 중...")
        ftp.login(FTP_USER, FTP_PASS)
        print("✅ 로그인 성공!")
        
        # 현재 디렉토리 확인
        current_dir = ftp.pwd()
        print(f"\n📂 현재 디렉토리: {current_dir}")
        
        print(f"\n📤 파일 업로드 시작...\n")
        uploaded_count = 0
        failed_files = []
        
        for file in existing_files:
            try:
                print(f"  업로드 중: {file}...", end=" ")
                success, result = upload_file(ftp, file, file)
                if success:
                    print(f"✅ 완료 ({result:,} bytes)")
                    uploaded_count += 1
                else:
                    print(f"❌ 실패: {result[:50]}")
                    failed_files.append((file, result))
            except Exception as e:
                print(f"❌ 오류: {str(e)[:50]}")
                failed_files.append((file, str(e)))
        
        ftp.quit()
        
        print(f"\n" + "=" * 60)
        print(f"✅ 업로드 완료!")
        print("=" * 60)
        print(f"\n📊 업로드 결과:")
        print(f"   ✅ 성공: {uploaded_count}개")
        if failed_files:
            print(f"   ❌ 실패: {len(failed_files)}개")
            for file, error in failed_files:
                print(f"      - {file}: {error[:50]}")
        
        print(f"\n💡 모든 카테고리 파일이 WordPress 서버에 업로드되었습니다.")
        print(f"   웹사이트에서 상단 여백 변경사항을 확인하세요:")
        print(f"   https://health9988234.mycafe24.com/")
        print("=" * 60)
            
    except Exception as e:
        print(f"\n❌ FTP 업로드 오류: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

