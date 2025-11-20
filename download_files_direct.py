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

# 다운로드할 파일 목록
FILES_TO_DOWNLOAD = [
    "index-v2.html",
    "category-심혈관질환.html",
    "category-당뇨병.html",
    "category-관절근골격계.html",
    "category-호르몬내분비.html",
    "category-정신건강신경계.html",
    "category-소화기질환.html",
    "category-안과치과기타.html",
    "food-main.html",
    "exercise-main.html",
    "lifestyle-main.html",
    "news-main.html",
    ".htaccess",
]

# sub-*.html 파일들
SUB_CATEGORY_FILES = [
    "sub-고혈압.html",
    "sub-당뇨.html",
    "sub-고지혈증.html",
    "sub-당뇨병합병증.html",
    "sub-공복혈당.html",
    "sub-공복혈당장애.html",
    "sub-혈당관리.html",
    "sub-허리디스크.html",
    "sub-허리디스크목디스크.html",
    "sub-당뇨합병증.html",
]

OTHER_FILES = [
    "post-detail.html",
]


def download_file(ftp, remote_file, local_file):
    """FTP에서 파일 다운로드"""
    try:
        with open(local_file, 'wb') as f:
            ftp.retrbinary(f'RETR {remote_file}', f.write)
        file_size = os.path.getsize(local_file)
        return True, file_size
    except Exception as e:
        return False, str(e)


def main():
    """메인 실행"""
    print("=" * 60)
    print("📥 WordPress 서버에서 파일 다운로드")
    print("=" * 60)
    
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
        
        # 다운로드할 파일 목록 합치기
        all_files = FILES_TO_DOWNLOAD + SUB_CATEGORY_FILES + OTHER_FILES
        
        print(f"\n📥 파일 다운로드 시작...\n")
        downloaded_count = 0
        failed_files = []
        skipped_files = []
        
        for file in all_files:
            try:
                print(f"  다운로드 중: {file}...", end=" ")
                
                # .htaccess 파일은 특별 처리
                if file == '.htaccess':
                    try:
                        with open('.htaccess', 'wb') as f:
                            ftp.retrbinary('RETR .htaccess', f.write)
                        file_size = os.path.getsize('.htaccess')
                        print(f"✅ 완료 ({file_size} bytes)")
                        downloaded_count += 1
                    except Exception as e:
                        if "550" in str(e) or "not found" in str(e).lower():
                            print("⚠️ 서버에 없음")
                            skipped_files.append(file)
                        else:
                            print(f"❌ 실패: {str(e)[:50]}")
                            failed_files.append(file)
                else:
                    success, result = download_file(ftp, file, file)
                    if success:
                        print(f"✅ 완료 ({result} bytes)")
                        downloaded_count += 1
                    else:
                        if "550" in result or "not found" in result.lower():
                            print("⚠️ 서버에 없음")
                            skipped_files.append(file)
                        else:
                            print(f"❌ 실패: {result[:50]}")
                            failed_files.append(file)
                            
            except Exception as e:
                print(f"❌ 오류: {str(e)[:50]}")
                failed_files.append(file)
        
        ftp.quit()
        
        print(f"\n" + "=" * 60)
        print(f"✅ 다운로드 완료!")
        print("=" * 60)
        print(f"\n📊 다운로드 결과:")
        print(f"   ✅ 성공: {downloaded_count}개")
        if skipped_files:
            print(f"   ⚠️ 서버에 없음: {len(skipped_files)}개")
            for f in skipped_files[:10]:
                print(f"      - {f}")
            if len(skipped_files) > 10:
                print(f"      ... 외 {len(skipped_files) - 10}개")
        if failed_files:
            print(f"   ❌ 실패: {len(failed_files)}개")
            for f in failed_files:
                print(f"      - {f}")
        
        print(f"\n💡 다운로드된 파일들:")
        for file in all_files:
            if os.path.exists(file):
                size = os.path.getsize(file)
                print(f"   ✅ {file} ({size} bytes)")
        
        print(f"\n💡 이제 다운로드된 파일들로 수정을 시작할 수 있습니다.")
        print("=" * 60)
            
    except Exception as e:
        print(f"\n❌ FTP 다운로드 오류: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

