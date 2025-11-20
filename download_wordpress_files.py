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

# sub-*.html 파일들도 다운로드
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

# post-detail.html도 확인
OTHER_FILES = [
    "post-detail.html",
]


def download_file(ftp, remote_file, local_file):
    """FTP에서 파일 다운로드"""
    try:
        with open(local_file, 'wb') as f:
            ftp.retrbinary(f'RETR {remote_file}', f.write)
        return True
    except Exception as e:
        return False, str(e)


def list_remote_files(ftp, pattern="*.html"):
    """서버에 있는 파일 목록 가져오기"""
    try:
        files = []
        ftp.retrlines('NLST', files.append)
        return [f for f in files if pattern in f or f.endswith('.html') or f == '.htaccess']
    except Exception as e:
        print(f"  ⚠️ 파일 목록 가져오기 실패: {e}")
        return []


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
        
        # 서버에 있는 파일 목록 확인
        print("\n📋 서버에 있는 HTML 파일 목록 확인 중...")
        remote_files = list_remote_files(ftp)
        print(f"   발견된 파일: {len(remote_files)}개")
        for f in remote_files[:20]:  # 처음 20개만 표시
            print(f"   - {f}")
        if len(remote_files) > 20:
            print(f"   ... 외 {len(remote_files) - 20}개")
        
        # 다운로드할 파일 목록 합치기
        all_files = FILES_TO_DOWNLOAD + SUB_CATEGORY_FILES + OTHER_FILES
        
        print(f"\n📥 파일 다운로드 시작...\n")
        downloaded_count = 0
        failed_files = []
        
        for file in all_files:
            # 서버에 파일이 있는지 확인
            if file in remote_files or file == '.htaccess':
                try:
                    print(f"  다운로드 중: {file}...", end=" ")
                    
                    # .htaccess 파일은 숨김 파일이므로 특별 처리
                    if file == '.htaccess':
                        try:
                            with open('.htaccess', 'wb') as f:
                                ftp.retrbinary('RETR .htaccess', f.write)
                            print("✅ 완료")
                            downloaded_count += 1
                        except:
                            # .htaccess가 없을 수도 있음
                            print("⚠️ 없음")
                    else:
                        with open(file, 'wb') as f:
                            ftp.retrbinary(f'RETR {file}', f.write)
                        print("✅ 완료")
                        downloaded_count += 1
                        
                except Exception as e:
                    print(f"❌ 실패: {str(e)[:50]}")
                    failed_files.append(file)
            else:
                print(f"  ⚠️ {file} - 서버에 없음")
        
        # sub-*.html 파일들 자동 검색
        print(f"\n🔍 sub-*.html 파일 자동 검색 중...")
        sub_files = [f for f in remote_files if f.startswith('sub-') and f.endswith('.html')]
        for sub_file in sub_files:
            if sub_file not in all_files:
                try:
                    print(f"  다운로드 중: {sub_file}...", end=" ")
                    with open(sub_file, 'wb') as f:
                        ftp.retrbinary(f'RETR {sub_file}', f.write)
                    print("✅ 완료")
                    downloaded_count += 1
                except Exception as e:
                    print(f"❌ 실패: {str(e)[:50]}")
        
        ftp.quit()
        
        print(f"\n" + "=" * 60)
        print(f"✅ 다운로드 완료!")
        print("=" * 60)
        print(f"\n📊 다운로드 결과:")
        print(f"   ✅ 성공: {downloaded_count}개")
        if failed_files:
            print(f"   ❌ 실패: {len(failed_files)}개")
            for f in failed_files:
                print(f"      - {f}")
        
        print(f"\n💡 이제 다운로드된 파일들로 수정을 시작할 수 있습니다.")
        print("=" * 60)
            
    except Exception as e:
        print(f"\n❌ FTP 다운로드 오류: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

